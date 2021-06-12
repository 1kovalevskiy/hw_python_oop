import datetime as dt
from typing import Union


class Calculator:
    def __init__(self, limit: Union[int, float]) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, other) -> None:
        self.records.append(other)

    def check_limit(self) -> Union[int, float]:
        return self.limit - self.get_today_stats()

    def get_today_stats(self) -> Union[int, float]:
        return sum([record.amount for record in self.records
                    if record.date == dt.date.today()])

    def check_timedelta_is_week(self, date, week_ago) -> bool:
        if (date > week_ago and date <= dt.date.today()):
            return True
        return False

    def get_week_stats(self) -> Union[int, float]:
        week_ago = dt.date.today() - dt.timedelta(weeks=1)
        return sum([record.amount for record in self.records
                    if self.check_timedelta_is_week(record.date, week_ago)])


class Record:
    """
    Record template of purchase or meal.
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
    """
    Calories calculator checks today's and week's calories intake,
    and today calories limit.
    """
    def get_calories_remained(self) -> str:
        """
        Method returns message about remained calories.
        """
        self.today_calories_remained = self.check_limit()
        if self.today_calories_remained > 0:
            return (
                "Сегодня можно съесть "
                "что-нибудь ещё, но с общей калорийностью не более "
                f"{str(self.today_calories_remained)} кКал")
        return "Хватит есть!"


class CashCalculator(Calculator):
    """
    Cash calculator checks daily spending, week spending,
    and today ballance limit.
    """
    USD_RATE: float = 72.0
    EURO_RATE: float = 88.0
    POUND_RATE: float = 100.0

    def get_today_cash_remained(self, currency: str) -> str:
        """
        Method returns message about remained spending.
        """
        cash_now = {"rub": (self.check_limit(), "руб")}
        if cash_now["rub"][0] == 0:
            return "Денег нет, держись"
        cash_now["usd"] = (cash_now["rub"][0] / self.USD_RATE, "USD")
        cash_now["eur"] = (cash_now["rub"][0] / self.EURO_RATE, "Euro")
        cash_now["gbp"] = (cash_now["rub"][0] / self.POUND_RATE, "Pound")

        try:
            money_value, money_currency = cash_now[currency]
        except Exception:
            raise ValueError("Такой валюты не существует")
        if money_value > 0:
            return f"На сегодня осталось {money_value:.2f} {money_currency}"
        else:
            return (f"Денег нет, держись: твой долг - {-money_value:.2f} "
                    f"{money_currency}")


if __name__ == '__main__':
    cash_calculator = CashCalculator(2000)
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    cash_calculator.add_record(Record(amount=860, comment='Серёге за обед'))
    cash_calculator.add_record(Record(amount=3000,
                                      comment='бар в Танин др',
                                      date='04.06.2021'))
    cash_calculator.add_record(Record(amount=3000,
                                      comment='суши-бар',
                                      date='30.05.2021'))
    print(cash_calculator.get_today_cash_remained("gbp"))
    for record in cash_calculator.records:
        print(f"{record.date}")
