'''
Created on Oct 28, 2016

@author: jupark
'''

from django import template
register = template.Library()
    
#@register.filter(name='key')
def attribute(d, key_name):
    try:
        value = getattr(d, key_name)
    except KeyError:
        from django.conf import settings

        value = settings.TEMPLATE_STRING_IF_INVALID

    return value

register.filter('attribute', attribute)

def key(d, key_name):
    try:
        value = d[key_name]
    except KeyError:
        from django.conf import settings

        value = settings.TEMPLATE_STRING_IF_INVALID

    return value
register.filter('key', key)

def times(number):
    return range(number)
register.filter('range', times)

def firstThree(value):
    return value[0:3]
register.filter('firstThree', firstThree)