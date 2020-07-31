from decouple import config
import cv2
import numpy as np
from project.controller.robot import Robot
from project.controller.ai_controller import *
import signal
import datetime



# def buscarPorFiguraColor(figure, color, dir_camera):
#     model_ai = Model_AI()
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

def buscarPorColor(robot, color, dir_camera):
    model_ai = Model_AI()
    cap = cv2.VideoCapture()
    active = cap.open(dir_camera)
    recogioObject = False
    lastTime = datetime.datetime.now()
    robot.grabando = True
    ultimoMovimiento = robot.ultimoMovimiento
    while active:
        active, frame = cap.read()
        located, new_dir =  model_ai.search_by_color(frame, color)
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
    
    # variables para buscar
    # entrada de la camara
    DIR_CAMERA = config('DIR_CAMERA')
    portSerial = config('USER_SERIAL')
    robot = Robot(portSerial) 

    #COLOR = 'blue'
    COLOR = 'red'
    #COLOR = 'green'
    FIGURE =  "cubo"
    #FIGURE =  "tetraedro"
    #FIGURE =  "esfera"
    
    
    # escenarios

    # buscarPorFiguraColor(FIGURE, COLOR, DIR_CAMERA )
    # buscarPorFigura(FIGURE,  DIR_CAMERA )
    buscarPorColor(robot, COLOR, DIR_CAMERA )
    