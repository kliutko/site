from .models import ViewCount
from modules.services.utils import get_client_ip
from datetime import timedelta
from django.utils import timezone


class ViewCountReklamaMixin:
    """
    Миксин для увеличения счетчика просмотров рекламы
    """
    def get_object(self):
        # получаем статью из метода родительского класса
        obj = super().get_object()
        # получаем IP-адрес пользователя
        ip_address = get_client_ip(self.request)
        # получаем текущую дату и время
        now = timezone.now()
        # вычитаем 7 дней из текущей даты
        week_ago = now - timedelta(days=1)
        # проверяем, есть ли записи за последние 7 дней для данного пользователя и данной статьи
        # если нет, то создаем новую запись
        ViewCount.objects.get_or_create(article=obj, ip_address=ip_address, viewed_on__gte=week_ago)

        # получаем или создаем запись о просмотре статьи для данного пользователя
        # ViewCount.objects.get_or_create(article=obj, ip_address=ip_address)
        return obj