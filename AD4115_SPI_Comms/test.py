import AD4115_SPI_Driver as adc_spi
from AD4115_SPI_Driver import register_map
from time import sleep
import time
import matplotlib.pyplot as plt
import numpy as np
import spidev

spi = adc_spi.spi_open()


r = adc_spi.read_adc(spi,register_map['ID'])

byte0 = '{0:08b}'.format(r[1])
byte1 = '{0:08b}'.format(r[2])

print(hex(int(str(byte0+byte1),2)))

adc_spi.write_adc(spi,register_map['ADCMODE'],0x8600)
sleep(0.1)
adc_spi.write_adc(spi,register_map['IFMODE'],0x1040)
sleep(0.1)
adc_spi.write_adc(spi,register_map['GPIOCON'],0x2880)
sleep(0.1)
adc_spi.write_adc(spi,register_map['SETUPCON0'],0x720)
sleep(0.1)

response = adc_spi.read_adc(spi,register_map['SETUPCON0'])
print(response)
byte0 = '{0:08b}'.format(response[1])
byte1 = '{0:08b}'.format(response[2])
print(hex(int(str(byte0+byte1),2)))