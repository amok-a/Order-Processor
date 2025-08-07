from django.db import models


class Customer(models.Model):
    """Модель заказчика/подписчика."""

    telegram_id = models.BigIntegerField(unique=True)