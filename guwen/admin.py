from django.contrib import admin
from models import *

admin.site.register(Hanzi)
admin.site.register(HanziMeta)
admin.site.register(EnglishTerm)
admin.site.register(Syllable)
admin.site.register(PtrHanziSyllable)
admin.site.register(LexicalEntry)
admin.site.register(CedictDataSingle)