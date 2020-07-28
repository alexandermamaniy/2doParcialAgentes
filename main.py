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

def display_analysis(frame, model_ai, color:str):
    font = cv2.FONT_HERSHEY_SIMPLEX
    encoded_color = model_ai.encode_color(color)
    mask = color_filter(frame, encoded_color)
    contours = find_contours(mask)
    cv2.drawContours(frame, contours, -1, [255,0,0], 2)
    locations = get_locations(contours)
    if locations.any():
         # actualizando de direccion
        for loc in locations:
            cx, cy = loc
            cv2.circle(frame,(cx, cy), 3, (0,255,255), -1)
            cv2.putText(frame,"(x: " + str(cx) + ", y: " + str(cy) + ")",(cx+10,cy+10), font, 0.5,(255,255,255),1)
        

def escenario():
    model_ai = Model_AI()
    img = cv2.imread("media/Muestra.png")

    active = True
    mira = 0
    direction = -1
    color='blue'
    while active:
        center = np.int32([img.shape[0]//2, mira])
        frame = get_frame(img, center)

        # la funcion que devuelve la direccion de giro , el color detectado y la figura
        located, new_dir = model_ai.search_by_color(frame, color) # <- -1, 0 1 ->
        if located:
            direction = new_dir

        display_analysis(frame, model_ai, color)

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
    cap = cv2.VideoCapture()
    active = cap.open("http://192.168.100.64:8080/videofeed")

    color = 'red'

    while active:
        active, frame = cap.read()
        located, new_dir = model_ai.search_by_color(frame, color)

        if located:
            print(new_dir)

        display_analysis(frame, model_ai, color)

        cv2.imshow("Camara", frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    #escenario()
    camara()