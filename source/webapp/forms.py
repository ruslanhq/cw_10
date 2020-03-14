from django import forms

from webapp.models import File


class SearchForm(forms.Form):
    form = forms.CharField(max_length=40, label='Form', required=False)


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        exclude = ['created_at', 'author']
