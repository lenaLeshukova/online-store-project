from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import User

class UserRegisterForm(UserCreationForm):
    # Явное поле подтверждения пароля для кастомной валидации по критериям
    password_confirm = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'})
    )

    class Meta:
        model = User
        fields = ['email', 'avatar', 'phone', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Автоматическая стилизация всех полей под Bootstrap
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'

    def clean_password_confirm(self):
        """Проверка совпадения двух паролей"""
        password = self.cleaned_data.get("password_1")  # Внутреннее имя поля в UserCreationForm
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают!")
        return password_confirm


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

