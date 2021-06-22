class ValveControl:
    _maxChannelPressure = 0

    def resetMaxChannelPressure():
        ValveControl._maxChannelPressure = 0

    def setMaxChannelPressure(value):
        if (value>ValveControl._maxChannelPressure):
            ValveControl._maxChannelPressure = value
        #print(f'actual max pressure = {ValveControl._maxChannelPressure}')
    
    def __init__():
        pass


if __name__=='__main__':
    ValveControl.setMaxChannelPressure(10)
    ValveControl.setMaxChannelPressure(100)
    ValveControl.setMaxChannelPressure(50)
    
    print(f'max={ValveControl._maxChannelPressure}')
    

