import AD4115_SPI_Driver as adc_spi
from AD4115_SPI_Driver import register_map
from time import sleep
import time
import matplotlib.pyplot as plt
import numpy as np
import spidev

spi = adc_spi.spi_open()


r = adc_spi.read_adc(spi,register_map['ID'])

adc_spi.write_adc(spi,register_map['ADCMODE'],0x600)
sleep(0.1)
adc_spi.write_adc(spi,register_map['IFMODE'],0x1040)
adc_spi.write_adc(spi,register_map['GPIOCON'],0x2880)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH0'],0x8010)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH1'],0x8030)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH2'],0x8050)
sleep(0.1)
adc_spi.write_adc(spi,register_map['CH3'],0x8070)

start = time.time()
for x in range(100):

    adc_spi.GPIO3_LO(spi)
    adc_spi.GPIO3_HI(spi)
    adc_spi.GPIO3_LO(spi)
    sleep(0.001)
    response = adc_spi.read_adc(spi,register_map['STATUS'])
    print(response)

end = time.time()    
print(end-start)

#start = time.time()

# adc_data = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
# print(adc_data)
# 
# for x in range(1000):
#     sleep(0)
#     print(x)
#     response = adc_spi.read_adc(spi,register_map['DATA'])
#     print(response)
#     byte0 = '{0:08b}'.format(response[1])
#     byte1 = '{0:08b}'.format(response[2])
#     byte2 = '{0:08b}'.format(response[3])
#     val = int(str(byte0+byte1+byte0),2)
#     if response[4] < 16:
#         adc_data[response[4]].append(val)