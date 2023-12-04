import AD4115_SPI_Driver as adc_spi
from AD4115_SPI_Driver import register_map
from time import sleep

spi = adc_spi.spi_open()
r = adc_spi.read_adc(spi,register_map['ID'])
print(r)

adc_spi.write_adc(spi,register_map['GPIOCON'],0x2880)
adc_spi.write_adc(spi, register_map['IFMODE'],0x1040)


response = adc_spi.read_adc(spi,register_map['GPIOCON'])
print(response)

byte0 = '{0:08b}'.format(response[1])
byte1 = '{0:08b}'.format(response[2])
byte2 = '{0:08b}'.format(response[3])
print(hex(int(str(byte0+byte1),2)))


# def toggle_GPIO3():
#     response = adc_spi.read_adc(spi,register_map['GPIOCON'])
#     byte0 = '{0:08b}'.format(response[1])
#     byte1 = '{0:08b}'.format(response[2])
#     x = int(str(byte0+byte1),2)
#     y = (x^(1<<7))
#     adc_spi.write_adc(spi,register_map['GPIOCON'],y)


#for i in range(20):
#    toggle_GPIO3()
#    sleep(0.1)

adc_spi.GPIO3_HI(spi)

