import datetime as dt


class Calculator:
    """
    Класс калькулятора, от которого наследуются класс калькулятора денег,
    а также класс калькулятора каллорий.
    Является шаблоном, поэтому в нем определены общие методы, как:
    add_record(), get_today_stats(), get_week_stats()
    """
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, other):
        self.records.append(other)

    def get_today_stats(self):
        self.today_value = 0
        for record in self.records:
            if record.date == dt.datetime.now().date():
                self.today_value += record.amount
        return self.today_value

    def get_week_stats(self):
        """
        days=7
        weeks=1
        """
        self.week_value = 0
        for record in self.records:
            timedelta = dt.datetime.now().date() - record.date
            if (timedelta < dt.timedelta(weeks=1)
                    and record.date <= dt.datetime.now().date()):
                self.week_value += record.amount
        return self.week_value


class Record:
    """
    Шаблон записей о расходах или о полученных каллориях
    """
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y')
        else:
            self.date = dt.datetime.now()
        self.date = self.date.date()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        self.today_calories_remained = self.limit - self.get_today_stats()
        if self.today_calories_remained > 0:
            self.remained_value_message = (
                "Сегодня можно съесть "
                "что-нибудь ещё, но с общей калорийностью не более "
                f"{str(self.today_calories_remained)} кКал")
            return self.remained_value_message
        else:
            self.remained_value_message = "Хватит есть!"
            return self.remained_value_message


class CashCalculator(Calculator):
    USD_RATE = 72.0
    EURO_RATE = 88.0

    def get_today_cash_remained(self, currency):
        self.today_cash_value = self.get_today_stats()
        if self.today_cash_value < self.limit:
            self.remained_value_message = "На сегодня осталось "
            self.remained_cash = self.limit - self.today_cash_value
        elif self.today_cash_value == self.limit:
            self.remained_value_message = "Денег нет, держись"
        else:
            self.remained_value_message = "Денег нет, держись: твой долг - "
            self.remained_cash = self.today_cash_value - self.limit
        if currency == 'rub' and self.today_cash_value != self.limit:
            self.remained_value_message += f"{self.remained_cash} руб"
        elif currency == 'usd' and self.today_cash_value != self.limit:
            self.remained_cash_usd = self.remained_cash / self.USD_RATE
            self.remained_value_message += f"{self.remained_cash_usd:.2f} USD"
        elif currency == "eur" and self.today_cash_value != self.limit:
            self.remained_cash_euro = self.remained_cash / self.EURO_RATE
            self.remained_value_message += (
                f"{self.remained_cash_euro:.2f} Euro")
        return self.remained_value_message


cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,git add .
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=1000, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='04.06.2021'))
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар',
                                  date='30.05.2021'))
print(cash_calculator.get_week_stats())
for record in cash_calculator.records:
    print(f"{record.date}")
