from signal import pause
from sqlite3 import Time
from gpiozero import Button
import yaml
from gsmmodem.modem import GsmModem

allowed_numbers = []

with open("/home/pi/work/phones.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

allowed_numbers = data["phonenumbers"]


def checkNumber(number):
    if number == None:
        return False
    for p in allowed_numbers:
        if (number == p) or (p in number):
            return True
    return False


def handleIncomingCall(call):
    if call.number != None and not checkNumber(call.number):
        call.hangup()
        return
    if call.ringCount >= 5 and checkNumber(call.number):
        call.answer()
    else:
        print(' Call from {0} is still ringing...'.format(call.number))


k1 = Button(20)
k2 = Button(21)
print('Initializing modem...')
modem = GsmModem('/dev/ttyAMA0', 115200,
                 incomingCallCallbackFunc=handleIncomingCall)
modem.connect()

print(modem.manufacturer)


def k1_released():
    print("K1 released")
    try:
        modem.dial(allowed_numbers[0])
    except Exception as e:
        print("Exception: ", e)


def k2_released():
    print("K2 released")
    try:
        modem.dial(allowed_numbers[1])
    except Exception as e:
        print("Exception: ", e)


k1.when_released = k1_released
k2.when_released = k2_released

print('Waiting for incoming calls...')
# try:
#     # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal
#     modem.rxThread.join(2**31)
# finally:
#     modem.close()

pause()
