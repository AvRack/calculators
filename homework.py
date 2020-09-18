import datetime as dt

DATE_FORMAT = '%d.%m.%Y'


class Record:
    def __init__(self, amount, comment, date = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()

            
class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        now = dt.date.today()
        stats = sum ([record.amount for record in self.records if now == record.date])
        return stats
        
    def get_week_stats(self):
        now = dt.date.today()
        week_stats = sum([record.amount for record in self.records if now - dt.timedelta(days=7) <= record.date <= now])
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        rest = self.limit - self.get_today_stats()
        if rest > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {rest} кКал'
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 74.89
    EURO_RATE = 88.68

    def get_today_cash_remained(self, currency):
        cash = self.limit - self.get_today_stats()
        if cash == 0:
            return 'Денег нет, держись'
        currency = self.get_currency(currency)
        cash = round(cash / currency['value'], 2)
        if cash > 0:
            return f"На сегодня осталось {cash} {currency['short_name']}"
        return f"Денег нет, держись: твой долг - {abs(cash)} {currency['short_name']}"
    
    def get_currency(self, currency):
        currencies = {
            'rub': {
                'short_name':'руб',
                'value': 1
            },
            'eur': {
                'short_name': 'Euro',
                'value': self.EURO_RATE
            },
            'usd': {
                'short_name': 'USD',
                'value': self.USD_RATE
            }  
        }
        currency = currencies.get(currency)
        return currency