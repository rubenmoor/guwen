from selectable.base import ModelLookup
from selectable.registry import registry

from models import EnglishTerm

class EnglishTermLookup(ModelLookup):
	model = EnglishTerm
	search_fields = ('term__istartswith',)

registry.register(EnglishTermLookup)