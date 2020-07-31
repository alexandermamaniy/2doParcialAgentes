from decouple import config
import cv2
import numpy as np
from project.controller.robot import Robot
from project.controller.ai_controller import *
import signal
import datetime
import sys


# def buscarPorFiguraColor(figure, color, dir_camera):
#    
#     cap = cv2.VideoCapture()
#     active = cap.open(dir_camera)
#     # robot = Robot()    
#     while active:
#         active, frame = cap.read()
#         located, new_dir = model_ai.serch_by_color_and_figure(frame, figure, color)
#         if located:
#             print(new_dir)
#             if new_dir == -1:
#                 pass
#                 # robot.izquierda()
#             elif new_dir == 1:
#                 pass
#                 # robot.derecha()
#             else:
#                 pass
#                 # robot.detener()

#         cv2.imshow("Camara", frame)
#         if cv2.waitKey(1) == ord('q'):
#             cv2.destroyAllWindows()
#             break



# def buscarPorFigura(figure, dir_camera):
#     model_ai = Model_AI()
#     cap = cv2.VideoCapture()
#     active = cap.open(dir_camera)
       
#     while active:
#         active, frame = cap.read()
#         located, new_dir =  model_ai.search_by_figure(frame, figure)
#         if located:
#             print(new_dir)
#             if new_dir == -1:
#                 pass
#                 # robot.izquierda()
#             elif new_dir == 1:
#                 pass
#                 # robot.derecha()
#             else:
#                 pass
#                 # robot.detener()

#         cv2.imshow("Camara", frame)
#         if cv2.waitKey(1) == ord('q'):
#             cv2.destroyAllWindows()
#             break

def searchPatronRobot(robot, dir_camera, funcion_callback, *args ):
    
    cap = cv2.VideoCapture()
    active = cap.open(dir_camera)
    recogioObject = False
    lastTime = datetime.datetime.now()
    robot.grabando = True
    ultimoMovimiento = robot.ultimoMovimiento
    while active:
        active, frame = cap.read()
        located, new_dir =  funcion_callback(frame, *args)
        if located and not recogioObject :
            print(new_dir, robot.dataSensorUltraSonic)
            distancia = robot.dataSensorUltraSonic
            if new_dir == -1 and  distancia >= 10 and ultimoMovimiento != 'izquierda':
                
                print('va Izquierda')
                nowTime = datetime.datetime.now()
                segundosTrascurridos = (lastTime - nowTime).total_seconds()
                lastTime = nowTime
                # robot.izquierda(segundosTrascurridos)
                ultimoMovimiento = 'izquierda'

            elif new_dir == 1 and  distancia >= 10 and ultimoMovimiento != 'derecha' :
                print('va derecha')
                nowTime = datetime.datetime.now()
                segundosTrascurridos = (lastTime - nowTime).total_seconds()
                lastTime = nowTime
                # robot.derecha(segundosTrascurridos)
                ultimoMovimiento = 'derecha'
            elif new_dir == 0 and  distancia >= 9  and ultimoMovimiento != 'detenerse' :
                print('se detiene')
                nowTime = datetime.datetime.now()
                segundosTrascurridos = (lastTime - nowTime).total_seconds()
                lastTime = nowTime
                # robot.detener(segundosTrascurridos)
                
                print('avanza hacia delante')
                nowTime = datetime.datetime.now()
                segundosTrascurridos = (lastTime - nowTime).total_seconds()
                lastTime = nowTime
                # robot.avanzar(segundosTrascurridos)
                ultimoMovimiento = 'avanzar'

            elif new_dir == 0 and  distancia <= 4  and ultimoMovimiento != 'detenerse' :
                print('se detiene')
                nowTime = datetime.datetime.now()
                segundosTrascurridos = (lastTime - nowTime).total_seconds()
                lastTime = nowTime
                # robot.detener(segundosTrascurridos)
                ultimoMovimiento = 'detenerse'
                if new_dir == 0 and  (distancia >= 2 or   distancia <= 3):
                    print('cerrar pinza')
                    nowTime = datetime.datetime.now()
                    segundosTrascurridos = (lastTime - nowTime).total_seconds()
                    lastTime = nowTime
                    # robot.cerrarPinza(segundosTrascurridos)
                    robot.grabando = False
                    ultimoMovimiento = 'giro180'

                    print('Dar vuelta de 180 grados')
                    nowTime = datetime.datetime.now()
                    segundosTrascurridos = (lastTime - nowTime).total_seconds()
                    lastTime = nowTime
                    # robot.rotar180(segundosTrascurridos)
                    
                    print('indicar que ya tiene un objeto')
                    recogioObject = True

        elif recogioObject:
            print('retornar')
            print('Abrir pinzas')
            print('retroceder unos cm')
            print('dar giro de 180 grados')
            print('Indicar que ')            
            recogioObject = False
            print('====lista de movimineto===')
            for i in robot.movimientos:
                print(i)
            signal.pause()


        cv2.imshow("Camara", frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    
    # variables de entorno
    DIR_CAMERA = config('DIR_CAMERA')   # http://192.168.1.2:4747/video
    portSerial = config('USER_SERIAL')  # COM3

    robot = Robot(portSerial)
    model_ai = Model_AI()

    menu = """Seleccion el escenario
    1 - forma
    2 - color
    3 - forma y color
    """ 
    
    print(menu)
    n = int(input())

    if n == 1:
        mensaje = """Escoja la forma
        1 - TETRAEDRO
        2 - ESFERA
        3 - CUBO"""
        print(mensaje)
        n2 = int(input())
        COLOR = None
        if n == 1:
            FIGURE =  "tetraedro"
        elif n==2:
            FIGURE =  "esfera"
        elif n==3:
            FIGURE =  "cubo"
        else:
            print('opcion invalida')
            sys.exit(1)
       
        modelo_callback = model_ai.search_by_figure
        searchPatronRobot(robot, DIR_CAMERA, modelo_callback,  FIGURE, COLOR )
    
   
    elif n==2:
        mensaje = """Escoja el color
        1 - ROJO
        2 - AZUL
        3 - VERDE"""
        print(mensaje)
        n2 = int(input())
        FIGURE = None
        if n2 == 1:
            COLOR =  "red"
        elif n2==2:
            COLOR =  "blue"
        elif n2==3:
            COLOR =  "green"
        else:
            print('opcion invalida')
            sys.exit(1)
        modelo_callback = model_ai.search_by_color
        searchPatronRobot(robot, DIR_CAMERA, modelo_callback,  FIGURE, COLOR )

    elif n==3:
        mensaje = """Escoja la forma
        1 - TETRAEDRO
        2 - ESFERA
        3 - CUBO"""
        print(mensaje)
        n2 = int(input())
        if n2 == '1':
            FIGURE =  "tetraedro"
        elif n2=='2':
            FIGURE =  "esfera"
        elif n2=='3':
            FIGURE =  "cubo"
        else:
            print('opcion invalida')
            sys.exit(1)
        mensaje = """Escoja el color
        1 - ROJO
        2 - AZUL
        3 - VERDE"""
        print(mensaje)
        n2 = int(input())
        if n2 == 1:
            COLOR =  "red"
        elif n2==2:
            COLOR =  "blue"
        elif n2==3:
            COLOR =  "green"
        else:
            print('opcion invalida')
            sys.exit(1)
        
        modelo_callback = model_ai.serch_by_color_and_fig
        searchPatronRobot(robot, DIR_CAMERA, modelo_callback,  FIGURE, COLOR )
    else:
        print('opcion invalida')
        sys.exit(1)

