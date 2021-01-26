from django import forms

class UrlForm(forms.Form):
	url = forms.URLField(label = 'Input your URL')
	price = forms.IntegerField(label = 'Input your wanted price')