from django import template

register = template.Library()

@register.filter
def at(dictionary, key):
	return dictionary[key]