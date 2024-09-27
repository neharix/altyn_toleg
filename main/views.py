import datetime

from django.http import HttpRequest
from django.shortcuts import render

from .containers import CardContainer
from .models import *


def main(request: HttpRequest):
    cards = [CardContainer(card) for card in Card.objects.filter(user=request.user)]
    return render(request, "views/main.html", {"cards": cards})


def add_card(request: HttpRequest):
    if request.method == "POST":
        if (
            request.POST.get("expiration-date", False)
            and request.POST.get("number", False)
            and request.POST.get("cardholder", False)
        ):
            expiration_date = datetime.date(
                int("20" + request.POST["expiration-date"].split("/")[1]),
                int(request.POST["expiration-date"].split("/")[0]),
                1,
            )
            Card.objects.create(
                holder=request.POST["cardholder"],
                number=request.POST["number"],
                expiration_date=expiration_date,
                user=request.user,
            )
    return render(request, "views/add_card.html")


def recharge(request: HttpRequest):
    cards = [CardContainer(card) for card in Card.objects.filter(user=request.user)]
    return render(request, "views/recharge.html", {"cards": cards})


def user_cards(request: HttpRequest):
    cards = [CardContainer(card) for card in Card.objects.filter(user=request.user)]
    return render(request, "views/cards.html", {"cards": cards})
