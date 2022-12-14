# -*- coding: utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit, Button
from crispy_forms.bootstrap import StrictButton, FormActions, FieldWithButtons
import selectable.forms as selectable

from fields import StringListField
from lookups import EnglishTermLookup
from models import *

class CedictUpdateForm(forms.Form):
    cedict_gz = forms.FileField(
        label='Latest cedict version (.gz-file)'
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('cedict_update')
        self.helper.layout = Layout(
            'cedict_gz',
            FormActions(
                Submit('save', 'Save', css_class='btn-sm'),
                Button('cancel', 'Cancel', css_class='btn-sm', onclick='window.history.back()'),
                ),            
            )
        super(CedictUpdateForm, self).__init__(*args, **kwargs)

class SearchForm(forms.Form):
    input_search = forms.CharField(
        label='Search all volumes',
        widget=forms.TextInput(attrs={
            'placeholder': u'字, pīn yin1, keyword, 12 (ALT+F)',
            'size': '24',
            'accesskey': 'F',
            }),
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_action = reverse('search')
        #self.helper.attrs = {}
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-8'
        self.helper.layout = Layout(
            FieldWithButtons(
                'input_search',
                StrictButton('Go!', type='submit'),
                )
            )
        super(SearchForm, self).__init__(*args, **kwargs)

class HanziEditForm(forms.ModelForm):
    keyword = forms.CharField(max_length=72)
    # edit primitive meanings by editing english terms tbd.
    primitive_meanings = StringListField(required=False)
    # explicitly setting formfield disables django's automated handling of m2m saving
    termElements = forms.ModelMultipleChoiceField(
        EnglishTerm.objects,
        label='Elements',
        widget=selectable.AutoCompleteSelectMultipleWidget(
            EnglishTermLookup,
            # position='top-inline',
            position='top',
            ),
        required=False,
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('hanzi_edit', args=[kwargs['instance'].pk])
        self.helper.layout = Layout(
            'heisigBook',
            'heisigLesson',
            'heisigFrame',
            'heisigID',
            'char',
            'numStrokes',
            'keyword',
            'primitive_meanings',
            'termElements',
            'isHeisigPrimitive',
            'isRealPrimitive',
            'dataExceptionInfo',
            'isDataComplete',
            'isDataLocked',
            FormActions(
                Submit('save', 'Save', css_class='btn-sm'),
                Button('cancel', 'Cancel', css_class='btn-sm', onclick='window.history.back()'),
                ),
            )

        kwargs.setdefault('initial', {}).update({
            'keyword': kwargs['instance'].termKeyword,
            'primitive_meanings': '\n'.join(
                unicode(term) for term in kwargs['instance'].termPrimitiveMeanings.all()
                ),
            'termElements': kwargs['instance'].termElements.all(),
        })
        super(HanziEditForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(HanziEditForm, self).save(commit=False)
        instance.termKeyword.term = self.cleaned_data['keyword']

        if commit:
            instance.save()
            instance.termKeyword.save()
            elements_new = set(self.cleaned_data['termElements'])
            elements_old = set(instance.termElements.all())
            instance.termElements.add(*(elements_new - elements_old))
            instance.termElements.remove(*(elements_old - elements_new))
            primitive_meanings_new = set(self.cleaned_data['primitive_meanings'])
            primitive_meanings_old = set(et.term for et in instance.termPrimitiveMeanings.all())
            for termString in  primitive_meanings_new - primitive_meanings_old:
                EnglishTerm.objects.create(term=termString, hanziPrimitive=instance)
            LexicalEntry.update_hanzi(instance)
            HanziMeta.update()
        return instance 

    class Meta:
        model = Hanzi
        fields = [
            'heisigBook',
            'heisigLesson',
            'heisigFrame',
            'heisigID',
            'char',
            'numStrokes',
            'termElements',
            'isHeisigPrimitive',
            'isRealPrimitive',
            'dataExceptionInfo',
            'isDataComplete',
            'isDataLocked',
            ]

class HanziAddForm(HanziEditForm):
    primitive_meanings = StringListField(required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('hanzi_add')
        self.helper.layout = Layout(
            'heisigBook',
            'heisigLesson',
            'heisigFrame',
            'heisigID',
            'char',
            'numStrokes',
            'keyword',
            'primitive_meanings',
            'termElements',
            'isHeisigPrimitive',
            'isRealPrimitive',
            'dataExceptionInfo',
            'isDataComplete',
            'isDataLocked',
            )
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-sm'))
        super(HanziEditForm, self).__init__(*args, **kwargs)
        self.fields['char'].widget = forms.TextInput(attrs={
            'autofocus': 'autofocus',
            'maxlength': 1,
            })

    def clean_keyword(self):
        keyword = self.cleaned_data['keyword']
        if EnglishTerm.objects.filter(term=keyword).exists():
            raise forms.ValidationError(
                'The term {} exists already in the database.'.format(keyword)
                )
        return keyword
    
    def clean_primitive_meanings(self):
        primitive_meanings = self.cleaned_data['primitive_meanings']
        terms = EnglishTerm.objects.filter(term__in=primitive_meanings)
        if terms.count() > 0:
            raise forms.ValidationError(
                'The term {} exists already in the database.'.format(term[0].term)
                )
        return primitive_meanings
            
    def clean(self):
        cleaned_data = super(HanziEditForm, self).clean()
        heisigFrame = cleaned_data.get('heisigFrame', 0)
        heisigBook = cleaned_data.get('heisigBook', 0)
        heisigID = cleaned_data.get('heisigID', 0)
        hanzis = Hanzi.objects.filter(heisigBook=heisigBook)
        if heisigFrame != 0 and hanzis.filter(heisigFrame=heisigFrame).exists():
            raise forms.ValidationError(
                'Hanzi with Heisig frame {} in Vol. {} already exists.'.format(
                    heisigFrame,
                    heisigBook,
                    )
                )
        if hanzis.filter(heisigID=heisigID).exists():
            raise forms.ValidationError(
                'Hanzi with HeisigID {} in Vol. {} already exists.'.format(
                    heisigID,
                    heisigBook,
                    )
                )
        return cleaned_data

    def save(self, commit=True):
        instance = super(HanziEditForm, self).save(commit=False)
        if commit:
            instance.save()
            EnglishTerm.objects.create(term=self.cleaned_data['keyword'], hanziCharacter=instance)
            for term in self.cleaned_data['primitive_meanings']:
                EnglishTerm.objects.create(term=term, hanziPrimitive=instance)
            instance.termElements.add(*self.cleaned_data['termElements'])
            LexicalEntry.update_hanzi(instance)
            HanziMeta.update()
        return instance 
