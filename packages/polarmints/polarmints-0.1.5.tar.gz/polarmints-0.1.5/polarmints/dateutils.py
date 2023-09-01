import pandas_market_calendars as mcal
import numpy as np
import polars as pl
from datetime import date


def busday_offset(dates: pl.Series, offsets, cal_name: str = None, **kwargs) -> pl.Series:
    if cal_name:
        kwargs['holidays'] = mcal.get_calendar(cal_name).holidays().holidays
    kwargs['roll'] = kwargs.get('roll', 'forward')
    res = np.busday_offset(dates, offsets, **kwargs)
    return pl.from_numpy(res)

