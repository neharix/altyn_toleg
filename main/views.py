from django.http import HttpRequest
from django.shortcuts import render


def main(request: HttpRequest):
    return render(request, "views/main.html")


def add_card(request: HttpRequest):
    if request.method == "POST":
        print(request.POST["expiration-date"])
        print(request.POST["number"])
        print(request.POST["cardholder"])
    return render(request, "views/add_card.html")
