import AD4115_SPI_Driver as adc_spi
from AD4115_SPI_Driver import register_map
from time import sleep
import time
import matplotlib.pyplot as plt
import numpy as np
import spidev

import RPi.GPIO as GPIO
import time
import datetime


from pydub import AudioSegment
from pydub.playback import play, _play_with_simpleaudio
import simpleaudio

#-----------------------------------------------------------------------
# GPIO and Sound Setup

#start = AudioSegment.from_wav("/home/vault/Documents/GIT/TheVaultBTYSE/Audio/3-2-1_GO.wav")
mission_impossible = AudioSegment.from_mp3("/home/vault/TheVaultBTYSE/Audio/Mission Impossible Themefull theme.mp3")

GPIO.setmode(GPIO.BOARD)

door_sensor1_pin = 37

button_pin = 12

GPIO.setup(door_sensor1_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#------------------------------------------------------------------------
# SPI and ADC Setup
spi = adc_spi.spi_open()

adc_spi.write_adc(spi,register_map['ADCMODE'],0x8600)
sleep(0.1)
adc_spi.write_adc(spi,register_map['IFMODE'],0x1040)
sleep(0.1)
adc_spi.write_adc(spi,register_map['GPIOCON'],0x2880)
sleep(0.1)
adc_spi.write_adc(spi,register_map['SETUPCON0'],0x420)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH0'],0x8010)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH1'],0x8030)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH2'],0x8050)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH3'],0x8070)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH4'],0x8090)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH5'],0x80B0)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH6'],0x80D0)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH7'],0x80F0)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH8'],0x8110)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH9'],0x8130)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH10'],0x8150)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH11'],0x8170)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH12'],0x8190)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH13'],0x81B0)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH14'],0x81D0)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH15'],0x81F0)
sleep(0.1)

response = adc_spi.read_adc(spi,register_map['ID'])

byte0 = '{0:08b}'.format(response[1])
byte1 = '{0:08b}'.format(response[2])
byte2 = '{0:08b}'.format(response[3])

if hex(int(str(byte0+byte1),2)) == "0x38de":
    print("Comms Connected")
else:
    print("Comms Failed")
    
#-------------------------------------------------------------------------------------------------
# Disable un-connected receiver channels
receiver_connected = [1]*16
on_threshold = 200000

for i in range (100):
    adc_spi.GPIO3_LO(spi)
    adc_spi.GPIO3_HI(spi)
    adc_spi.GPIO3_LO(spi)
    sleep(0.001)
    response = adc_spi.read_adc(spi,register_map['DATA'])
    byte0 = '{0:08b}'.format(response[1])
    byte1 = '{0:08b}'.format(response[2])
    byte2 = '{0:08b}'.format(response[3])
    val = int(str(byte0+byte1+byte0),2)
    if response[4] < 16:
        if val < on_threshold:
            adc_spi.write_adc(spi,register_map['CH{0}'.format(response[4])],0x0)# Disable Channel
            receiver_connected[response[4]] = 0
            
#--------------------------------------------------------------------------------------------------
# Ensure doors are closed before Start Button can be pressed
while True:
    door1_status = GPIO.input(door_sensor1_pin)
    button_status = GPIO.input(button_pin)
    if door1_status == 1:
        print('Exit Door Open')
        time.sleep(1)
    elif door1_status == 0 and button_status == 0:
        playback = _play_with_simpleaudio(mission_impossible)
        print('GAME START')
        break
#--------------------------------------------------------------------------------------------------
# Game Loop
adc_data = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
adc_diff = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
timer = 0
penalty = 0
threshold = -75000
laser_break = 0
last_seconds = 0
while True:
    start = time.time()
    minutes,seconds = divmod(timer, 60)
    if int(seconds) != int(last_seconds):
        print("%02d:%02d"% (minutes,seconds))
        last_seconds = int(seconds)
    door1_status = GPIO.input(door_sensor1_pin)
    if door1_status == 1:
        print('Game Complete')
        break
    adc_spi.GPIO3_LO(spi)
    adc_spi.GPIO3_HI(spi)
    adc_spi.GPIO3_LO(spi)
    sleep(0.001)
#     print(x)
    response = adc_spi.read_adc(spi,register_map['DATA'])
#     print(response)
    byte0 = '{0:08b}'.format(response[1])
    byte1 = '{0:08b}'.format(response[2])
    byte2 = '{0:08b}'.format(response[3])
    val = int(str(byte0+byte1+byte0),2)
    if response[4] < 16:
        adc_data[response[4]].append(val)
        tmp = adc_data[response[4]][-2:]
        if len(tmp) == 2:
            adc_diff[response[4]].append(tmp[1]-tmp[0])
            if adc_diff[response[4]][-1] < threshold:
                penalty = 10
                laser_break = laser_break + 1
            else:
                penalty = 0
    end = time.time()
    timer = timer+(end-start)+penalty
    
print("number of lasers tripped = ", laser_break)
print("Channels Connected = ", receiver_connected.count(1))

sleep(5)
playback.stop()

plt.figure(1)
plt.plot(adc_diff[0])
plt.plot(adc_diff[1])
plt.plot(adc_diff[2])
plt.plot(adc_diff[3])
plt.plot(adc_diff[4])
plt.plot(adc_diff[5])
plt.plot(adc_diff[6])
plt.plot(adc_diff[7])
plt.plot(adc_diff[8])
plt.plot(adc_diff[9])
plt.plot(adc_diff[10])
plt.plot(adc_diff[11])
plt.plot(adc_diff[12])
plt.plot(adc_diff[13])
plt.plot(adc_diff[14])
plt.plot(adc_diff[15])
plt.grid()
plt.show()
plt.figure(2)
plt.plot(adc_data[0])
plt.plot(adc_data[1])
plt.plot(adc_data[2])
plt.plot(adc_data[3])
plt.plot(adc_data[4])
plt.plot(adc_data[5])
plt.plot(adc_data[6])
plt.plot(adc_data[7])
plt.plot(adc_data[8])
plt.plot(adc_data[9])
plt.plot(adc_data[10])
plt.plot(adc_data[11])
plt.plot(adc_data[12])
plt.plot(adc_data[13])
plt.plot(adc_data[14])
plt.plot(adc_data[15])
plt.grid()
plt.show()

adc_spi.spi_close(spi)


