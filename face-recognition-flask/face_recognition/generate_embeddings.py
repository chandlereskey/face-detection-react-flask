import cv2
import numpy
import numpy as np
from imgbeddings import imgbeddings
from PIL import Image
import os

haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def generate_embeddings(images):

    embeddings = []
    ibed = imgbeddings()

    for i in range(len(images)):
        pil_img = Image.open(images[f'images{i}']).convert('RGB')  # load with Pillow
        img = numpy.array(pil_img)

        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        face = haar_cascade.detectMultiScale(
            gray_img, scaleFactor=1.05, minNeighbors=1, minSize=(100, 100)
        )
        if len(face) > 0:
            x, y, w, h = face[0][0], face[0][1], face[0][2], face[0][3]
            cropped_img = img[y: y+h, x: x+w]

            face_img = Image.fromarray(cropped_img.astype('uint8'))

            embedding = ibed.to_embeddings(face_img)
            print(np.array(embedding[0].tolist()).reshape(1, -1).shape)
            embeddings.append(embedding[0].tolist())

    file = open('embeddings.txt', 'w+')

    file.write(str(embeddings))
    file.close()