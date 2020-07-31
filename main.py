import cv2
import numpy as np
from project.controller.connection.robot import Robot
from project.controller.ai_controller import *


def buscarPorFiguraColor(figure, color, dir_camera):
    model_ai = Model_AI()
    cap = cv2.VideoCapture()
    active = cap.open(dir_camera)
    # robot = Robot()    
    while active:
        active, frame = cap.read()
        located, new_dir = model_ai.serch_by_color_and_figure(frame, figure, color)
        if located:
            print(new_dir)
            if new_dir == -1:
                pass
                # robot.izquierda()
            elif new_dir == 1:
                pass
                # robot.derecha()
            else:
                pass
                # robot.detener()

        cv2.imshow("Camara", frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break



def buscarPorFigura(figure, dir_camera):
    model_ai = Model_AI()
    cap = cv2.VideoCapture()
    active = cap.open(dir_camera)
    # robot = Robot()    
    while active:
        active, frame = cap.read()
        located, new_dir =  model_ai.search_by_figure(frame, figure)
        if located:
            print(new_dir)
            if new_dir == -1:
                pass
                # robot.izquierda()
            elif new_dir == 1:
                pass
                # robot.derecha()
            else:
                pass
                # robot.detener()

        cv2.imshow("Camara", frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

def buscarPorColor(color, dir_camera):
    model_ai = Model_AI()
    cap = cv2.VideoCapture()
    active = cap.open(dir_camera)
    # robot = Robot()    
    while active:
        active, frame = cap.read()
        located, new_dir =  model_ai.search_by_color(frame, color)
        if located:
            print(new_dir)
            if new_dir == -1:
                pass
                # robot.izquierda()
            elif new_dir == 1:
                pass
                # robot.derecha()
            else:
                pass
                # robot.detener()

        cv2.imshow("Camara", frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    
    # variables para buscar
    # entrada de la camara
    #DIR_CAMERA = "http://192.168.1.2:4747/video"
    DIR_CAMERA = "media/video_prueba1.mp4"
    
    #COLOR = 'blue'
    COLOR = 'red'
    #COLOR = 'green'
    FIGURE =  "cubo"
    #FIGURE =  "tetraedro"
    #FIGURE =  "esfera"
    
    
    # escenarios

    buscarPorFiguraColor(FIGURE, COLOR, DIR_CAMERA )
    # buscarPorFigura(FIGURE,  DIR_CAMERA )
    # buscarPorColor(COLOR, DIR_CAMERA )
    