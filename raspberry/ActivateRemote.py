import time
import sys
import RPi.GPIO as GPIO

codes=['','']
#taze
codes[0] = '1101100111010111111111101110000110010010111'
#vibration
codes[1] = '1101100111010111111111011101011110000111111'
short_delay =0.0002389
long_delay =0.0007471
extended_delay = 0.0013897


NUM_ATTEMPTS = 10
TRANSMIT_PIN = 24

def transmit_code(code):
    '''Transmit a chosen code string using the GPIO transmitter'''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    for t in range(NUM_ATTEMPTS):
        GPIO.output(TRANSMIT_PIN, 1)
        time.sleep(extended_delay)
        GPIO.output(TRANSMIT_PIN, 0)
        time.sleep(long_delay)
        for i in code:
            if i == '1':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(short_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(long_delay)
            elif i == '0':
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(long_delay)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(short_delay)
            else:
                continue
    GPIO.cleanup()


def activateRemote(code):
    """Method to activate the remote for a brief time

    Parameters
    ----------
    code : int
        which mode to be activated, 0 is taze, 1 is vibration
    
    """
    #5 seconds = 10 iterations
    for x in range(0, 2):
        transmit_code(codes[code])
activateRemote(1)