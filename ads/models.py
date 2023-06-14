from user.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Ad(models.Model):
    STATUS_CHOICES = [
        (True, 'Опубликовано'),
        (False, 'Не опубликовано')
    ]
    name = models.CharField(max_length=100)
    author_id = models.IntegerField()
    price = models.SmallIntegerField()
    description = models.CharField(max_length=2000)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')
    category_id = models.IntegerField()

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name