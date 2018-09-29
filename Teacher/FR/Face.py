import cv2
import numpy as np
import os
from django.conf import settings
from Teacher.models import Student

class Train:
    path = settings.BASE_DIR + "/media/"

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    full_path = "/home/jenish/Documents/FaceRecognition/media/training-data"

    def __init__(self,room):
        self.subjects = [""]

        #self.cam = cv2.VideoCapture(2)
        data = Student.objects.all()
        for obj in data:
            spath = self.full_path + "/" + obj.image_path
            index = spath.split('/')[7].replace('s', '')
            roll_no = obj.roll_no
            self.subjects.insert(int(index), roll_no)
        print(self.subjects)


    def detect_face(self,img):
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray,scaleFactor = 1.2,minNeighbors = 5)

        if len(faces)==0:
            return None,None

        (x,y,w,h) = faces[0]
        return gray[y:y+w,x:x+h],faces[0]

    def prepare_training_data(self,data_folder_path):
        dirs = os.listdir(data_folder_path)

        faces = []
        labels = []

        for dir_name in dirs:
            if not dir_name.startswith('s'):
                continue
            label = int(dir_name.replace("s",""))

            #folder-path to media
            subject_dir_path = data_folder_path + "/" + dir_name

            subject_images_names = os.listdir(subject_dir_path)

            for image_name in subject_images_names:
                if image_name.startswith("."):
                    continue
                image_path = subject_dir_path + "/" + image_name

                image = cv2.imread(image_path)

                face,rect = self.detect_face(image)

                if face is not None:
                    faces.append(face)
                    labels.append(label)

        cv2.destroyAllWindows()

        return faces,labels

    def train_algorithm(self):
        faces, labels = self.prepare_training_data(self.path + "training-data")
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_recognizer.train(faces, np.array(labels))
        face_recognizer.save('faceRecognizers.xml')


    def predict2(self,test_img):
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        if os.path.isfile('faceRecognizers.xml'):
            face_recognizer.read('faceRecognizers.xml')
            image = cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)
            user,confidence = face_recognizer.predict(image)
            if confidence <100:
                print("u = ",user,confidence)
                print(self.subjects[user])
                return user
            else:
                print("unkonw")


    def showVideo(self):
        attended_student = []
        self.cam = cv2.VideoCapture(2)
        while 1:

            ret,frame = self.cam.read()
            if not frame is None:
                if not ret : continue
            faces = self.face_cascade.detectMultiScale(frame, scaleFactor=1.2,minNeighbors=7,minSize=(100,100))
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
                roi = frame[y:y+h,x:x+h]
            cv2.namedWindow('', flags=cv2.WINDOW_AUTOSIZE)
            cv2.imshow("",frame)

            k = cv2.waitKey(1)

            if k %256 ==27:#if esc pressed
                return attended_student

            elif k%256 ==32:
                if len(faces) ==0:#if space is pressed
                    continue
                label= self.predict2(roi)
                if label is None:
                    continue
                attended_student.append(self.subjects[label])
        cv2.destroyAllWindows()



