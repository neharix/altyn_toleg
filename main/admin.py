from django.contrib import admin

from .models import *


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ["pk", "number", "holder", "balance", "expiration_date"]


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ["pk", "amount", "card", "status", "payment_time", "user"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["pk", "number", "balance", "username"]
