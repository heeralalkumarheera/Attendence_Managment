#importing computervision to perform the actions like detecting the faces and handles face recognition process. 
import cv2
#importing built in operating system in python. 
import os
#importing numpy library to perform the numerical operations store and manipulate the image data.
import numpy as np
#importing image from the pillow library which specifically used to convert the images to greyscale. 
from PIL import Image
from config import CASCADE_PATH, MODEL_PATH, TRAINING_DIR

#LBPHFaceRecognizer_create() LBPH is a alogorithm (Local Binary Patterns Histogram) is method used for face recognition which is located in face package of opencv library.
recognizer = cv2.face.LBPHFaceRecognizer_create()
#CascadeClassifier is used for real object detection.
detector = cv2.CascadeClassifier(str(CASCADE_PATH))

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faceSamples = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image

        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces = detector.detectMultiScale(imageNp)
        # If a face is there then append that in the list as well as Id of it
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y+h, x:x+w])
            Ids.append(Id)
    return faceSamples, Ids


faces, Ids = getImagesAndLabels(str(TRAINING_DIR))
recognizer.train(faces, np.array(Ids))
recognizer.save(str(MODEL_PATH))