from decouple import config
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

#         display_analysis(frame, model_ai, color)

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

#         display_analysis(frame, model_ai )

#         cv2.imshow("Camara", frame)
#         if cv2.waitKey(1) == ord('q'):
#             cv2.destroyAllWindows()
#             break

def buscarPorColor(robot, color, dir_camera):
    model_ai = Model_AI()
    cap = cv2.VideoCapture()
    active = cap.open(dir_camera)
    recogioObject = False
    while active:
        active, frame = cap.read()
        located, new_dir =  model_ai.search_by_color(frame, color)
        if located and not recogioObject :
            print(new_dir, robot.dataSensorUltraSonic)
            distancia = robot.dataSensorUltraSonicyu{}
            if new_dir == -1 and  distancia >= 10:
                print('se detiene')
                print('va Izquierda')
                print('se detiene')
                # robot.izquierda()
            elif new_dir == 1 and  distancia >= 10 :
                print('se detiene')
                print('va derecha')
                print('se detiene')
                # robot.derecha()
            elif new_dir == 0 and  distancia >= 5  :
                print('se detiene')
                print('avanza hacia delante')
                print('se detiene')
            elif new_dir == 0 and  (distancia == 4 or distancia == 4)  :
                print('se detiene')
                if new_dir == 0 and  (distancia >= 2 or   distancia <= 3)   :
                    print('cerrar pinza')
                    print('Dar vuelta de 180 grados')
                    print('indicar que ya tiene un objeto')
                    recogioObject = True
        elif recogioObject:
            print('retornar')
            print('Abrir pinzas')
            print('retroceder unos cm')
            print('dar giro de 180 grados')
            print('Indicar que ')            
            recogioObject = False
                
        display_analysis(frame, model_ai, color)

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
    #COLOR = 'red'
    COLOR = 'green'
    #FIGURE =  "cubo"
    #FIGURE =  "tetraedro"
    FIGURE =  "esfera"
    
    
    # escenarios

    # buscarPorFiguraColor(FIGURE, COLOR, DIR_CAMERA )
    # buscarPorFigura(FIGURE,  DIR_CAMERA )
    buscarPorColor(robot, COLOR, DIR_CAMERA )
    