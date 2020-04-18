import pytz
import time
import datetime
from ..temp.functions import phone_target, wait_time, dial_number, input_phone_number, number_validation, read_serial



def script_executor():
    phone_target("Phone")
    dial_number()
    wait_time()


def script_executor_time():
    start_time = str(datetime.datetime.now(pytz.timezone('US/Pacific')).strftime('"%m-%d-%y %H:%M:%S.%f"'))
    return start_time
