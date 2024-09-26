from django.urls import path

from .views import *

urlpatterns = [
    path("", main, name="home"),
    path("add_card/", add_card, name="add_card"),
    path("recharge/", recharge, name="recharge"),
]
