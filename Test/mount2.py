import os
from time import sleep
from datetime import datetime

def usbMounted():
    s='ls /media/gga'
    r=os.popen(s).read()
    print(f'ls=|{r}| len={len(r)}')
    return len(r)>0

print(f'start {datetime.now()}')
usbFlashMounted = usbMounted()
print(f'after check {datetime.now()}')
#r=str(os.system("ls /dev/sd*"))
#s=str.format("pumount /media/gga")
#r=os.popen(s)
if not usbFlashMounted:
    print(f'before list {datetime.now()}')
    rr=os.popen('ls /dev/sd*').read()
    r= rr.splitlines()
    print(f'after list {datetime.now()}')
    if not r is None:
        s=str.format("pmount {} /media/gga",r[0])
        rr = os.popen(s).read()
        print(f'mount={rr}')

        while not usbFlashMounted:
            sleep(1)
            print(f'wait {datetime.now()}')
            usbFlashMounted = usbMounted()

if usbFlashMounted:
    ff = open('/media/gga/qwe2.txt','w')
    ff.write('asdasdasd')
    ff.close()

    s=str.format("pumount /media/gga")
    os.popen(s)
    print(f'save {datetime.now()}')

print('finish')    
#tt=os.popen('pmount ')
#print(f'{r}')

