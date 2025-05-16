from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import logout

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Если пользователь не авторизован, просто продолжаем выполнение
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Получаем время последнего запроса с преобразованием из строки в datetime
        last_touch_str = request.session.get('last_touch')
        if last_touch_str:
            last_touch = datetime.fromisoformat(last_touch_str)
            # Проверяем, прошло ли больше 3 часов
            if timezone.now() - last_touch > timedelta(hours=3):
                logout(request)

        # Обновляем метку времени 'last_touch'
        request.session['last_touch'] = timezone.now().isoformat()

        response = self.get_response(request)
        return response
