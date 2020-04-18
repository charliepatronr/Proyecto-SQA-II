import pytz
import time
import datetime
from ..scripts.functions import dial_adb, wait_time, read_serial



def script_executor():
    dial_adb()
    wait_time()


def script_executor_time():
    start_time = str(datetime.datetime.now(pytz.timezone('US/Pacific')).strftime('"%m-%d-%y %H:%M:%S.%f"'))
    return start_time
