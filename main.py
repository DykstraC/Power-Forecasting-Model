import time
import datetime as dt
import calendar
#import tk

class PowerError(Exception):
    def __init__(self, msg, obj=None):
        if obj is None:
            self.msg = msg
        else:
            self.msg = obj.__class__.__name__ + ':: ' + msg

    def __str__(self):
        return repr(self.msg)

def get_period(stime, etime):
    # Convert start_time arg to time of day slot
    start_period = stime.hour * 2 + 1
    if 0 < stime.minute:
        start_period_modifier = 1
    else:
        start_period_modifier = 0

    temp_start_period = start_period + start_period_modifier
    start_period = temp_start_period - 1

    if stime.hour == 0:
        start_period = 48


    # Convert end_time arg to time of day slot
    end_period = etime.hour * 2 + 1
    if 0 < etime.minute:
        end_period_modifier = 1
    else:
        end_period_modifier = 0

    temp_end_period = end_period + end_period_modifier
    end_period = temp_end_period - 1

    if etime.hour == 0:
        end_period = 48

    print(start_period, '\n', end_period)

    return start_period, end_period


def get_dateDiff(sdate, edate, start_period, end_period):
    days_between = edate - sdate
    periods_between = (days_between*48) - start_period - (48 - end_period)

    return periods_between





def get_datetime():
    start_year = int(input("Input Start Year: "))
    start_month = int(input("Input Start Month: "))
    start_day = int(input("Input Start Day: "))
    end_year = int(input("Input End Year: "))
    end_month = int(input("Input End Month: "))
    end_day = int(input("Input End Day: "))
    start_time = int(input("Input Start Time (24hr format e.g. 2300): "))
    end_time = int(input("Input End Time (24hr format e.g. 2300): "))

    start_date = dt.datetime(start_year, start_month, start_day)
    end_date = dt.datetime(end_year, end_month, end_day)

    print(end_date-start_date)

def subroutine_list():
    get_period(start_time, end_time, speriod, eperiod)
    get_dateDiff(start_date, end_date, speriod, eperiod, forecast_periods)
    
