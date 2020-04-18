import pytz
import time
import datetime
from ..temp.functions import phone_target, wifi_off_func, wait_time, read_serial


def script_executor():
    phone_target("Settings")
    wifi_off_func()
    wait_time()


def script_executor_time():
    start_time = str(datetime.datetime.now(pytz.timezone('US/Pacific')).strftime('"%m-%d-%y %H:%M:%S.%f"'))
    return start_time


