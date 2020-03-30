'''
Created on 11/09/2012

@author: todd
'''

from enum import Enum, unique, IntEnum
import sys
import os
import copy
import logging
import math
import datetime as dt
import calendar
import numpy as np
import random
import unittest

#import power_enum as pe

# eg implement property
# property(fget=None, fset=None, fdel=None, doc=None) -> property attribute
# class C(object):
#     def getx(self): return self.__x
#     def setx(self, value): self.__x = value
#     def delx(self): del self.__x
#     x = property(getx, setx, delx, "I'm the 'x' property.")

MAX_DESC_LEN = 60

PERIODS_PER_DAY = 48

m_curr_plot_figure = 1


class PowerError(Exception):
    def __init__(self, msg, obj=None):
        if obj is None:
            self.msg = msg
        else:
            self.msg = obj.__class__.__name__ + ':: ' + msg

    def __str__(self):
        return repr(self.msg)


def get_next_plot():
    global m_curr_plot_figure
    m_curr_plot_figure += 1
    return m_curr_plot_figure - 1


def get_day_offset(date):
    # convert datetime arg to date & time of day timeslot 
    # reset date to be within the hist period
    start_of_year = date.replace(month=1, day=1)
    rslt = (date - start_of_year).days
    # TODO! - this has a very big effect on demand calibration not sure why
    # TODO! High how to handle leap years in calibration
    # hack move 29th to the 28th
    # if calendar.isleap(date.year):
    #     if date > date.replace(month=2, day=28):
    #         return rslt - 1
    return rslt


def get_period(time):
    # convert time arg to time of day timeslot
    period = time.hour * 2 + 1
    if 0 < time.minute:
        period += 1
    return period - 1


def get_month(days):
    # convert number of days into a month (use base year 2009 to avoid leap year)
    return (dt.datetime(2009, 1, 1) + dt.timedelta(days=days)).month


# this is the enum version of seasons
# TODO: low make this function 1 based so can use moth function
#def get_season(month):
#    season = pe.Seasons.SUMMER
#    if (month == 0) or (month == 1) or (month == 11):
#        season = pe.Seasons.SUMMER
#    elif (month >= 2 and month <= 4):
#        season = pe.Seasons.AUTUMN
#    elif (month >= 5 and month <= 7):
#        season = pe.Seasons.WINTER
#    elif (month >= 8 and month <= 10):
#        season = pe.Seasons.SPRING
#    else:
#        raise ValueError("Invalid month %i" %(month))
#    return season.value


def print_array(a, precision=2, new_line=False, format_spec=""):
    rslt_str = ""
    term_str = "\n" if new_line else ""
    format_str = ("{:." + str(precision) + "f}") if format_spec == "" else format_spec
    if len(a.shape) == 1:
        for x in a[0:-1]:
            rslt_str += format_str.format(x) + ","
        rslt_str += format_str.format(a[-1]) + term_str
    #             rslt_str += "{0:.2f}".format(x) + ","
    #         rslt_str += "{0:.2f}".format(a[-1]) + term_str
    elif len(a.shape) == 2:
        for row in a:
            for x in row[0:-1]:
                rslt_str += format_str.format(x) + ","
            rslt_str += format_str.format(row[-1]) + term_str
        #                 rslt_str += "{0:.2f}".format(x) + ","
        #             rslt_str += "{0:.2f}".format(row[-1]) + term_str
    else:
        raise ValueError("can only print up to 2 dimension arrays")
    return rslt_str


def print_list(lst, **kwargs):
    sep = kwargs.get('sep', ',')
    format_spec = kwargs.get('format_spec', '{!s}')

    rslt_str = ""
    # default format is the string representation {!s} the rerr is {!r}
    num = len(lst)
    if num <= 0:
        rslt_str = ""
    else:
        # if here then a non-empty list
        for i in range(num - 1):
            rslt_str += (format_spec + sep).format(lst[i])
        rslt_str += format_spec.format(lst[-1])

    return rslt_str


def print_list_deep(lst, **kwargs):
    sep = kwargs.get('sep', ',')
    format_spec = kwargs.get('format_spec', '{!s}')
    # forward_args=kwargs.get('forward_args', False)
    prt_funct_name = kwargs.get('print_function', '__str__')

    rslt_str = ""
    # use_prefix = (prefix != "")
    # default format is the string representation {!s} the rerr is {!r}
    num = len(lst)
    if num <= 0:
        rslt_str = ""
    else:
        # if here then a non-empty list
        for i in range(num):
            # if use_prefix:
            meth = getattr(lst[i], prt_funct_name)
            if i < num - 1:
                rslt_str += (format_spec + sep).format(meth(**kwargs))
            else:
                rslt_str += format_spec.format(meth(**kwargs))

    return rslt_str


