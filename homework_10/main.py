import requests

class WrongCurrency(Exception):
    def __init__(self, currency):
        self.currency = currency
        super().__init__(f"Incorrect currency input: {self.currency}")

API_KEY = 'HE1HGI5W3NY85L9G'
BASE_URL = 'https://www.alphavantage.co/query'

def get_exchange_rate(from_currency, to_currency):
    params = {
        'function': 'CURRENCY_EXCHANGE_RATE',
        'from_currency': from_currency,
        'to_currency': to_currency,
        'apikey': API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    try:
        rate = data['Realtime Currency Exchange Rate']['5. Exchange Rate']
        return float(rate)
    except KeyError:
        print("Ошибка получения курса:", data)
        return None


class Price:
    # CHF by USD
    CURRENCIES = {
        'UAH': get_exchange_rate('USD', 'UAH'),
        'EURO': get_exchange_rate('USD', 'EUR'),
        'GBP': get_exchange_rate('USD', 'GBP'),
        'USD': get_exchange_rate('UAH', 'USD'),
    }

    def __init__(self, amount: int, currency: str):
        self.amount = amount
        self.currency = currency
        if currency not in Price.CURRENCIES:
            raise WrongCurrency(self.currency)

    def __add__(self, other: 'Price') -> tuple[float, str]:
        if self.currency == other.currency:
            result = self.amount + other.amount
            return result, self.currency
        else:
            return self.chf_convert('add', self.amount, self.currency, other.amount, other.currency)


    def __sub__(self, other: 'Price') -> tuple[float, str]:
        if self.currency == other.currency:
            result = self.amount - other.amount
            return result, self.currency
        else:
            return self.chf_convert('sub', self.amount, self.currency, other.amount, other.currency)

    def chf_convert(self, add_or_sub: str, self_amount: int, self_currency: str, other_amount: int,
                    other_currency: str)  -> (float, str):
        self_chf = self_amount / Price.CURRENCIES[self_currency]
        other_chf = other_amount / Price.CURRENCIES[other_currency]
        if add_or_sub == 'add':
            result = (self_chf + other_chf) * Price.CURRENCIES[self_currency]
            return result, self.currency
        elif add_or_sub == 'sub':
            result = (self_chf - other_chf) * Price.CURRENCIES[self_currency]
            return result, self.currency
        return None


user_currencies = []

count_nums = [i for i in range(1, 1000)]
counter = iter(count_nums)


def new_curr(amount: int, currency: str):
    new_price = Price(int(amount), currency.upper())
    for name, rate in Price.CURRENCIES.items():
        if name == currency:
            user_currencies.append((next(counter), new_price, rate))
            break

def main():
    while True:
        try:
            if len(user_currencies) == 0:
                amount, currency = input("Enter amount and currency you"
                                         " want to convert separated by a space: ").upper().split()
                new_curr(amount, currency)
            else:
                print()
                option = input('Enter 1 if you want to add and convert new currency, '
                               '\nor 2 if you want to add or sub currencies: ')
                if option == '1':
                    amount, currency = input("Enter amount and currency you"
                                             " want to convert separated by a space: ").upper().split()
                    new_curr(amount, currency)
                elif option =='2':
                    if len(user_currencies) >= 2:
                        curr1, operand, curr2 = input("Enter id of the first currency, operand '+' or '-',"
                                                  " and id of second currency separated by space: ").split()
                        if curr1.isnumeric() and curr2.isnumeric():
                            for i in user_currencies:
                                if int(curr1) == i[0]:
                                    curr1_added = i[1]
                                if int(curr2) == i[0]:
                                    curr2_added = i[1]
                            if curr1_added and curr2_added:
                                if operand == '+':
                                    res, curr = curr1_added + curr2_added
                                    print(f"\n{res} {curr}\n")
                                elif operand == '-':
                                    res, curr = curr1_added - curr2_added
                                    print(f"\n{res} {curr}\n")
                                else:
                                    print('Wrong operand')
                            else:
                                print('There are no currencies added with these ids.')
                        else:
                            print('Id entered in wrong format')
                            continue
                    else:
                        print('You have only one added currency!')
                        continue
        except Exception:
            print("Information entered in wrong format!")

        for curr in user_currencies:
            if not curr[1].currency == 'USD':
                print(f"{curr[0]}. {curr[1].amount} {curr[1].currency} |"
                      f" exchange rate of one currency against"
                      f" the dollar: {curr[2]}. Total cost: {curr[1].amount / curr[2]}")
            else:
                print(f"{curr[0]}. {curr[1].amount} {curr[1].currency} |"
                      f" exchange rate of one currency against"
                      f"the hryvnia: {curr[2]}. Total cost: {curr[1].amount / curr[2]}")

if __name__ == "__main__":
    main()