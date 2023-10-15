import spidev
import math

spi = spidev.SpiDev()
spi.open(0,0)

spi.mode = 0b11
spi.max_speed_hz = 500000


response = spi.xfer2([0x47,0x0,0x0])

print(response)

msb = bin(response[1])[2:]
lsb = bin(response[2])[2:]
print(hex(int(str(msb+lsb),2)))


spi.close()