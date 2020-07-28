import cv2
import numpy as np

from project.controller.ai_controller import *

def get_frame(img, center):
    """
    Extrae un fragmento de una imagen mas grande
    """
    y1, x1 = (center - [150, 250])
    y2, x2 = (center + [150, 250])
    frame = img[y1: y2, x1 * int(x1 >= 0 ): x2]
    if x1 < 0:
        x1 = img.shape[1] + x1
        x2 = img.shape[1]
        frame = np.concatenate([img[y1: y2, x1: x2], frame], axis=1)
    elif x2 >= img.shape[1]:
        x1 = 0
        x2 = x1 + abs(img.shape[1] - x2)
        frame = np.concatenate([frame, img[y1: y2, x1: x2]], axis=1)
    frame = frame.copy()
    return frame


def escenario():
    font = cv2.FONT_HERSHEY_SIMPLEX
    model_ai = Model_AI()
    img = cv2.imread("media/Muestra.png")

    #out = cv2.VideoWriter('muestra.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (500,300))

    active = True
    #cap = cv2.VideoCapture()
    #active = cap.open("http://198.164.0.1:4040/video") #Ip cam
    mira = 0
    direction = -1
    color=None
    while active:
        center = np.int32([img.shape[0]//2, mira])
        frame = get_frame(img, center)
        #frame = cap.read()

        # la funcion que devuelve la direccion de giro , el color detectado y la figura
        color, new_dir, figura = model_ai.analyze_image(frame) # <- -1, 0 1 ->
        if color is not None:
            mask = color_filter(frame, color)
            contours = find_contours(mask)
            cv2.drawContours(frame, contours, -1, color, 2)
            locations = get_locations(contours)
            direction = new_dir
            for loc in locations:
                cx, cy = loc
                cv2.circle(frame,(cx, cy), 3, (0,255,255), -1)
                cv2.putText(frame,"(x: " + str(cx) + ", y: " + str(cy) + ")",(cx+10,cy+10), font, 0.5,(255,255,255),1)
        
        cv2.imshow("Camara", frame)
        #if (mira % 5 == 0):
        #    out.write(frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break
        mira += direction
        if mira >= img.shape[1]:
            mira = 0
        elif mira < 0:
            mira = img.shape[1] -1 

def camara():
    model_ai = Model_AI()
    font = cv2.FONT_HERSHEY_SIMPLEX
    cap = cv2.VideoCapture()
    active = cap.open("http://192.168.100.64:8080/videofeed")
    while active:
        active, frame = cap.read()
        print(frame.shape)
        color, direccion, __ = model_ai.analyze_image(frame)
        if color is not None:
            mask = color_filter(frame, color)
            contours = find_contours(mask)
            cv2.drawContours(frame, contours, -1, color, 2)
            locations = get_locations(contours)
            for loc in locations:
                cx, cy = loc
                cv2.circle(frame,(cx, cy), 3, (0,255,255), -1)
                #Escribimos las coordenadas del centro
                cv2.putText(frame,"(x: " + str(cx) + ", y: " + str(cy) + ")",(cx+10,cy+10), font, 0.5,(255,255,255),1)

            cv2.imshow("mask", mask)
            cv2.imshow("Camara", frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    #escenario()
    camara()