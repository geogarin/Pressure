import sys
import subprocess

print(sys.path)

#subprocess.Popen("onboard")
#subprocess.Popen(["pkill", "onboard"])

d=2/3

s=str.format("{:.{}f}",d,3)

print(f"{s}")


numbers = [0]*5

numbers[0]=10
numbers[1]=5

Sum = sum(numbers)
print(Sum)

print(numbers)