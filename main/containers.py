from .models import Card


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
