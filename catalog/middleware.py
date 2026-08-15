from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Список разрешенных имен URL для анонимов
        open_url_names = [
            'catalog:home',
            'users:login',
            'users:register',
        ]

        # Разрешаем системные пути (админка, статика, медиа) без авторизации
        if request.path.startswith('/admin/') or request.path.startswith(
                '/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            # Получаем имена текущего URL, безопасно проверяя совпадения
            try:
                from django.urls import resolve
                current_url_name = f"{resolve(request.path).app_name}:{resolve(request.path).url_name}"
            except Exception:
                current_url_name = None

            # Если страница не входит в список разрешенных — отправляем на авторизацию
            if current_url_name not in open_url_names:
                return redirect('users:login')

        return self.get_response(request)
