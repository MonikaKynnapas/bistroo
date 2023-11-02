import django.forms
from django import forms
import bistroo.settings
from .models import *


class MenuCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['name'].widget = forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control mb-2'})
        self.fields['date'].label = 'Kuupäev'
        self.fields['theme'].label = 'Teema'
        self.fields['recommends'].label = 'Soovitab'
        self.fields['prepared'].label = 'Valmistas'

    class Meta:
        model = Menu
        widgets = {
            'date': django.forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'theme': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'recommends': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'prepared': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        }
        fields = ('date', 'theme', 'recommends', 'prepared')
