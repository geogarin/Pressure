from pyiArduinoI2Crelay import *        # Подключаем библиотеку для работы с реле и силовыми ключами.
from time import sleep
d=0.3
for a in range(17,22):                  # Подключаем метод sleep библиотеки time
    pwrfet = pyiArduinoI2Crelay(a);      # Создаём объект pwrfet для работы с функциями и методами библиотеки Py_iarduino_I2C_Relay, указывая адрес модуля на шине I2C.
                                        # Если объявить объект без указания адреса (pwrfet = pyiArduinoI2Crelay()), то адрес будет найден автоматически.
    pwrfet.digitalWrite(ALL_CHANNEL,LOW)   # Выключаем все каналы модуля.
    for i in range(0,1):                           # Входим в бесконечный цикл
        #Включаем и выключаем каналы модуля:    #
        pwrfet.digitalWrite(1,HIGH)           # Включаем 1 канал
        pwrfet.digitalWrite(4,LOW)            # и выключаем 4.
        sleep(d)                             # Ждём   500 мс.
        pwrfet.digitalWrite(2,HIGH)           # Включаем 2 канал
        pwrfet.digitalWrite(1,LOW)            # и выключаем 1.
        sleep(d)                             # Ждём   500 мс.
        pwrfet.digitalWrite(3,HIGH)           # Включаем 3 канал
        pwrfet.digitalWrite(2,LOW)            # и выключаем 2.
        sleep(d)                             # Ждём   500 мс.
        pwrfet.digitalWrite(4,HIGH)           # Включаем 4 канал
        pwrfet.digitalWrite(3,LOW)            # и выключаем 3.
        sleep(d)                             # Ждём   500 мс.
    pwrfet.digitalWrite(ALL_CHANNEL,LOW)