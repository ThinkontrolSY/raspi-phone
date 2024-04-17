import time
from signal import pause
import binascii
from gpiozero import Button
from gsmmodem.modem import GsmModem

allowed_numbers = [
    {
        "name": "沈福建",
        "phone": "13867553811"
    },
    {
        "name": "沈彩娟",
        "phone": "15215911207"
    },
    {
        "name": "沈福娟",
        "phone": "15215915979"
    },
    {
        "name": "陈天喜",
        "phone": "85193291"
    },
    {
        "name": "沈阳",
        "phone": "13396553051"
    },
    {
        "name": "沈百泉",
        "phone": "13362177488"
    },
    {
        "name": "沈凌燕",
        "phone": "18906756722"
    }
]

# with open("./phones.yaml", "r") as yamlfile:
#     data = yaml.load(yamlfile, Loader=yaml.FullLoader)

# allowed_numbers = data["contacts"]


def lookUpContact(number):
    if number == None:
        return None
    for p in allowed_numbers:
        if (number == p.get('phone')) or (p.get('phone') in number):
            return p.get('name')
    return None


def handleIncomingCall(call):
    print('Incoming call from {0} ...'.format(call.number))
    name = lookUpContact(call.number)
    if call.number != None and name == None:
        call.hangup()
        return
    if name != None:
        voice("{} 来电话".format(name))
        if call.ringCount >= 5:
            call.answer()
    else:
        print(' Call from {0} is still ringing...'.format(call.number))


k1 = Button(20)
k2 = Button(21)
print('Initializing modem...')
modem = GsmModem('/dev/ttyAMA0', 115200,
                 incomingCallCallbackFunc=handleIncomingCall)
modem.connect()


def voice(text):
    try:
        msg = binascii.hexlify(text.encode("utf_16_be")).decode()
        print(msg)
        responseLines = modem.write('AT+CTTS=1,"{}"'.format(msg))
        print(responseLines)
    except Exception as e:
        print("Exception: ", e)


def k1_released():
    print("K1 released")
    try:
        c = allowed_numbers[0]
        voice("打电话给: {}".format(c.get('name')))
        time.sleep(5)
        modem.dial(c.get('phone'))
    except Exception as e:
        print("Exception: ", e)


def k2_released():
    print("K2 released")
    try:
        c = allowed_numbers[1]
        voice("打电话给: {}".format(c.get('name')))
        time.sleep(5)
        modem.dial(c.get('phone'))
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
