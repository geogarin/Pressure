import smbus
from time import sleep
class mcp4725:
    MCP4725_WRITE_FAST_MODE = 0b00000000
    MAX_PRESSURE = 1000

    def __init__(self,addr=0x62,i2cBusNo=0):
        self.addr = addr
        self.bus = smbus.SMBus(i2cBusNo)

    def setVoltage(self,val):
        packet = [None]*2
        assert 0 <= val <= 4095
        val &= 0xFFF
        packet[0] = mcp4725.MCP4725_WRITE_FAST_MODE | (val >> 8)
        packet[1] = val & 0xFF
        self.bus.write_block_data(self.addr,0,packet)
    
    def setNormalizedValue(self,val):
        assert 0.0<=val<=1.0

        print(f'{val} {int(val*4095)}')
        self.setVoltage(int(val*4095))

    def setPressure(self,val):
        assert 0.0<=val<=900.0
        self.setNormalizedValue(val/mcp4725.MAX_PRESSURE)

if __name__=='__main__':

    m = mcp4725()
    """
    print('максимальное напряжение')
    m.setNormalizedValue(1) # максимальное напряжение
    sleep(5)
    print('половина напряжения')
    m.setNormalizedValue(0.5) # половина напряжения
    sleep(5)
    print('ноль')
    m.setNormalizedValue(0) # ноль
    print('900')
    m.setPressure(900)
    sleep(5)
    """
    m.setPressure(0)


    
