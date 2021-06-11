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
    Record template of purchase of meal.
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

    def get_today_cash_remained(self, currency: str) -> str:
        """
        Method returns message about remained spending.
        """
        self.cash_now = {"rub": self.check_limit()}
        if self.cash_now["rub"] == 0:
            return "Денег нет, держись"
        self.cash_now["usd"] = self.cash_now["rub"] / self.USD_RATE
        self.cash_now["eur"] = self.cash_now["rub"] / self.EURO_RATE
        if self.cash_now["rub"] > 0:
            self.cash_now["message"] = (
                "На сегодня осталось ")
            self.cash_now["money"] = self.cash_now[currency]
        else:
            self.cash_now["message"] = (
                "Денег нет, держись: твой долг - ")
            self.cash_now["money"] = -self.cash_now[currency]

        if currency == "rub":
            self.cash_now["currency"] = " руб"
        elif currency == "usd":
            self.cash_now["currency"] = " USD"
        elif currency == "eur":
            self.cash_now["currency"] = " Euro"

        return (f'{self.cash_now["message"]}'
                f'{self.cash_now["money"]:.2f}'
                f'{self.cash_now["currency"]}')


if __name__ == '__main__':
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    cash_calculator.add_record(Record(amount=860, comment='Серёге за обед'))
    cash_calculator.add_record(Record(amount=3000,
                                      comment='бар в Танин др',
                                      date='04.06.2021'))
    cash_calculator.add_record(Record(amount=3000,
                                      comment='бар',
                                      date='30.05.2021'))
    print(cash_calculator.get_today_cash_remained("eur"))
    for record in cash_calculator.records:
        print(f"{record.date}")
