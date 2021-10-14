import RPi.GPIO as GPIO
import time 
import numpy as np
import matplotlib.pyplot as grafics

#Нумерация GPIO
dac = [26,19,13,6,5,11,9,10]
leds = [21,20,16,12,7,8,25,24]
troykaModule = 17
comparator = 4

bits = len(dac)
levels = 2**bits
maxVoltage = 3.3

U_t = [0]

#Перевод числа из десятичной системы в двоичную
def decimal2binary(decimal):
    return [int(bit) for bit in bin(decimal)[2:].zfill(bits)]

#Подача двоичного кода на GPIO ЦАП для наглядности повышения/понижения напряжения на конденсаторе
def bin2dac(value):
    signal = decimal2binary(value)
    GPIO.output(dac,signal)
    return signal

#АЦП преобразование аналогового сигнала с конденсатора в цифровой
def adc(a,b):
    if (b-a >1):
        signal = bin2dac(int(a + int((b-a)/2)))
        time.sleep(0.01)
        compvalue = GPIO.input(comp)
        if (compvalue == 0):
            adc(a,a+ int((b-a)/2))
        else:
            adc(a+int((b-a)/2), b)
    else:
        signal = bin2dac(int(a+int((b-a)/2)))
        voltage = (a/levels)*maxVoltage
        light(voltage)
        print("Напряжение на конденсаторе = {^ .2f}".format(voltage))
        U_t.append(voltage)


#Показать напряжение на светодиотах leds
def light(voltage):
    p = int((voltage/maxVoltage)*10)
    sign = int(2**(p-1) - 0.5)
    out_sign = decimal2binary(sign)
    GPIO.output(leds, out_sign)

#Подключение входа/выхода // инициализация
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(troykaModule, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comparator, GPIO.IN)
GPIO.setwarnings(False)

try:
     start_time = time.time() #начало отсчёта времени
     while U_t[-1]< 3.26: #выполняем до момента почти полной зарядки конденсатора
        adc(0, 256)
        GPIO.setup(troykaModule, GPIO.OUT, initial = 1) #подаём напряжение на тройка-модуль -> конденсатор заряжается
    
     while U_t[-1] > 0:
        adc(0, 256)
        GPIO.setup(troykaModule, GPIO.OUT, initial = 0) #прекращаем подачу напряжения на тройка-модуль -> конденсатор начинает разряжаться
    
    print("Время эксперимента %s" %(time.time() - start_time)) #фиксируем время
    times = np.linspace(start = 0, stop = time.time() - start_time, num = len(U_t))

    #Создание файлов отсчёта
    U_t_str = [str(item) for item in U_t]
    with open('data.txt', 'w') as f: #сохранение значений напряжения в файл data.txt
        f.write("U(t) = \n")
        f.write(("\n").join(U_t_str))

    with open('settings.txt', 'w') as f: #сохранение отсчёта о времени и единице напряжения в файл settings.txt
        f.write("Время эксперимента: \n")
        f.write(str(time.time() - start_time))
        f.write("Единица напряжения: \n")
        f.write(str(times[1]))
        f.write("Шаг по времени: \n")
        f.write(str(time.time() - start_time)/len(times))
        f.write("Шаг по напряжению: \n")
        f.write(str(3.3/255))

    #Построение графика
    grafics.plot(times, U_t, c="black")
    grafics.show()

except KeyboardInterrupt:
    print ("Программа остановленна из-за риска ошибки")
else:
    print("Ошибок нет")
finally:
    #Cleanup
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    GPIO.cleanup(leds)
    GPIO.cleanup(troykaModule)
    print("GPIO cleanup!")