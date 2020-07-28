import cv2
import numpy as np

UMBRAL = 60

class Model_AI():
    def __init__(self):
        self.min_distance = UMBRAL
        self.color_detected = False
        self.current_direction = 0
        self.current_color = None
    
    def search_by_color(self, img, color):
        located = False
        mask = color_filter(img, self.current_color)
        contours = find_contours(mask)
        locations = get_locations(contours)
        center = np.int32(np.array(img.shape[:2]) // 2)
        if locations is not None:
            distances = np.linalg.norm(locations - np.array(list(reversed(center))), axis=1)
            min_index = np.argmin(distances)
            if distances.min() < UMBRAL:
                self.current_direction = int(self.min_distance > distances.min()) * self.current_direction
                self.min_distance = distances.min()
                located = self.current_direction == 0
            else:
                vector = locations[min_index] - np.array(list(reversed(center)))
                vector = vector / (np.abs(vector).sum() * 0.5)
                vector = np.tanh(vector)
                self.current_direction = int(round(vector[0]))
        return located, self.current_direction

    def analyze_image(self, img, color=None):
        """
        Aqué se analiza una imagen, recibe como argumentos.

        Args:
        - img: una imagen representada en una matris de forma (h, w, chanels)
        - color: (opcional) el color especifico que se quiere detectar

        Returns:
        - color, un array de tres valores [B, G, R], si no detecto nada el varlor sera None
        - direccion, Un numero entero entre -1 a 1,  izq = -1, der = 1, centrado = 0
        """
        if color is None and not self.color_detected:
            color, self.current_direction = detect_color(img)
            if color is not None:
                self.current_color = color
                self.color_detected = True
        elif not self.color_detected and color is not None:
            self.current_color = color
            self.color_detected = True

        if self.current_color is not None:
            mask = color_filter(img, self.current_color)
            contours = find_contours(mask)
            locations = get_locations(contours)
            center = np.int32(np.array(img.shape[:2]) // 2)
            distances = np.linalg.norm(locations - np.array(list(reversed(center))), axis=1)
            min_index = np.argmin(distances)
            if distances.min() < UMBRAL:
                self.current_direction = int(self.min_distance > distances.min()) * self.current_direction
                self.min_distance = distances.min()
                if self.current_direction == 0:
                    self.color_detected = False
                    self.current_color = None
                    self.min_distance = UMBRAL
                    self.current_direction = 0
            elif distances.min() >= UMBRAL:
                vector = locations[min_index] - np.array(list(reversed(center)))
                vector = vector / (np.abs(vector).sum() * 0.5)
                vector = np.tanh(vector)
                self.current_direction = int(round(vector[0]))
        return self.current_color, self.current_direction


def color_filter(img, color):
    """
    Metes una imagen y el color que quieres detectar [255,0,0]->Azul, [0,255,0]->Verde, [0,0,255] -> azul
    
    Return: una imagen con las mismas dimenciones a la original pero solo con siluetas blancas
    """
    c3, c2, c1 = max_color(color)
    mask = (img[:,:,c1] > img[:,:,c2]) * (img[:,:,c1] > img[:,:,c3])
    mask = mask * (img[:,:,c1] - img[:,:,c2]) > 10
    mask = mask * 255
    mask = np.uint8(mask)
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel, iterations = 4)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
    mask = cv2.dilate(mask,kernel,iterations=3)
    dist_transform = cv2.distanceTransform(mask,cv2.DIST_L2,5)
    _, mask = cv2.threshold(dist_transform,0.4*dist_transform.max(),255,0)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    return mask

def find_contours(mask):
    mask = np.uint8(mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    contours,_ = cv2.findContours(mask,1,2)
    return contours

def get_locations(contours):
    locations = None
    for i in contours:
        #Calcular el centro a partir de los momentos
        momentos = cv2.moments(i)
        if momentos['m00']:
            cx = int(momentos['m10']/momentos['m00'])
            cy = int(momentos['m01']/momentos['m00'])
        else:
            cx = int(momentos['m10'])
            cy = int(momentos['m01'])
        #Dibujar el centro
        locations.append([cx, cy])
    return np.int32(locations)

def detect_color(img):
    shape = img.shape[:2]
    left  = [[shape[0]//2-20, 20], [shape[0]//2+20, 60]]
    right = [[shape[0]//2-20, shape[1] - 60], [shape[0]//2+20, shape[1] - 20]]
    (ly1, lx1), (ly2, lx2) = left
    (ry1, rx1), (ry2, rx2) = right
    left_part    = img[ly1: ly2, lx1: lx2]
    right_part   = img[ry1: ry2, rx1: rx2]
    center_part  = img[shape[0]//2-20:shape[1]//2+20, shape[1]//2-20:shape[1]//2+20]
    left_color   = np.median(left_part, axis=(0,1))
    right_color  = np.median(right_part, axis=(0,1))
    center_color = np.median(center_part, axis=(0,1))
    #print(left_color, right_color,"   ", end="\r")
    color = None
    direction = 0
    if abs(center_color.max() - np.median(center_color)) > 40:
        color = center_color
    elif abs(left_color.max() - np.median(left_color)) > 40:
        direction = -1
        color = left_color
    elif abs(right_color.max() - np.median(right_color)) > 40:
        direction = 1
        color = right_color
    return color, direction

def max_color(color):
    color = color[:3]
    return np.argsort(color)