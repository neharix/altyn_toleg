from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    number = models.CharField(max_length=8)
    balance = models.FloatField(default=0)

    REQUIRED_FIELDS = ["number"]


class History(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    card = models.ForeignKey("Card", models.PROTECT)


class Card(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    holder = models.CharField(max_length=250)
    balance = models.IntegerField(default=1000)
    number = models.CharField(max_length=19)
    expiration_date = models.DateField()

    def __str__(self):
        return f"{self.number} {self.holder}"
