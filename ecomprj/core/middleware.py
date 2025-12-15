from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
import datetime


class CacheStatsMiddleware(MiddlewareMixin):
    """
    Middleware для отслеживания статистики использования кеша.
    Увеличивает счетчик каждый раз когда обрабатывается запрос.
    """

    def process_request(self, request):
        try:
            # Увеличиваем счетчик запросов в Redis
            today = datetime.date.today().isoformat()
            cache_key = f"requests_count_{today}"

            count = cache.get(cache_key, 0)
            cache.set(cache_key, count + 1, 60 * 60 * 24)  # Храним 24 часа

            # Сохраняем информацию о последнем посещении
            cache.set("last_request_time", datetime.datetime.now().isoformat(), 60 * 60)
        except Exception:
            # Игнорируем ошибки кеша, чтобы не ломать сайт
            pass

        return None

    def process_response(self, request, response):
        try:
            # Можем добавить информацию о кеше в headers для отладки
            if hasattr(request, "user") and request.user.is_authenticated:
                session_key = f"user_session_{request.user.id}"
                cache.set(session_key, True, 60 * 30)  # 30 минут
        except Exception:
            # Игнорируем ошибки кеша
            pass

        return response
