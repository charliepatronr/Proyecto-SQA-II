import datetime
import pytz
import sys
from functions import wait_time, read_serial
from Project.classes1 import dial_number_adb, dial_number_ui, wifi_on, wifi_off

script_list = [dial_number_adb, dial_number_ui, wifi_on, wifi_off]


def script_execution():
    serial_number = None
    script_to_run = None
    active = True

    while active:
        script_to_run = input(
            "To execute the desired script press the respective number:\n 1. Wifi On \n 2. Wifi Off \n "
            "3. Call ADB \n 4. Call UI\n 5. Exit\n")

        if script_to_run == 1:
            individual_script = wifi_on
        elif script_to_run == 2:
            individual_script = wifi_off
        elif script_to_run == 3:
            individual_script = dial_number_adb
        elif script_to_run == 4:
            individual_script = dial_number_ui
        elif script_to_run > 4:
            sys.exit("Exited")

        try:
            serial_number = individual_script.read_serial()
        except Exception as ex:
            print(ex)

        start_time_execution = individual_script.script_executor_time()
        print('Device {0} tests started at :  {1}'.format(serial_number, start_time_execution))

        try:
            individual_script.script_executor()
            wait_time()

        except Exception as ex:
            print(ex)

        finally:
            stop_time_execution = individual_script.script_executor_time()
            print('Device {0} tests ended at :  {1}'.format(serial_number, stop_time_execution))


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    script_execution()
