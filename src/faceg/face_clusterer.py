import cv2 as cv
import face_recognition
import numpy as np
from sklearn.cluster import DBSCAN


class faceClusterer():
    def __init__(self, images, detection_model='hog'):
        self.images = images
        self.detection_model = detection_model


    def get_encodings(self):
        encodings = []
        for image in self.images:
            img = cv.imread(image)
            rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            faces = face_recognition.face_locations(rgb, model=self.detection_model)
            ecds = face_recognition.face_encodings(rgb, faces)

            for ecd in ecds:
                encodings.append((image, ecd))
        
        return np.array(encodings, dtype='object')
        

    def cluster_faces(self):
        encodings = self.get_encodings()
        ecds = [e[1] for e in encodings]
        clt = DBSCAN(metric="euclidean", n_jobs=-1)
        clt.fit(ecds)

        labeled_imgs = []

        for i, lbl in enumerate(clt.labels_):
            labeled_imgs.append((encodings[i][0], lbl))

        return labeled_imgs