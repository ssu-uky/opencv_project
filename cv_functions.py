from django.conf import settings
import numpy as np
import cv2  # python-opencv


def cv_detect_face(path):  # path parameter를 통해 파일 경로 받음
    img = cv2.imread(path, 1)  # 경로가 잘못 되었다면 파일이 읽어지지 않음 // == type : None으로 나옴

    if type(img) is np.ndarray:
        print(img.shape)  # 세로, 가로, 채널

        # Haar-based Cascade Classifier : AdaBoost 기반 머신러닝 물체 인식 모델
        # 이미지에서 눈, 얼굴 등의 부위를 찾는데 주로 이용

        # 이미 학습된 모델을 OpenCV 에서 제공 (http://j.mp/2qIxrxX)
        baseUrl = settings.MEDIA_ROOT_URL + settings.MEDIA_URL

        face_cascade = cv2.CascadeClassifier(
            baseUrl + "haarcascade_frontalface_default.xml"
        )
        eye_cascade = cv2.CascadeClassifier(baseUrl + "haarcascade_eye.xml")

        # 굳이 컬러이미지를 사용해야하는 상황이 아니라면, 컬러이미지를 흑백으로 만든 후 모델 트레이닝 하고, 모델 예측할때에도 흑백이미지로 예측하게끔하기
        # 컬러이미지를 흑백이미지로 변경하면 이미지의 채널이 3개에서 1개로 줄어들게 되어 모델학습도가 빨라짐
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # detectMultiScale(Original img, ScaleFactor, minNeighbor) : further info. @ http://j.mp/2SxjtKR
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)  # 각각의 얼굴에 있는 좌표들을 리스트로 내어줌
        # cvlib -> detect_face => 특정한 함수가 내어 놓은 것은 얼굴의 좌표들 & 예측확률을 줌

        for x, y, w, h in faces:  # x: y: w:너비 h:높이
            cv2.rectangle(
                img, (x, y), (x + w, y + h), (255, 0, 0), 2
            )  # 이미지 원본 위에 픽셀 기준으로 사각형을 그림
            roi_gray = gray[y : y + h, x : x + w]
            roi_color = img[y : y + h, x : x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for ex, ey, ew, eh in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        cv2.imwrite(path, img)

    else:
        print("Error occurred within cv_detect_face!")
        print(path)
