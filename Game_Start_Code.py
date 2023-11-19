import RPi.GPIO as GPIO
import time

from pydub import AudioSegment
from pydub.playback import play, _play_with_simpleaudio

start = AudioSegment.from_wav("/home/strimble/Documents/GIT/TheVaultBTYSE/Audio/3-2-1_GO.wav")
mission_impossible = AudioSegment.from_mp3("/home/strimble/Documents/GIT/TheVaultBTYSE/Audio/Mission Impossible Themefull theme.mp3")

GPIO.setmode(GPIO.BOARD)

door_sensor1_pin = 37
door_sensor2_pin = 36

button_pin = 12

GPIO.setup(door_sensor1_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(door_sensor2_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:
    while True:
        door1_status = GPIO.input(door_sensor1_pin)
        door2_status = GPIO.input(door_sensor2_pin)
        button_status = GPIO.input(button_pin)
        if door1_status == 1:
            print('Door 1 Open')
            time.sleep(1)
        elif door2_status == 1:
            print('Door 2 Open')
            time.sleep(1)
        elif door1_status == 0 and door2_status == 0 and button_status == 0:
            playback = _play_with_simpleaudio(start)
            print('GAME START')
            break
        
    # time.sleep(5)
    # print(thread.is_alive())

    time.sleep(3)
    playback = _play_with_simpleaudio(mission_impossible)
    while True:
        door2_status = GPIO.input(door_sensor2_pin)
        if door2_status == 1:
            print('Game Complete')
            time.sleep(5)
            playback.stop()
            break



