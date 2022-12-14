# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Hanzi'
        db.create_table(u'guwen_hanzi', (
            ('heisigID', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('char', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('isHeisigPrimitive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isRealPrimitive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('numStrokes', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, blank=True)),
            ('heisigBook', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, blank=True)),
            ('heisigLesson', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, blank=True)),
            ('heisigFrame', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, blank=True)),
            ('dataExceptionInfo', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, blank=True)),
            ('isDataComplete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isDataLocked', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'guwen', ['Hanzi'])

        # Adding model 'EnglishTerm'
        db.create_table(u'guwen_englishterm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=72)),
            ('hanziCharacter', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='termKeyword', unique=True, null=True, to=orm['guwen.Hanzi'])),
            ('hanziPrimitive', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='termPrimitiveMeanings', null=True, to=orm['guwen.Hanzi'])),
        ))
        db.send_create_signal(u'guwen', ['EnglishTerm'])

        # Adding model 'HanziMeta'
        db.create_table(u'guwen_hanzimeta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('numHanzi', self.gf('django.db.models.fields.IntegerField')()),
            ('maxHeisigID', self.gf('django.db.models.fields.IntegerField')()),
            ('percentageDataComplete', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=1)),
            ('percentageDataLocked', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=1)),
            ('dateUpdated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'guwen', ['HanziMeta'])

        # Adding model 'PtrElementUser'
        db.create_table(u'guwen_ptrelementuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('element', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guwen.EnglishTerm'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guwen.Hanzi'])),
        ))
        db.send_create_signal(u'guwen', ['PtrElementUser'])

        # Adding model 'Syllable'
        db.create_table(u'guwen_syllable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pinyin_latin', self.gf('django.db.models.fields.CharField')(unique=True, max_length=8)),
            ('pinyin', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('pinyinWOTone', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('tone', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'guwen', ['Syllable'])

        # Adding model 'PtrHanziSyllable'
        db.create_table(u'guwen_ptrhanzisyllable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hanzi', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ptrSyllableLexicalEntry', to=orm['guwen.Hanzi'])),
            ('syllable', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ptrHanziLexicalEntry', to=orm['guwen.Syllable'])),
            ('lexical_entry', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ptrHanziSyllable', null=True, to=orm['guwen.LexicalEntry'])),
        ))
        db.send_create_signal(u'guwen', ['PtrHanziSyllable'])

        # Adding model 'LexicalEntry'
        db.create_table(u'guwen_lexicalentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('hanzi', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lexical_entries', to=orm['guwen.Hanzi'])),
        ))
        db.send_create_signal(u'guwen', ['LexicalEntry'])

        # Adding model 'CedictDataSingle'
        db.create_table(u'guwen_cedictdatasingle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('simplified_hanzi', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('traditional_hanzi', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('latin_pinyin', self.gf('django.db.models.fields.CharField')(max_length=72)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'guwen', ['CedictDataSingle'])

        # Adding model 'HeisigExcelPinyin'
        db.create_table(u'guwen_heisigexcelpinyin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('heisigID', self.gf('django.db.models.fields.IntegerField')()),
            ('pinyin', self.gf('django.db.models.fields.CharField')(max_length=72)),
        ))
        db.send_create_signal(u'guwen', ['HeisigExcelPinyin'])


    def backwards(self, orm):
        # Deleting model 'Hanzi'
        db.delete_table(u'guwen_hanzi')

        # Deleting model 'EnglishTerm'
        db.delete_table(u'guwen_englishterm')

        # Deleting model 'HanziMeta'
        db.delete_table(u'guwen_hanzimeta')

        # Deleting model 'PtrElementUser'
        db.delete_table(u'guwen_ptrelementuser')

        # Deleting model 'Syllable'
        db.delete_table(u'guwen_syllable')

        # Deleting model 'PtrHanziSyllable'
        db.delete_table(u'guwen_ptrhanzisyllable')

        # Deleting model 'LexicalEntry'
        db.delete_table(u'guwen_lexicalentry')

        # Deleting model 'CedictDataSingle'
        db.delete_table(u'guwen_cedictdatasingle')

        # Deleting model 'HeisigExcelPinyin'
        db.delete_table(u'guwen_heisigexcelpinyin')


    models = {
        u'guwen.cedictdatasingle': {
            'Meta': {'object_name': 'CedictDataSingle'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latin_pinyin': ('django.db.models.fields.CharField', [], {'max_length': '72'}),
            'simplified_hanzi': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'traditional_hanzi': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'guwen.englishterm': {
            'Meta': {'object_name': 'EnglishTerm'},
            'hanziCharacter': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'termKeyword'", 'unique': 'True', 'null': 'True', 'to': u"orm['guwen.Hanzi']"}),
            'hanziPrimitive': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'termPrimitiveMeanings'", 'null': 'True', 'to': u"orm['guwen.Hanzi']"}),
            'hanziUsers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'termElements'", 'symmetrical': 'False', 'through': u"orm['guwen.PtrElementUser']", 'to': u"orm['guwen.Hanzi']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '72'})
        },
        u'guwen.hanzi': {
            'Meta': {'object_name': 'Hanzi'},
            'char': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'dataExceptionInfo': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'heisigBook': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'heisigFrame': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'heisigID': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'heisigLesson': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'isDataComplete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isDataLocked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isHeisigPrimitive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isRealPrimitive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'numStrokes': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'guwen.hanzimeta': {
            'Meta': {'object_name': 'HanziMeta'},
            'dateUpdated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maxHeisigID': ('django.db.models.fields.IntegerField', [], {}),
            'numHanzi': ('django.db.models.fields.IntegerField', [], {}),
            'percentageDataComplete': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '1'}),
            'percentageDataLocked': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '1'})
        },
        u'guwen.heisigexcelpinyin': {
            'Meta': {'object_name': 'HeisigExcelPinyin'},
            'heisigID': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pinyin': ('django.db.models.fields.CharField', [], {'max_length': '72'})
        },
        u'guwen.lexicalentry': {
            'Meta': {'object_name': 'LexicalEntry'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'hanzi': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lexical_entries'", 'to': u"orm['guwen.Hanzi']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'guwen.ptrelementuser': {
            'Meta': {'object_name': 'PtrElementUser'},
            'element': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['guwen.EnglishTerm']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['guwen.Hanzi']"})
        },
        u'guwen.ptrhanzisyllable': {
            'Meta': {'object_name': 'PtrHanziSyllable'},
            'hanzi': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ptrSyllableLexicalEntry'", 'to': u"orm['guwen.Hanzi']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lexical_entry': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ptrHanziSyllable'", 'null': 'True', 'to': u"orm['guwen.LexicalEntry']"}),
            'syllable': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ptrHanziLexicalEntry'", 'to': u"orm['guwen.Syllable']"})
        },
        u'guwen.syllable': {
            'Meta': {'object_name': 'Syllable'},
            'hanzis': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'syllables'", 'symmetrical': 'False', 'through': u"orm['guwen.PtrHanziSyllable']", 'to': u"orm['guwen.Hanzi']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pinyin': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'pinyinWOTone': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'pinyin_latin': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'tone': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['guwen']