import datetime as dt

date_format = '%d.%m.%Y'


class Record:
    def __init__(self, amount, comment, date = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            date = dt.datetime.strptime(date, date_format)
            self.date = dt.date(date.year, date.month, date.day)

            
class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        stats = 0
        now = dt.date.today()
        for record in self.records:
            if now.day == record.date.day and now.month == record.date.month and now.year == record.date.year:
                stats += record.amount
        return stats
        
    def get_week_stats(self):
        week_stats = 0
        for record in self.records:
            if record.date >= dt.date.today() - dt.timedelta(days=7) and record.date <= dt.date.today():
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        Calculator.__init__(self, limit)

    def get_calories_remained(self):
        rest = self.limit - self.get_today_stats()
        if rest > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {rest} кКал')
        else:
            return ('Хватит есть!')
        return rest


class CashCalculator(Calculator):
    USD_RATE = 74.89
    EURO_RATE = 88.68
    def __init__(self, limit):
        Calculator.__init__(self, limit)

    def get_today_cash_remained(self, currency):
        cash = self.limit - self.get_today_stats()
        currency = self.get_currency(currency)
        cash = round(cash / currency['value'], 2)
        #cash = cash.round_cash()
        if cash > 0:
            return(f"На сегодня осталось {cash} {currency['short_name']}")
        elif cash == 0:
            return('Денег нет, держись')
        else:
            return(f"Денег нет, держись: твой долг - {abs(cash)} {currency['short_name']}")
    
    def get_currency(self, currency):
        currencies = {
            'rub': {
                'short_name':'руб',
                'value': 1
            },
            'eur': {
                'short_name': 'Euro',
                'value': CashCalculator.EURO_RATE
            },
            'usd': {
                'short_name': 'USD',
                'value': CashCalculator.USD_RATE
            }  
        }
        currency = currencies.get(currency)
        return currency


cash_calculator = CashCalculator(1000)
calories_calculator = CaloriesCalculator(1500)
r1 = Record(amount=200, comment='1')
r2 = Record(amount=300, comment='2')
r3 = Record(amount=500, comment='23123123', date='09.09.2020')
r4 = Record(amount=200, comment='1')
r5 = Record(amount=300, comment='2')
r6 = Record(amount=500, comment='23123123', date='09.09.2020')
calories_calculator.add_record(r1)
calories_calculator.add_record(r2)
calories_calculator.add_record(r3)
cash_calculator.add_record(r4)
cash_calculator.add_record(r5)
cash_calculator.add_record(r6)
print(cash_calculator.get_today_stats())
print(calories_calculator.get_week_stats())
print(calories_calculator.get_calories_remained())
print(cash_calculator.get_today_cash_remained('rub'))