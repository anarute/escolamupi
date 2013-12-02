# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from accounts.models import TimtecUser


class Note(models.Model):
    text = models.TextField(_('Note'))
    user = models.ForeignKey(TimtecUser, verbose_name=_('User'))
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
