class WrongCurrency(Exception):
    def __init__(self, currency):
        self.currency = currency
        super().__init__(f"Incorrect currency input: {self.currency}")


class Price:
    # CHF by USD
    CURRENCIES = {
        'UAH': 41.5,
        'EURO': 1.11,
        'GBP': 1.32,
        'USD': 1,
    }

    def __init__(self, amount: int, currency: str):
        self.amount = amount
        self.currency = currency
        if not currency in Price.CURRENCIES:
            raise WrongCurrency(self.currency)


    def __add__(self, other):
        if self.currency == other.currency:
            result = self.amount + other.amount
            return print(f"{result} {self.currency}")
        else:
            self.chf_convert('add', self.amount, self.currency, other.amount, other.currency)

    def __sub__(self, other):
        if self.currency == other.currency:
            result = self.amount - other.amount
            return print(f"{result} {self.currency}")
        else:
            self.chf_convert('sub', self.amount, self.currency, other.amount, other.currency)

    def chf_convert(self, add_or_sub, self_amount, self_currency, other_amount, other_currency):
        self_chf = self_amount / Price.CURRENCIES[self_currency]
        other_chf = other_amount / Price.CURRENCIES[other_currency]
        if add_or_sub == 'add':
            result = (self_chf + other_chf) * Price.CURRENCIES[self_currency]
            return print(f"{result} {self.currency}")
        elif add_or_sub == 'sub':
            result = (self_chf - other_chf) * Price.CURRENCIES[self_currency]
            return print(f"{result} {self.currency}")
        return None

