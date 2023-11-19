import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

door_sensor_pin = 12

GPIO.setup(door_sensor_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

print(GPIO.input(door_sensor_pin))
while True:
    if GPIO.input(door_sensor_pin) == 0:
        print('door closed')
    else:
        print('door open')
    time.sleep(0.5)
    
        