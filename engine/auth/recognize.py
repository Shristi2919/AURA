import time
import cv2
import pyautogui as p
import os                                                                                   



def AuthenticateFace():

    flag = 0

    BASE = os.path.dirname(os.path.abspath(__file__))

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(os.path.join(BASE, 'trainer', 'trainer.yml'))

    faceCascade = cv2.CascadeClassifier(
        os.path.join(BASE, 'haarcascade_frontalface_default.xml')
    )

    font = cv2.FONT_HERSHEY_SIMPLEX
    names = ['', 'Shristi', 'Disha', 'Ipsita', 'Anjali', 'Kanya']

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)

    if not cam.isOpened():
        print("❌ Cannot access camera")
        return 0

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    print("🎥 Starting face recognition... Press ESC to exit")

    while True:
        ret, img = cam.read()

        if not ret:
            print("❌ Failed to grab frame")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            id, accuracy = recognizer.predict(gray[y:y + h, x:x + w])

            if accuracy < 100:
                name = names[id] if id < len(names) else "Unknown"
                confidence = f"{round(100 - accuracy)}%"
                flag = 1
            else:
                name = "Unknown"
                confidence = f"{round(100 - accuracy)}%"
                flag = 0

            cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('Face Recognition', img)

        key = cv2.waitKey(10) & 0xFF
        if key == 27:
            break

        if flag == 1:
            break

    cam.release()
    cv2.destroyAllWindows()

    return flag