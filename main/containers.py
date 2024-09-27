from .models import Card, History


class CardContainer:
    def __init__(self, card: Card):
        self.pk = card.pk
        self.holder = (
            card.holder.split()[0].capitalize()
            + " "
            + card.holder.split()[1].capitalize()
        )
        self.number = card.number.split()[3]
        self.expiration_date = card.expiration_date.strftime("%m/%y")


class HistoryContainer:
    def __init__(self, history: History):
        self.pk = history.pk
        self.amount = history.amount
        self.payment_time = history.payment_time.strftime("%d.%m.%Y %H:%M")
        self.status = history.status
