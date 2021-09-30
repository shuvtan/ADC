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



def uravno(value):
    while (value >= 1):
        a = value
        i = 0
        while a>1:
            a = a/2
            i = i+1

        signal = bin2dac(i)
        sleep(0.0001)
        voltage = value/levels * maxVoltage
        comparatorValue = GPIO.input(comparator)
        if comparatorValue == 1:
            print ("Ряд = {:^3} -> {}, output voltage = {:.2f}".format(value,signal, voltage))
            value = value/2
            uravno(value)
        else:
            print ("Ряд = {:^3} -> {}, output voltage = {:.2f}".format(value,signal, voltage))
            value = (value/2) + value
            uravno(value)
        a = value
        i = 0
        while a>1:
            a = a/2
            i = i+1
        return decimal2binary(i)
        
try:
    while True:
        n = 128
        m = uravno(n)
        print (m)
         
        
        

except KeyboardInterrupt:
    print ("Программа остановленна из-за риска ошибки")
else:
    print("Ошибок нет")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print("GPIO cleanup!")