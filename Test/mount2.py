import os
#r=str(os.system("ls /dev/sd*")) 
rr=os.popen('ls /dev/sd*').read()
r= rr.splitlines()

s=str.format("pmount {} /media/gga",r[0])
os.popen(s)
print(f'{s}')

ff = open('/media/gga/fff.txt','w')
ff.write('asdasdasd')
ff.close()

s=str.format("pumount /media/gga")
os.popen(s)
#tt=os.popen('pmount ')
#print(f'{r}')