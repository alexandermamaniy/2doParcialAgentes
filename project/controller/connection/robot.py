#!/usr/bin/python3
# -*- coding: utf-8 -*-

from decouple import config
from .connectSerial import  ConnectSerial

class Robot():
 
    def __init__(self):
        self.connection = ConnectSerial.getInstance(config('USER_SERIAL'))
    
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
    
