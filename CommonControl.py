from Dac import mcp4725

class CommonControl:
    _maxChannelPressure = 0

    def resetMaxChannelPressure():
        CommonControl._maxChannelPressure = 0

    def setMaxChannelPressure(value):
        if (value>CommonControl._maxChannelPressure):
            CommonControl._maxChannelPressure = value
        #print(f'actual max pressure = {CommonControl._maxChannelPressure}')

    def openInputPressure():
        m = mcp4725()
        m.setPressure(CommonControl._maxChannelPressure)
    
    def closeInputPressure():
        m = mcp4725()
        m.setPressure(0)

    def __init__():
        pass

if __name__=='__main__':
    CommonControl.setMaxChannelPressure(10)
    CommonControl.setMaxChannelPressure(100)
    CommonControl.setMaxChannelPressure(50)
    
    print(f'max={CommonControl._maxChannelPressure}')
    

