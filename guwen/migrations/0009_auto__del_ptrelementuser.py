# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'PtrElementUser'
        db.delete_table(u'guwen_ptrelementuser')

        # Adding M2M table for field hanziUsers on 'EnglishTerm'
        m2m_table_name = 'guwen_ptrelementuser'
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('englishterm', models.ForeignKey(orm[u'guwen.englishterm'], null=False)),
            ('hanzi', models.ForeignKey(orm[u'guwen.hanzi'], null=False))
        ))
        db.create_unique(m2m_table_name, ['englishterm_id', 'hanzi_id'])


    def backwards(self, orm):
        # Adding model 'PtrElementUser'
        db.create_table(u'guwen_ptrelementuser', (
            ('englishterm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guwen.EnglishTerm'])),
            ('hanzi', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['guwen.Hanzi'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'guwen', ['PtrElementUser'])

        # Removing M2M table for field hanziUsers on 'EnglishTerm'
        db.delete_table('guwen_ptrelementuser')


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
            'hanziUsers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'termElements'", 'symmetrical': 'False', 'db_table': "'guwen_ptrelementuser'", 'to': u"orm['guwen.Hanzi']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '72'})
        },
        u'guwen.hanzi': {
            'Meta': {'object_name': 'Hanzi'},
            'char': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'dataExceptionInfo': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'heisigBook': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'heisigFrame': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'heisigID': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'heisigLesson': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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