def setup_logging(log_filename, log_level=logging.DEBUG, clear_log=False):
    """ Setup logging in a standard format.
    :param log_filename: the filename to whcih to write log entries
    :param log_level: the log level, which log entries are actually written.
    :param clear_log: delete and pre-existing log file.
    :return:
    """
    try:
        if clear_log:
            os.remove(log_filename)
    except OSError:
        pass

    format_str = '%(asctime)s %(levelname)s:%(message)s'
    logging.basicConfig(filename=log_filename, format=format_str, level=log_level)
    console = logging.StreamHandler()
    console.setLevel(log_level)
    formatter = logging.Formatter('%(levelname)s:%(message)s')
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)


def move_window(x, window_len=11, window='hanning'):
    # """smooth the data using a window with requested size.

    # This method is based on the convolution of a scaled window with the signal.
    # The signal is prepared by introducing reflected copies of the signal 
    # (with the window size) in both ends so that transient parts are minimized
    # in the begining and end part of the output signal.

    # input:
    # x: the input signal 
    # window_len: the dimension of the smoothing window; should be an odd integer
    # window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
    # flat window will produce a moving average smoothing.

    # output:
    # the smoothed signal

    # example:

    # t=linspace(-2,2,0.1)
    # x=sin(t)+randn(len(t))*0.1
    # y=smooth(x)

    # see also: 

    # numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    # scipy.signal.lfilter

    # TODO:low the window parameter could be the window itself if an array instead of a string   
    # """

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len - 1:0:-1], x, x[-1:-window_len:-1]]
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')

    y = np.convolve(w / w.sum(), s, mode='valid')
    return y


def linear_lst_sqs(x_vals, y):
    """This performs a linear least squares fit returning the tuple (gradient, y-intercept)."""
    A = np.vstack([x_vals, np.ones(len(x_vals))]).T
    result = np.linalg.lstsq(A, y)
    # note: (m, c) = result[0]
    return result[0]


def general_lst_sqs():
    pass


class ZeroRand(object):
    """This class implments a random generator where the random stream is all zeros."""

    def __init__(self):
        pass

    def seed(self, seed=0):
        pass

    def random(self):
        return 0.0

    def gauss(self, mu, sigma):
        return 0.0


class TestRand(object):
    """This class implments a test random generator where the radom stream is set externally."""

    def __init__(self):
        self.rand_data = [-0.348327248, -0.509082324, -2.343443158, -1.090581234, -0.858025656, 0.303616401,
                          0.163561341, 2.269478685, -1.35370479, -0.538261309, -0.729239834, -0.702871573, 0.258354705,
                          1.104878637, 0.483139346, -0.640985464, 0.753935376, 1.315341832, 1.852348929, 1.242790339,
                          0.881447615, 0.892738326, 0.833203032, -0.331699768, 0.327335742, 0.163986844, -0.674826712,
                          1.534870352, -0.287946557, 0.144225138, 0.6830249, -1.885083917, 0.968947142, 0.816483565,
                          0.931849659, 2.038983752, 0.87943484, 0.0639302, -0.035171651, 0.126049603, -0.111577792,
                          -1.655515206, 1.122586203, 0.71371147, 1.078779201, 0.331623629, -1.423853106]
        self.index = 0

    def seed(self, seed=0):
        self.index = seed % len(self.rand_data)

    def random(self):
        rslt = self.rand_data[self.index]
        self.seed(self.index + 1)
        return rslt

    def gauss(self, *args):
        return self.random()

    def uniform(self, *args):
        return abs(self.random())


def rand_factory(rand_arg):
    rand_name = rand_arg.lower()
    if rand_name == "rand":
        return random.Random
    elif rand_name == "test":
        return TestRand
    elif rand_name == "zero":
        return ZeroRand
    return None


