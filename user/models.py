from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.name


class User(models.Model):
    ROLES = [
        ("member", "Пользователь"),
        ("moderator", "Модератор"),
        ("admin", "Админ"),
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLES, default="member")
    age = models.PositiveIntegerField()
    location_id = models.CharField(max_length=50)
    added_by_user = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
