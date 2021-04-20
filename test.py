import sys
import subprocess

print(sys.path)

#subprocess.Popen("onboard")
#subprocess.Popen(["pkill", "onboard"])

numbers = [0]*5

numbers[0]=10
numbers[1]=5

Sum = sum(numbers)
print(Sum)

print(numbers)