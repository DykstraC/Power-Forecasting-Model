import datetime as dt
import calendar
import numpy as np
import matplotlib
import sys
import os


class PowerError(Exception):
    def __init__(self, msg, obj=None):
        if obj is None:
            self.msg = msg
        else:
            self.msg = obj.__class__.__name__ + ':: ' + msg

    def __str__(self):
        return repr(self.msg)


def get_period(stime, etime):
    global start_period
    global end_period
    # Convert start_time arg to time of day slot
    start_period = int(str(stime)[:2]) * 2 + 1
    if 0 < int(str(stime)[-2:]):
        start_period_modifier = 1
    else:
        start_period_modifier = 0

    temp_start_period = start_period + start_period_modifier
    start_period = temp_start_period - 1

    if int(str(stime)[:2]) == 0:
         start_period = 48


    # Convert end_time arg to time of day slot
    end_period = int(str(etime)[:2]) * 2 + 1
    if 0 < int(str(etime)[-2:]):
        end_period_modifier = 1
    else:
        end_period_modifier = 0

    temp_end_period = end_period + end_period_modifier
    end_period = temp_end_period - 1

    if int(str(etime)[:2]) == 0:
        end_period = 48

    print(start_period, '\n', end_period)

    return start_period, end_period


def get_dateDiff(sdate, edate, start_period, end_period):
    global periods_between
    temp_days_between = edate - sdate
    print(temp_days_between.days)
    days_between = temp_days_between.days
    temp_start_period = int(start_period)
    temp_end_period = int(end_period)
    periods_between = (days_between*48) - temp_start_period - ( -(-48 + temp_end_period))

    return periods_between





def get_datetime(start_year, start_month, start_day, end_year, end_month, end_day, start_time, end_time):
    #start_year = int(input("Input Start Year: "))
    #start_month = int(input("Input Start Month: "))
    #start_day = int(input("Input Start Day: "))
    #end_year = int(input("Input End Year: "))
    #end_month = int(input("Input End Month: "))
    #end_day = int(input("Input End Day: "))
    #start_time = int(input("Input Start Time (24hr format e.g. 2300): "))
    #end_time = int(input("Input End Time (24hr format e.g. 2300): "))

    start_date = dt.datetime(start_year, start_month, start_day)
    end_date = dt.datetime(end_year, end_month, end_day)

    print(end_date-start_date)
    
    get_period(start_time, end_time)
    speriod = start_period
    eperiod = end_period
    print(speriod, eperiod)
    get_dateDiff(start_date, end_date, speriod, eperiod)
    forecast_period = periods_between
    print(forecast_period)


def price_Vector():
    with open(TradingPriceData.csv) as p:
        i = 0
        daily_price_demand = {}
        for i in range(periods_between - 1):
            if i == i + 5:
                pass









if __name__ == "__main__":
    get_datetime(2018, 4, 15, 2019, 5, 13, 1430, 1000)
    #sys.exit(main())