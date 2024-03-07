from django.forms import TextInput
from django.forms.models import inlineformset_factory
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
        fields = ('date', 'theme', 'recommends', 'prepared')

        widgets = {
            # 'date': django.forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date': django.forms.DateInput(attrs={'type': 'text', 'id': 'date', 'class': 'form-control', 'placeholder': 'Vali kuupäev', 'readonly': 'readonly'}, format='%d.%m.%Y'),
            'theme': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Kui lisad teema, pead lisama ka soovitaja'}),
            'recommends': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Kui lisad soovitaja, pead lisama ka teema'}),
            'prepared': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'plaCeholder': 'Valmistaja lisamine on vabatahtlik'}),
        }

    def clean(self):
        super(MenuCreateForm, self).clean()

        theme = self.cleaned_data['theme']
        recommends = self.cleaned_data['recommends']
        if(theme is None and recommends is not None) or (theme is not None and recommends is None):
            self.add_error('theme', ValidationError('Teemapäev ja soovitaja peavad mõlemad olema täidetud, mitte üks kahest.'))

        return self.cleaned_data

class FoodMenuUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FoodMenuUpdateForm, self).__init__(*args, **kwargs)

        # self.fields['name'].widget = forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control mb-2'})
        self.fields['food'].label = 'Toit'
        self.fields['full_price'].label = 'Täis hind'
        self.fields['half_price'].label = 'Pool hinda'
        self.fields['show_in_menu'].label = 'Näita menüüs'
        # self.fields['DELETE'].label = 'Kustuta'

    class Meta:
        model = FoodItem
        fields = ['food', 'full_price', 'half_price', 'show_in_menu']
        widgets = {
            'food': django.forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'full_price': django.forms.TextInput(attrs={'type': 'number', 'class': 'form-control', 'step': 0.01}),
            'half_price': django.forms.TextInput(attrs={'type': 'number', 'class': 'form-control', 'step': 0.01}),
            'show_in_menu': django.forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # 'DELETE': django.forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FoodMenuCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FoodMenuCreateForm, self).__init__(*args, **kwargs)

        self.fields['date'].label = 'Kuupäev'
        self.fields['category'].label = 'Kategooria'

    class Meta:
        model = FoodMenu
        fields = ['date', 'category']
        widgets = {
            'date': django.forms.Select(attrs={'type': 'date', 'class': 'form-control mb-2 form-select'}),
            'category': django.forms.Select(attrs={'class': 'form-control form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        category = cleaned_data.get('category')

        if FoodMenu.objects.filter(date=date, category=category).exists():
            raise ValidationError(
                f"Uut '{category}' kategooriat ei saa sellele kuupäevale sisestada, kuna see on juba olemas.")

        return cleaned_data


FoodMenuFormset = inlineformset_factory(
    FoodMenu,
    FoodItem,
    form=FoodMenuUpdateForm,
    extra=3,
    fields=('food', 'full_price', 'half_price', 'show_in_menu',))


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['number'].label = 'Number'
        self.fields['name'].label = 'Nimi'
    class Meta:
        model = Category
        fields = ['number', 'name']
        widgets = {
            'number': forms.TextInput(attrs={'type': 'text', 'class': 'form-control mb-2'}),
            'name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        }