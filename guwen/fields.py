from django import forms

class StringListField(forms.CharField):
	def __init__(self, *args, **kwargs):
		self.widget = forms.Textarea(attrs={'rows':3})
		super(StringListField, self).__init__(*args, **kwargs)

	def to_python(self, value):
		return [v for v in map(lambda x: x.strip(), value.split('\n')) if v != '']
