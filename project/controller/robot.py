#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .connection.connectSerial import  ConnectSerial
import threading
from ..model.movimiento import Movement 
class Robot():
 
    def __init__(self, portSerial):
        self.dataSensorUltraSonic = 0
        self.ultimoMovimiento = "detener"
        self.movimientos = []
        self.movimientos.append(self.ultimoMovimiento)
        self.grabando = False
        # self.connection = ConnectSerial.getInstance(portSerial)
        # self.threadSensorUltraSonic()


    def avanzar(self, timeLastMovement):
        self.connection.setDato('0')
        if self.grabando:
            self.movimientos[-1].time = timeLastMovement
            self.ultimoMovimiento = "avanzar"
            self.movimientos.append(self.ultimoMovimiento)

    def derecha(self, timeLastMovement):
        self.connection.setDato('1')
        if self.grabando:
            self.movimientos[-1].time = timeLastMovement
            self.ultimoMovimiento = "derecha"
            self.movimientos.append(self.ultimoMovimiento)

    def izquierda(self, timeLastMovement):
        self.connection.setDato('2')
        if self.grabando:
            self.movimientos[-1].time = timeLastMovement
            self.ultimoMovimiento = "izquierda"
            self.movimientos.append(self.ultimoMovimiento)

    def detener(self, timeLastMovement):
        self.connection.setDato('3')
        if self.grabando:
            self.movimientos[-1].time = timeLastMovement
            self.ultimoMovimiento = "detener"
            self.movimientos.append(self.ultimoMovimiento)


    def rotar180(self, timeLastMovement):
        #elf.connection.setDato('4')
        if self.grabando:
            self.movimientos[-1].time = timeLastMovement
            self.ultimoMovimiento = "rotar180"
            self.movimientos.append(self.ultimoMovimiento)

    def atras(self, timeLastMovement):
        self.connection.setDato('5')
        if self.grabando:
            self.movimientos[-1].time = timeLastMovement
            self.ultimoMovimiento = "atras"
            self.movimientos.append(self.ultimoMovimiento)

    def abrirPinza(self, timeLastMovement):        
        self.connection.setDato('SA')
        if self.grabando:
            self.movimientos[-1].time = timeLastMovement
            self.ultimoMovimiento = "abrirPinza"
            self.movimientos.append(self.ultimoMovimiento)

    
    def cerrarPinza(self, timeLastMovement):
        self.connection.setDato('SC')
        if self.grabando:
            self.movimientos[-1].time = timeLastMovement
            self.ultimoMovimiento = "cerrarPinza"
            self.movimientos.append(self.ultimoMovimiento)


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
    