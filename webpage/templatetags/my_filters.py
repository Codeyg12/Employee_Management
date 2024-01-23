from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

def currency(dollars):
    dollars = round(float(dollars), 2)
    return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])

register.filter('currency', currency)

@register.filter
def get_display_value(element, attr):
    if element and hasattr(element, attr):
        return getattr(element, attr)
    else: 
        return 'N/A'