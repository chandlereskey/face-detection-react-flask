import ast

import cv2
import numpy as np
from PIL import Image
from imgbeddings import imgbeddings
from sklearn.metrics import pairwise_distances_argmin_min

haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


with open('embeddings.txt', 'r') as text_file:
    file_content = text_file.read()

ibed = imgbeddings()

embeddings = np.array(ast.literal_eval(file_content))
text_file.close()

def detect_faces(frame, embeddings):
    key = cv2.waitKey(20)
    if key == 27:
        return None
    faces = haar_cascade.detectMultiScale(
        frame, scaleFactor=1.05, minNeighbors=1, minSize=(100, 100)
    )
    for x, y, w, h in faces:
        cropped_img = frame[y: y + h, x: x + w]
        face_img = Image.fromarray(cropped_img.astype('uint8'))

        embedding = np.array(ibed.to_embeddings(face_img)).reshape(1, -1)
        arg_min, distances = pairwise_distances_argmin_min(embedding, embeddings)
        if distances[0] <= 11:
            cv2.putText(frame, 'Chandler', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), )
        else:
            cv2.putText(frame, 'not chandler', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), )
    return frame
