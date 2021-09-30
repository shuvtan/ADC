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

try:
    while True:

        for value in range(256):
            
            signal = bin2dac(value)
            sleep(0.0001)
            voltage = value/levels * maxVoltage
            comparatorValue = GPIO.input(comparator)
            if comparatorValue == 0:
                print ("Ряд = {:^3} -> {}, output voltage = {:.2f}".format(value,signal, voltage))
                break
        

except KeyboardInterrupt:
    print ("Программа остановленна из-за риска ошибки")
else:
    print("Ошибок нет")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print("GPIO cleanup!")