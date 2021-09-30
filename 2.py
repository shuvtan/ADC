import RPi.GPIO as GPIO
from time import sleep


dac = [26,19,13,6,5,11,9,10]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3
troykaModule = 17
comparator = 4

def decimal2binary(decimal):
   return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

def bin2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac,signal)
    return signal

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(troykaModule, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comparator, GPIO.IN)



def dac1():
    value = 0
    i = 7
    while (i>=0):
        v = 2**i
        bin2dac(value+v)
        voltage = (v+value)/256*maxVoltage
        sleep(0.001)
        comparatorValue = GPIO.input(comparator)
        if comparatorValue == 1:
            value = value+v
        i = i-1
    print ("Ряд = {:^3} -> {}, output voltage = {:.2f}".format(1,value, voltage))
 

try:
    while True:
        dac1()
   
        
        

except KeyboardInterrupt:
    print ("Программа остановленна из-за риска ошибки")
else:
    print("Ошибок нет")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print("GPIO cleanup!")
 