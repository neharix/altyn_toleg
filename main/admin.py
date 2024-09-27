from django.contrib import admin

from .models import *


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ["pk", "number", "holder", "balance", "expiration_date"]
