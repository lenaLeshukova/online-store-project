from django import forms
from catalog.models import ContactMessage
from .models import Product

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш телефон', 'required': True}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ваше сообщение', 'required': True}),
        }

class ProductForm(forms.ModelForm):
    # Список запрещенных слов
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        """Стилизация всех полей под Bootstrap с учетом типа виджета"""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Если поле является чекбоксом, добавляем Bootstrap-класс для чекбоксов
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                # Для всех остальных полей (текст, числа, файлы, выпадающие списки)
                field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        """Валидация названия на запрещенные слова"""
        name = self.cleaned_data.get('name')
        if name:
            name_lower = name.lower()
            for word in self.FORBIDDEN_WORDS:
                if word in name_lower:
                    raise forms.ValidationError(f'Название не может содержать запрещенное слово: "{word}".')
        return name

    def clean_description(self):
        """Валидация описания на запрещенные слова"""
        description = self.cleaned_data.get('description')
        if description:
            description_lower = description.lower()
            for word in self.FORBIDDEN_WORDS:
                if word in description_lower:
                    raise forms.ValidationError(f'Описание не может содержать запрещенное слово: "{word}".')
        return description

    def clean_price(self):
        """Валидация цены на отрицательные значения"""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена продукта не может быть отрицательной.')
        return price
