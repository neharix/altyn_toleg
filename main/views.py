import datetime
import random

from django.http import HttpRequest
from django.shortcuts import redirect, render

from .containers import CardContainer, HistoryContainer
from .models import *


def main(request: HttpRequest):
    cards = [CardContainer(card) for card in Card.objects.filter(user=request.user)]
    histories = [
        HistoryContainer(history)
        for history in History.objects.filter(user=request.user).order_by(
            "-payment_time"
        )[:5]
    ]
    return render(request, "views/main.html", {"cards": cards, "histories": histories})


def user_history(request: HttpRequest):
    histories = [
        HistoryContainer(history)
        for history in History.objects.filter(user=request.user).order_by(
            "-payment_time"
        )
    ]
    return render(request, "views/history.html", {"histories": histories})


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


def confirm_payment(request: HttpRequest, card_pk: int, value: int):
    history = History.objects.create(
        user=request.user, amount=value, card=Card.objects.get(pk=card_pk)
    )
    return render(
        request,
        "views/confirm_payment.html",
        {
            "confirmation_code": random.randint(11111, 99999),
            "history_pk": history.pk,
        },
    )


def success(request: HttpRequest, card_pk: int, value: int, history_pk: int):
    card = Card.objects.get(pk=card_pk)
    request.user.balance += value
    request.user.save()
    card.balance -= value
    card.save()
    history = History.objects.get(pk=history_pk)
    history.status = True
    history.save()
    return redirect("history")
