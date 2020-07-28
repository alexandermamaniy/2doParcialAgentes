import cv2
import numpy as np
from project.controller.connection.robot import Robot
from project.controller.ai_controller import *

def display_analysis(frame, model_ai, color:str):
    font = cv2.FONT_HERSHEY_SIMPLEX
    encoded_color = model_ai.encode_color(color)
    mask = color_filter(frame, encoded_color)
    contours = find_contours(mask)
    cv2.drawContours(frame, contours, -1, [255,0,0], 2)
    locations = get_locations(contours)
    if locations.any():
         # actualizando de direccion
        for loc, c in zip(locations,contours):
            figure = find_figure(c)
            cx, cy = loc
            cv2.circle(frame,(cx, cy), 3, (0,255,255), -1)
            cv2.putText(frame,"(x: " + str(cx) + ", y: " + str(cy) + ")",(cx+10,cy+10), font, 0.5,(255,255,255),1)
            cv2.putText(frame, figure , (cx,cy-5),font,1,(0,255,0),1)

def buscarPorFiguraColor(figure, color, dir_camera):
    model_ai = Model_AI()
    cap = cv2.VideoCapture()
    active = cap.open(dir_camera)
    robot = Robot()    
    while active:
        active, frame = cap.read()
        located, new_dir = model_ai.serch_by_color_and_figure(frame, figure, color)
        if located:
            if new_dir == -1:
                robot.izquierda()
            elif new_dir == 1:
                robot.derecha()
            else:
                robot.detener()

        display_analysis(frame, model_ai, color)

        cv2.imshow("Camara", frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break



def buscarPorFigura(figure, dir_camera):
    model_ai = Model_AI()
    cap = cv2.VideoCapture()
    active = cap.open(dir_camera)
    robot = Robot()    
    while active:
        active, frame = cap.read()
        located, new_dir =  model_ai.search_by_figure(frame, figure)
        if located:
            if new_dir == -1:
                robot.izquierda()
            elif new_dir == 1:
                robot.derecha()
            else:
                robot.detener()

        display_analysis(frame, model_ai, 'WHITE')

        cv2.imshow("Camara", frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

def buscarPorColor(color, dir_camera):
    model_ai = Model_AI()
    cap = cv2.VideoCapture()
    active = cap.open(dir_camera)
    robot = Robot()    
    while active:
        active, frame = cap.read()
        located, new_dir =  model_ai.search_by_color(frame, color)
        if located:
            if new_dir == -1:
                robot.izquierda()
            elif new_dir == 1:
                robot.derecha()
            else:
                robot.detener()

        display_analysis(frame, model_ai, color)

        cv2.imshow("Camara", frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    
    # variables para buscar
    # entrada de la camara
    DIR_CAMERA = "http://192.168.100.83:8080/videofeed"
    
    #COLOR = 'blue'
    #COLOR = 'red'
    COLOR = 'green'
    #FIGURE =  "cubo"
    #FIGURE =  "tetraedro"
    FIGURE =  "esfera"
    
    
    # escenarios

    #buscarPorFiguraColor(FIGURE, COLOR, DIR_CAMERA )
    #buscarPorFigura(FIGURE,  DIR_CAMERA )
    buscarPorColor(COLOR, DIR_CAMERA )
    