class TimeStep(object):
    """This hold the time step used in a simulation or time series. 17520 periods per year"""

    def __init__(self, init_num_dt_year=PERIODS_PER_DAY * 365):
        self.__num_dt_year = 0
        self.__num_dt_day = 0
        self.__dt = 0.0
        self.__sqrt_dt = 0.0
        self.__time_delta = None
        self.init_datetime = None  # init datetime
        self.curr_time_step = 0  # curr time step (integer)
        self.curr_time = 0.0  # curr time in yrs
        self.curr_datetime = None  # curr timedelta
        self.day_index = None
        self.night_index = None

        self.set_num_dt_year(init_num_dt_year)
        self.reset()

    def reset(self):
        self.curr_time_step = 0
        self.curr_time = 0.0
        self.curr_datetime = copy.copy(self.init_datetime)

    def increment(self):
        self.curr_time_step += 1
        self.curr_time += self.__dt
        self.curr_datetime += self.__time_delta

    # get / set
    def get_num_dt_year(self):
        return self.__num_dt_year

    def set_num_dt_year(self, arg_in):
        value_int = int(arg_in)
        if (value_int <= 0) or (value_int % (365 * 24) != 0):
            raise ValueError("The number of steps per year must be a whole number per hour.")
        self.__num_dt_year = value_int
        self.__num_dt_day = self.__num_dt_year // 365
        self.__dt = 1.0 / self.__num_dt_year  # time step in years
        self.__sqrt_dt = math.sqrt(self.dt)
        self.__time_delta = dt.timedelta(seconds=int(24.0 * 60.0 * 60.0 / self.__num_dt_day))

        periods_per_hr = self.__num_dt_day / 24
        self.day_index = np.array([False] * self.__num_dt_day)
        self.day_index[int(7 * periods_per_hr): int((7 + 12) * periods_per_hr)] = True  # this assumes day = 7am -> 7pm
        self.night_index = np.invert(self.day_index)

    num_dt_year = property(get_num_dt_year, set_num_dt_year, None, "The number of steps per year.")

    # get only
    def get_dpy(self):
        return 365

    dpy = property(get_dpy, None, None, "The number of days in a year.")

    def get_num_dt_day(self):
        return self.__num_dt_day

    num_dt_day = property(get_num_dt_day, None, None, "The number of steps per day.")

    def get_dt(self):
        return self.__dt

    dt = property(get_dt, None, None, "The duration of a step in years.")

    def get_sqrt_dt(self):
        return self.__sqrt_dt

    sqrt_dt = property(get_sqrt_dt, None, None, "The square root of duration of a step in years.")

    def get_time_delta(self):
        return self.__time_delta

    time_delta = property(get_time_delta, None, None, "The time delta of a step.")

    def get_dt_secs(self):
        return self.__time_delta.seconds

    dt_secs = property(get_dt_secs, None, None, "The number of seconds in a step.")

    # methods
    def get_timeslot(self, datetime):
        # convert datetime to timeslot wihtin the day
        startOfDate = dt.datetime(datetime.year, datetime.month, datetime.day)
        return int(float((datetime - startOfDate).seconds) / self.__time_delta.seconds)

    def get_day_night(self, datetime):
        if self.day_index[self.get_timeslot(datetime)]:
            return pe.DayNights.DAY.value
        else:
            return pe.DayNights.NIGHT.value


def set_attrib_args(obj, skip=None, mapper=None, argument_attribute_name='', dict_arg=None, **kwargs):
    """ Set an objects attributes according to a passed in dictionary or kwargs.

    :param obj: object to set the attributes.
    :param skip: list of attribute names to skip, not set.
    :param mapper: translates the attribute names if present in this dict.
    ;param argument_attribute_name: copy the argument dictionary and store it in a attribute of this name (ignore if '')
    :param args: the first argument should be the dict of attributes to set.
    :param kwargs: the key wrod args is the dict of attributes to set.

    :param attrib_dict: dict of attributes to set.
    :return: the obj with its attributes set.
    """
    # set via an unnamed dict
    if dict_arg is not None:
        if (type(dict_arg) is dict):
            _set_attrib_dict(obj, skip, mapper, argument_attribute_name, dict_arg)
        else:
            raise ValueError("Passed a non dictionary to the dict_arg")
    # set via named args (done after so has precendence)
    _set_attrib_dict(obj, skip, mapper, argument_attribute_name, kwargs)
    return obj


