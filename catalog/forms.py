from django.forms import ModelForm, BooleanField, forms

from catalog.models import Product, Version


class StyleFormMixin:
    """Миксин для формы товара"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):
    """Форма для создания товара"""
    banned_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ('name', 'category', 'description', 'image', 'price', 'is_active')
        # exclude = ('created_at', 'updated_at', 'viewed', 'slug', 'owner')
        # fields = '__all__'

    def clean_name(self):
        """Проверка на наличие запрещенных слов"""
        clean_name = self.cleaned_data['name']
        for word in self.banned_words:
            if word in clean_name.lower():
                raise forms.ValidationError(f'Нельзя использовать слово "{word}"')
        return clean_name

    def clean_description(self):
        """Проверка на наличие запрещенных слов"""
        clean_description = self.cleaned_data['description']
        for word in self.banned_words:
            if word in clean_description.lower():
                raise forms.ValidationError(f'Нельзя использовать слово "{word}"')
        return clean_description


class VersionForm(StyleFormMixin, ModelForm):
    """Форма для создания версии товара"""
    class Meta:
        model = Version
        fields = '__all__'
