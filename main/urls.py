from django.urls import path

from .views import *

urlpatterns = [
    path("", main, name="home"),
    path("add_card/", add_card, name="add_card"),
    path("recharge/", recharge, name="recharge"),
    path("history/", user_history, name="history"),
    path(
        "recharge/card/<int:card_pk>/value/<int:value>/",
        confirm_payment,
    ),
    path(
        "recharge/card/<int:card_pk>/value/<int:value>/success/<int:history_pk>/",
        success,
    ),
]
