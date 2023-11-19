import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
#THESE ARE PIN NUMBERS
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, 1)
sleep(10)
GPIO.output(11, 0)
sleep(5)
GPIO.cleanup()