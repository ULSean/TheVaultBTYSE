import spidev

register_map = {'STATUS':0x0,
             'ADCMODE':0x1,
             'IFMODE':0x2,
             'REGCHECK':0x3,
             'DATA':0x4,
             'GPIOCON':0x6,
             'ID':0x7,
             'CH0':0x10,
             'CH1':0x11,
             'CH2':0x12,
             'CH3':0x13,
             'CH4':0x14,
             'CH5':0x15,
             'CH6':0x16,
             'CH7':0x17,
             'CH8':0x18,
             'CH9':0x19,
             'CH10':0x1A,
             'CH11':0x1B,
             'CH12':0x1C,
             'CH13':0x1D,
             'CH14':0x1E,
             'CH15':0x1F,
             'SETUPCON0':0x20,
             'SETUPCON1':0x21,
             'SETUPCON2':0x22,
             'SETUPCON3':0x23,
             'SETUPCON4':0x24,
             'SETUPCON5':0x25,
             'SETUPCON6':0x26,
             'SETUPCON7':0x27,
             'FILT_CON0':0x28,
             'FILT_CON1':0x28,
             'FILT_CON2':0x2A,
             'FILT_CON3':0x2B,
             'FILT_CON4':0x2C,
             'FILT_CON5':0x2D,
             'FILT_CON6':0x2E,
             'FILT_CON7':0x2F}

def spi_open():
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.mode = 0b11
    spi.max_speed_hz = 1000000
    return spi
    
def spi_close(spi):
    spi.close()
    
def read_adc(spi, register):
    comm_header = 64 #0b0100 0000 which is read in COMMS register
    value = int(register) #register value in decimal
    tx = comm_header+value #combine comm_header with register value to write to ADC
    return spi.xfer2([tx,0x0,0x0,0x0,0x0])

def write_adc(spi, register, value):
    val2bin = '{0:016b}'.format(value)
    byte0 = int('0b' + val2bin[0:8],2)
    byte1 = int('0b' + val2bin[8:16],2)
    spi.writebytes([register,byte0,byte1])# byte0 and byte1 are not in correct format
    
def toggle_GPIO3(spi):
    response = read_adc(spi,register_map['GPIOCON'])
    byte0 = '{0:08b}'.format(response[1])
    byte1 = '{0:08b}'.format(response[2])
    x = int(str(byte0+byte1),2)
    y = (x^(1<<7))
    write_adc(spi,register_map['GPIOCON'],y)

def GPIO3_HI(spi):
    response = read_adc(spi,register_map['GPIOCON'])
    byte0 = '{0:08b}'.format(response[1])
    byte1 = '{0:08b}'.format(response[2])
    x = int(str(byte0+byte1),2)
    y = (x|(1<<7))
    write_adc(spi,register_map['GPIOCON'],y)
    
def GPIO3_LO(spi):
    response = read_adc(spi,register_map['GPIOCON'])
    byte0 = '{0:08b}'.format(response[1])
    byte1 = '{0:08b}'.format(response[2])
    x = int(str(byte0+byte1),2)
    y = (x&~(1<<7))
    write_adc(spi,register_map['GPIOCON'],y)




