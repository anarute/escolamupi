import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def allow_html_markdown(value):
    extensions = ["nl2br", ]

    return mark_safe(markdown.markdown(force_unicode(value),
                                       extensions,
                                       safe_mode=False,
                                       enable_attributes=False))



