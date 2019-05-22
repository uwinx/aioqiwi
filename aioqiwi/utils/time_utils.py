import datetime


class EasyDate:
    def __init__(self, date: datetime.datetime = None, tzd="03:00"):
        self.__fmt = f"%Y-%m-%dT%H:%M:%S+{tzd}"
        self.__date = date or datetime.datetime.now()

    def go_back(self, days: int):
        return EasyDate(self.__date - datetime.timedelta(days=days))

    def go_ahead(self, days: int):
        return EasyDate(self.__date + datetime.timedelta(days=days))

    def update(self, date=None):
        self.__date = date or datetime.datetime.now()

    @property
    def today(self):
        return self.__date.strftime(self.__fmt)

    @property
    def datetime(self):
        return self.__date

    def strftime(self, new_format):
        self.__fmt = new_format
        return self.today

    def __repr__(self):
        return self.today

    def __gt__(self, other):
        if isinstance(other, EasyDate):
            return self.datetime > other.datetime
        elif not isinstance(other, datetime.datetime):
            return self.datetime > other

    def __ge__(self, other):
        if isinstance(other, EasyDate):
            return self.datetime >= other.datetime
        elif not isinstance(other, datetime.datetime):
            return self.datetime >= other

    def __lt__(self, other):
        if isinstance(other, EasyDate):
            return self.datetime < other.datetime
        elif not isinstance(other, datetime.datetime):
            return self.datetime < other

    def __le__(self, other):
        if isinstance(other, EasyDate):
            return self.datetime <= other.datetime
        elif not isinstance(other, datetime.datetime):
            return self.datetime <= other

    def __str__(self):
        return self.today


class TimeRange:
    def __init__(self, start, stop=None):
        if stop is None and isinstance(start, (datetime.datetime, int, EasyDate)):
            if isinstance(start, int):
                self.to_date = EasyDate(
                    datetime.datetime.now() + datetime.timedelta(days=start)
                )
            else:
                self.to_date = start
            self.from_date = EasyDate()

            if self.from_date > self.to_date:
                self.from_date, self.to_date = self.to_date, self.from_date

        elif isinstance(start, (datetime.datetime, EasyDate)) and isinstance(
            stop, (datetime.datetime, EasyDate)
        ):
            self.from_date = EasyDate(start)
            self.to_date = EasyDate(stop)
        else:
            raise ValueError("Arguments for start and stop must be datetime.datetime")

    @property
    def dates(self):
        return self.from_date, self.to_date