def _set_attrib_dict(obj, skip, mapper, argument_attribute_name, attrib_dict):
    """ Set an objects attributes according to a passed in dictionary.

    :param obj: object to set the attributes.
    :param skip: list of attribute names to skip, not set.
    :param mapper: translates the attribute names if present in this dict.
    :param attrib_dict: dict of attributes to set.
    :return: the obj with its attributes set.
    """
    # no effect if dict is None or empty
    if attrib_dict is None or 0 == len(attrib_dict):
        return obj  # do not set anything

    # here assumed anything goes
    check_skip = skip is not None
    check_mapper = mapper is not None
    for attrib_name in list(attrib_dict.keys()):
        if check_skip and (attrib_name in skip):
            continue  # deliberately skipped
        attrib_value = attrib_dict[attrib_name]
        if check_mapper:
            attrib_name = mapper.get(attrib_name, attrib_name)  # convert to mapped name else keep unchanged
        setattr(obj, attrib_name, attrib_value)
    if '' != argument_attribute_name:
        setattr(obj, argument_attribute_name, attrib_dict.copy())
    return obj


class SetAttribTestCase(unittest.TestCase):
    class TestClass(object):
        def __str__(self):
            rslt = "TestClass: "
            rslt += str(self.__dict__)
            return rslt

    def setUp(self):
        self.test_dict = {
            'db_connection_type': 'sql',
            'db_type': 'MySQLdb',
            'db_server': 'localhost',
            'db_user': 'root',
            'db_password': 'pw',
            'db_database': 'db',
            'db_port': 3307
        }
        self.test_class = SetAttribTestCase.TestClass()
        self.print_class = False

    def tearDown(self):
        pass

    def _check_values(self, rslt_class, skip=None, mapper=None):
        # input:     'db_user': 'root'
        # output:    'user': 'root'
        # mapper:    'db_user': 'usr'
        # inv_mapper:'usr': 'db_user'

        # test_dict is the test input (expected)
        keys = list(self.test_dict.keys())
        keys.sort()
        for key in keys:
            if skip is not None and (key in skip):
                continue  # deliberately skipped
            expected = self.test_dict.get(key, 'Not present!!!')
            rslt = getattr(rslt_class, key, 'Not present!!!')
            if mapper is not None and key in mapper:
                rslt = getattr(rslt_class, mapper[key], 'Not present!!!')
            self.assertEqual(rslt, expected, "Error in selection expected [{}] result was [{}]".format(expected, rslt))

    def test_init_arg(self):
        skip = None  # { 'db_port': 1 }
        set_attrib_args(self.test_class, dict_arg=self.test_dict)
        if self.print_class:
            print("test_init_arg  : " + str(self.test_class))
        self._check_values(self.test_class)

    def test_init_kwarg(self):
        set_attrib_args(self.test_class, None, None, **self.test_dict)
        if self.print_class:
            print("test_init_kwarg: " + str(self.test_class))
        self._check_values(self.test_class)

    def test_init_none_kwarg(self):
        set_attrib_args(self.test_class, **self.test_dict)
        if self.print_class:
            print("test_init_none_kwarg: " + str(self.test_class))
        self._check_values(self.test_class)

    def test_init_skip(self):
        skip = {'db_user': 1}
        set_attrib_args(self.test_class, skip, **self.test_dict)
        if self.print_class:
            print("test_init_skip : " + str(self.test_class))
        self._check_values(self.test_class, skip)

    def test_init_map(self):
        mapper = {'db_user': 'usr'}
        set_attrib_args(self.test_class, None, mapper, **self.test_dict)
        if self.print_class:
            print("test_init_map : " + str(self.test_class))
            # print "test_init_map : " + str(self.test_dict)
        self._check_values(self.test_class, None, mapper)


def run_unit_tests():
    # print("run_unit_tests")
    suite = unittest.TestLoader().loadTestsFromTestCase(SetAttribTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)


def main(argv=None):
    # sql = """SELECT [temp_date], [time_slot], [temperature], [demand] FROM [NEMdata].[dbo].[vw_temp_vs_demand]
    # where region = 'VIC1' order by temp_date, time_slot"""
    # sql = """SELECT settDATE, periodid, availability FROM power.tabtotalavailability
    # where regionid = 'VIC1' order by settdate, periodid;"""
    # raw_rows = get_db_data_deprecated(sql)
    # raw_transpose = zip(*raw_rows)
    # hist_dates = np.array(raw_transpose[0], dtype=object)
    # hist_period = np.array(raw_transpose[1], dtype=np.int)
    # hist_period -= 1       # make it zero based
    # hist_avail = np.array(raw_transpose[2], dtype=np.float)
    # print hist_dates
    # print hist_avail

    run_unit_tests()
#    print(get_season(1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
