import datetime
import typing


class DatetimeModule:
    TZD = "03:00"
    """Moscow city default timezone"""

    DATETIME_FMT = "%Y-%m-%dT%H:%M:%S+{}"
    """Qiwi API datetime format"""

    @property
    def datetime_fmt(self):
        """Get datetime format string with qiwi TZD"""
        return self.DATETIME_FMT.format(self.TZD)

    def parse_date_string(self, dt: str) -> datetime.datetime:
        """Get datetime with qiwi TZD format from string"""
        return datetime.datetime.strptime(dt, self.datetime_fmt)

    def parse_datetime(self, dt: datetime.datetime):
        return dt.strftime(self.datetime_fmt)

    def check_and_parse_datetime(
        self, dt: typing.Optional[typing.Union[str, datetime.datetime]]
    ) -> typing.Optional[str]:
        return (
            dt
            if isinstance(dt, str)
            else self.parse_datetime(dt)
            if isinstance(dt, datetime.datetime)
            else None
        )
