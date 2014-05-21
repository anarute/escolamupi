# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group, AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from allauth.account.signals import user_signed_up

from paypal.standard.ipn.signals import (payment_was_successful, subscription_signup, 
						payment_was_flagged, payment_was_refunded, 
						payment_was_reversed)
import re
import os
import hashlib


def path_and_rename(path):
    def wrapper(instance, filename):
        root, ext = os.path.splitext(filename)
        m = hashlib.md5()
        m.update(root.encode('utf-8'))
        m.update(instance.username.encode('utf-8'))
        filename = m.hexdigest() + ext
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper


class TimtecUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_REGEXP = re.compile('^[\w.+-]+$')
    username = models.CharField(
        _('Username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    './+/-/_ characters'),
        validators=[
            validators.RegexValidator(USERNAME_REGEXP, _('Enter a valid username.'), 'invalid')
        ])

    email = models.EmailField(_('Email address'), blank=False, unique=True)
    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('Staff status'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)

    picture = models.ImageField(_("Picture"), upload_to=path_and_rename('user-pictures'), blank=True)
    occupation = models.CharField(_('Occupation'), max_length=30, blank=True)
    city = models.CharField(_('City'), max_length=30, blank=True)
    site = models.URLField(_('Site'), blank=True)
    biography = models.TextField(_('Biography'), blank=True)
    accepted_terms = models.BooleanField(_('Accepted terms and condition'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        if self.first_name or self.last_name:
            return self.get_full_name()
        return self.email

    def get_picture_url(self):
        if not self.picture:
            location = "/%s/%s" % (settings.STATIC_URL, 'img/avatar-default.png')
        else:
            location = "/%s/%s" % (settings.MEDIA_URL, self.picture)
        return re.sub('/+', '/', location)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def get_user_type(self):
        if self.is_superuser:
            return "superuser"
	elif self.groups.filter(name='professors').count():
            return "professors"
        elif self.groups.filter(name='students').count():
            return "students"
        return "unidentified"

    def is_pilot(self):
        return self.groups.filter(name='pilot_course').count() > 0

    @staticmethod
    def add_default_group(sender, user, **kwargs):
        if settings.REGISTRATION_DEFAULT_GROUP_NAME:
            user.groups.add(Group.objects.get(name=settings.REGISTRATION_DEFAULT_GROUP_NAME))
            user.save()

def paypal_signal_was_successful(sender, **kwargs):
	# Verify if the message is from paypal 
	# https://www.paypal.com/cgi-bin/webscr?cmd=_notify-validate&mc_gross=19.95&protection_eligibility=Eligible
	# if yes, it will return VERIFIED

	# Verify if the message does not exist already txn_id = 61E67681CH3238416
	
	send_mail("Uepa", "=)", "contato@mupi.me", ["virgilio.santos@gmail.com"])		
	from urlparse import parse_qs
	custom = parse_qs(sender.custom)
	print custom
 	print sender.txn_type + " -- " + custom['user_id'][0] + " -- " + custom['user_mail'][0]
	user = TimtecUser.objects.get(id=custom['user_id'][0])
	print user.email + "--" + custom['user_mail'][0]
	if sender.payment_status == "Completed":
		user.is_staff = True
		user.save() 


def paypal_signal_subscription_signup(sender, **kwargs):
	send_mail("Uepa subscription!", "=)", "contato@mupi.me", ["virgilio.santos@gmail.com"])

payment_was_successful.connect(paypal_signal_was_successful)
#payment_was_flagged.connect(paypal_signal_was_successful)
#payment_was_refunded.connect(paypal_signal_was_successful)
#payment_was_reversed.connect(paypal_signal_was_successful)

subscription_signup.connect(paypal_signal_subscription_signup)

user_signed_up.connect(TimtecUser.add_default_group, dispatch_uid="TimtecUser.add_default_group")

