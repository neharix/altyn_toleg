import datetime
import random

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import redirect, render

from . import utils
from .containers import CardContainer, HistoryContainer
from .models import *


def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            email = request.POST.get("email")
            number = request.POST.get("number")
            try:
                user = User.objects.get(email=email, number=number)
                print("user found")
                login(request, user)
                print("success")
            except:
                password = utils.generate_password()
                user = User.objects.create(
                    email=email,
                    username=f"user{number}",
                    number=number,
                    password_for_usage=password,
                    password=password,
                )
                login(request, user)
                print("user created")
            return redirect("home")
        return render(request, "views/login.html")


@login_required(login_url="/login/")
def logout_view(request: HttpRequest):
    logout(request)
    return redirect("login")


@login_required(login_url="/login/")
def main(request: HttpRequest):
    cards = [CardContainer(card) for card in Card.objects.filter(user=request.user)]
    histories = [
        HistoryContainer(history)
        for history in History.objects.filter(user=request.user).order_by(
            "-payment_time"
        )[:5]
    ]
    return render(request, "views/main.html", {"cards": cards, "histories": histories})


@login_required(login_url="/login/")
def user_history(request: HttpRequest):
    histories = [
        HistoryContainer(history)
        for history in History.objects.filter(user=request.user).order_by(
            "-payment_time"
        )
    ]
    return render(request, "views/history.html", {"histories": histories})


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def recharge(request: HttpRequest):
    cards = [CardContainer(card) for card in Card.objects.filter(user=request.user)]
    return render(request, "views/recharge.html", {"cards": cards})


@login_required(login_url="/login/")
def user_cards(request: HttpRequest):
    cards = [CardContainer(card) for card in Card.objects.filter(user=request.user)]
    return render(request, "views/cards.html", {"cards": cards})


@login_required(login_url="/login/")
def confirm_payment(request: HttpRequest, card_pk: int, value: int):
    history = History.objects.create(
        user=request.user, amount=value, card=Card.objects.get(pk=card_pk)
    )
    confirmation_code = random.randint(11111, 99999)
    send_mail(
        "Altyn Töleg tassyklama kody",
        f"Tölegi ýerine ýetirmek üçin tassyklama kodyňyz: {confirmation_code}",
        "altyntoleg@gmail.com",
        [request.user.email],
    )
    return render(
        request,
        "views/confirm_payment.html",
        {
            "confirmation_code": confirmation_code,
            "history_pk": history.pk,
        },
    )


@login_required(login_url="/login/")
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
