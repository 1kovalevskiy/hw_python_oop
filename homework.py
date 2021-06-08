import datetime as dt
from typing import Union


class Calculator:
    """
    Класс калькулятора, от которого наследуются класс калькулятора денег,
    а также класс калькулятора каллорий.
    Является шаблоном, поэтому в нем определены общие методы, как:
    add_record(), get_today_stats(), get_week_stats().
    """
    def __init__(self, limit: Union[int, float]) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, other) -> None:
        self.records.append(other)

    def check_limit(self) -> Union[int, float]:
        return self.limit - self.get_today_stats()

    def get_today_stats(self) -> Union[int, float]:
        self.today_value = 0
        self.today_value = sum([record.amount for record in self.records
                                if record.date == dt.datetime.now().date()])
        return self.today_value

    def check_timedelta_is_week(self, date) -> bool:
        if (dt.date.today() - date < dt.timedelta(weeks=1)
                and date <= dt.date.today()):
            return True
        return False

    def get_week_stats(self) -> Union[int, float]:
        self.week_value = 0
        self.week_value = sum([record.amount for record in self.records
                               if self.check_timedelta_is_week(record.date)])
        return self.week_value


class Record:
    """
    Шаблон записей о расходах или о полученных каллориях.
    """
    def __init__(self, amount: Union[int, float],
                 comment: str,
                 date=None) -> None:
        self.amount = amount
        self.comment = comment
        if date:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.date.today()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        self.today_calories_remained = self.check_limit()
        if self.today_calories_remained > 0:
            return (
                "Сегодня можно съесть "
                "что-нибудь ещё, но с общей калорийностью не более "
                f"{str(self.today_calories_remained)} кКал")
        return "Хватит есть!"


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


if __name__ == '__main__':
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
