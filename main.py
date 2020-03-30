import datetime as dt
import calendar
import numpy as np
import matplotlib
import sys
import os
from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout
#import nested_dict as nd


class PowerError(Exception):
    def __init__(self, msg, obj=None):
        if obj is None:
            self.msg = msg
        else:
            self.msg = obj.__class__.__name__ + ':: ' + msg

    def __str__(self):
        return repr(self.msg)


#class Form(QDialog):

#    def __init__(self, parent=None):
#        super(Form, self).__init__(parent)
#        # Create widgets
#        self.edit = QLineEdit("Write my name here")
#        self.button = QPushButton("Show Greetings")
#        # Create layout and add widgets
#        layout = QVBoxLayout()
#        layout.addWidget(self.edit)
#        layout.addWidget(self.button)
#        # Set dialog layout
#        self.setLayout(layout)
#        # Add button signal to greetings slot
#        self.button.clicked.connect(self.greetings)

#    # Greets the user
#    def greetings(self):
#        print ("Hello %s" % self.edit.text())


def get_period(stime, etime):
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
    
    speriod, eperiod = get_period(start_time, end_time)
    #speriod = start_period
    #eperiod = end_period
    print(speriod, eperiod)
    forecast_period = get_dateDiff(start_date, end_date, speriod, eperiod)
    # = periods_between
    print(forecast_period)


#def price_Vector():
#    i = 0
#    daily_price_demand = {} #nd.nested_dict()
#    with open(TradingPriceData.csv) as p:
#        # gather headers except first key header
#        headers = p.next().split(',')[1:]
#        # iterate lines
#        for line in p:
#            # gather the colums
#            cols = line.strip().split(',')
#            # check to make sure this key should be mapped.
#            if cols[0] not in keys:
#                continue
#            # add key to dict
#            daily_price_demand[cols[0]] = dict(
#                # inner keys are the header names, values are columns
#                (headers[idx], v) for idx, v in enumerate(cols[1:]))
#        #for i in range(periods_between - 1):
#            #if i == p[i + 5]:
#            #daily_price_demand[p[i]][p[i+1]] = 

# create empty dictionary
# d = {}

#-----------------------------------------read from file b.csv-----------------
#with open(b_file) as f:
#    # gather headers except first key header
#    headers = f.next().split(',')[1:]
#    # iterate lines
#    for line in f:
#        # gather the colums
#        cols = line.strip().split(',')
#        # check to make sure this key should be mapped.
#        if cols[0] not in keys:
#            continue
#        # add key to dict
#        d[cols[0]] = dict(
#            # inner keys are the header names, values are columns
#            (headers[idx], v) for idx, v in enumerate(cols[1:]))

if __name__ == "__main__":
    get_datetime(2018, 4, 15, 2019, 5, 13, 1430, 1000)
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
#    form = Form()
#    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())