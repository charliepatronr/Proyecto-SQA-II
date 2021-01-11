import re
import time
from subprocess import check_output, check_call
from uiautomator import Device


def read_serial(position=1):
    """
    Function that returns the serial number of device in the first position
    """
    output = check_output(['adb', 'devices'])
    lines = output.splitlines()
    desired_device = lines[position].split()[0]
    return desired_device


def serial_number_device(serial_number=read_serial()):
    """
    Function that returns the serial number and device for future assignment
    """
    return [serial_number, Device(serial_number)]


def phone_target(name):
    """
    Function which receives the name of the target app to open it on the device
    """
    serial_number, d = serial_number_device()
    # Wakes phone up
    check_call(['adb', '-s', serial_number, 'shell', 'input keyevent', 'KEYCODE_WAKEUP'])

    # Travels to home
    check_call(['adb', '-s', serial_number, 'shell', 'input keyevent', 'KEYCODE_HOME'])
    wait_time()

    # Clicks on apps
    d(text='Apps', packageName='com.sec.android.app.launcher').click()
    wait_time()

    # Searches for desired app, allows scrolling

    d(className="android.view.ViewGroup", packageName="com.sec.android.app.launcher") \
        .child_by_text(
        name,
        allow_scroll_search=True,
        resourceId="com.sec.android.app.launcher:id/app_icon"
    ).click()

    wait_time()

    return



def input_phone_number():
    """
    Function that receives the desired phone number to call from the user.
    """
    phone_number = input("Input desired phone number to call ")
    phone_number = str(phone_number)
    if number_validation(phone_number):
        print 'The following phone number {} is being called'.format(phone_number)
        return phone_number


def number_validation(phone_number):
    """
        Function that validates each phone number with a regex and a 15 max length which
        is the length limit for a phone number around the world and with a min length
        of 3 for emergency numbers.
        Returns true if number is validated
    """
    regex = re.match(r'^([\s\d\+\*\+\#]+)$', phone_number)
    length = len(phone_number)
    if 3 <= length <= 15 and regex:
        return True
    else:
        print "Input a valid number and try again "
        return False


def converter(number):
    """
        Function that returns a string corresponding to each number or character inside
        the phone number, to be later appended in the resourceId inside dial_number() so
        these can be identified.
    """
    if number == "1":
        return "one"
    elif number == "2":
        return "two"
    elif number == "3":
        return "three"
    elif number == "4":
        return "four"
    elif number == "5":
        return "five"
    elif number == "6":
        return "six"
    elif number == "7":
        return "seven"
    elif number == "8":
        return "eight"
    elif number == "9":
        return "nine"
    elif number == "0":
        return "zero"
    elif number == "*":
        return "star"
    elif number == "+":
        return "plus"


def dial_number():
    """
    Function that uses other functions to ask for a number, validate it,
    convert it, and finally dial it
    """
    serial_number, d = serial_number_device()
    # Due to unstable phone app cache checks if dial pad button is displayed in contacts page or if phone app goes
    # straight to dial pad
    if d(resourceId='com.samsung.android.contacts:id/floating_action_button',
         packageName='com.samsung.android.contacts').exists:
        d(resourceId='com.samsung.android.contacts:id/floating_action_button',
          packageName='com.samsung.android.contacts').click()
        time.sleep(3)

    else:
        time.sleep(3)

    phone_number = input_phone_number()
    # Dial numbers, converter functions id_number is appended in the resourceId to be clicked
    for individual_number in phone_number:
        id_number = converter(individual_number)
        if id_number == "plus":
            d(resourceId='com.samsung.android.contacts:id/zero',
              className='android.widget.RelativeLayout').long_click()
        else:
            d(resourceId='com.samsung.android.contacts:id/' + id_number,
              className='android.widget.RelativeLayout').click()

    # Calls Phone Number

    d(resourceId='com.samsung.android.contacts:id/dialButton', className='android.widget.ImageButton').click()

    time.sleep(5)
    return


def dial_adb():
    """
    Function that asks for the device, inputs phone number, validates it and
    finally calls the number using adb
    """
    serial_number, d = serial_number_device()
    phone_number = input_phone_number()
    if number_validation(phone_number):
        check_output(['adb', 'shell', 'am', 'start', '-a', 'android.intent.action.CALL', '-d', 'tel:' + phone_number])
    d.wait.update()


def wifi_on_func():
    """
    Function that turns the wifi setting on
    """

    serial_number, d = serial_number_device()

    # Connections
    d(text='Connections', className='android.widget.TextView').click()
    time.sleep(3)

    # Clicks wifi section
    d(text='Wi-Fi', className='android.widget.TextView').click()
    time.sleep(3)

    # Wi-Fi Off to On
    if d(text='OFF', className='android.widget.Switch').exists:
        time.sleep(1)
        print("Status: Wi-Fi Off")
        d(text='OFF', className='android.widget.Switch').click()
        time.sleep(5)
        if d(text='ON', className='android.widget.Switch').exists:
            print("Wi-Fi ON --- Turned On")
    else:
        print("Wi-Fi already ON - No need Turn ON")

    time.sleep(5)
    # home
    check_call(['adb', '-s', serial_number, 'shell', 'input keyevent', 'KEYCODE_HOME'])
    time.sleep(3)

    return


def wifi_off_func():
    """
    Function that turns the wifi setting off
    """

    serial_number, d = serial_number_device()
    # Connections
    d(text='Connections', className='android.widget.TextView').click()
    time.sleep(3)

    # Clicks wifi section
    d(text='Wi-Fi', className='android.widget.TextView').click()
    time.sleep(3)

    # Wi-Fi ON to OFF
    if d(text='ON', className='android.widget.Switch').exists:
        time.sleep(1)
        print("Status: Wi-Fi ON")
        d(text='ON', className='android.widget.Switch').click()
        time.sleep(5)
        if d(text='OFF', className='android.widget.Switch').exists:
            print("Wi-Fi off --- Turned off")
    else:
        print("Wi-Fi already OFF - No need Turn OFF")

    time.sleep(3)
    # home
    check_call(['adb', '-s', serial_number, 'shell', 'input keyevent', 'KEYCODE_HOME'])
    time.sleep(3)

    return


def wait_time(delay=3):
    time.sleep(delay)
