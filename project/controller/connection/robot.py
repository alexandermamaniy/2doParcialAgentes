#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .connectSerial import  ConnectSerial
import threading

class Robot():
 
    def __init__(self, portSerial):
        self.dataSensorUltraSonic = 0
        # self.connection = ConnectSerial.getInstance(portSerial)
        
        # self.threadSensorUltraSonic()

    def avanzar(self):
        self.connection.setDato('0')
    def derecha(self):
        self.connection.setDato('1')
    def izquierda(self):
        self.connection.setDato('2')
    def detener(self):
        self.connection.setDato('3')
    def rotar180(self):
        pass
        #elf.connection.setDato('4')
    def atras(self):
        self.connection.setDato('5')
    
    def abrirPinza(self):
        self.connection.setDato('SA')
    
    def cerrarPinza(self):
        self.connection.setDato('SC')

    def __targetSensorUltraSonic(self):
        while True:
            try:
                value = int(self.connection.getDato())
                if isinstance(value,int):
                    self.dataSensorUltraSonic = value
                else:
                    raise Exception(f'dato invalido {value}')
            except Exception as e:
                print(e)

    def threadSensorUltraSonic(self):
        threadPlayMovements = threading.Thread(target=self.__targetSensorUltraSonic)
        threadPlayMovements.setDaemon(True)
        threadPlayMovements.start()
    