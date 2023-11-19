import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

button_pin = 12

GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

print(GPIO.input(button_pin))
while True:
    if GPIO.input(button_pin) == 0:
        print('button pressed')
        time.sleep(1)
