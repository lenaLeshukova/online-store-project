from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import UpdateView

from users.forms import UserProfileForm
from users.forms import UserRegisterForm, UserLoginForm


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object

        # Критерий: Отправка письма
        try:
            send_mail(
                subject='Добро пожаловать в Skystore!',
                message=f'Вы успешно зарегистрировались. Ваш логин: {user.email}',
                from_email='eir-smart@yandex.ru',
                recipient_list=[user.email],
                fail_silently=False,  # Выбросит ошибку, если SMTP упадет
            )
            messages.success(self.request,
                             'Регистрация успешна! На ваш email отправлено приветственное письмо.')
        except Exception as e:
            # Обрабатываем ошибку отправки почты, чтобы регистрация не падала полностью
            messages.warning(self.request,
                             'Вы зарегистрированы, но не удалось отправить приветственное письмо.')

        return response

    def form_invalid(self, form):
        messages.error(self.request,
                       'Ошибка регистрации. Проверьте введенные данные.')
        return super().form_invalid(form)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('catalog:home')  # Перенаправление после успешного входа

    def form_invalid(self, form):
        # Критерий: Демонстрация ошибок аутентификации пользователю
        messages.error(self.request,
                       'Неверный email или пароль. Пожалуйста, попробуйте снова.')
        return super().form_invalid(form)

class UserLogoutView(LogoutView):
    # В Django 5.0+ LogoutView требует метод POST, перенаправление настроим в форме
    next_page = reverse_lazy('catalog:home')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')  # Перенаправление на эту же страницу после сохранения

    def get_object(self, queryset=None):
        # Метод возвращает текущего вошедшего пользователя для редактирования
        return self.request.user
