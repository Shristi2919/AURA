import time
import cv2
import pyautogui as p


def AuthenticateFace():

    flag = 0  # 0 = not recognized, 1 = recognized

    # Load recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('engine\\auth\\trainer\\trainer.yml')

    # Load Haar Cascade
    cascadePath = "engine\\auth\\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX

    # Names list (index must match ID used during training)
    names = ['', 'Shristi', 'Disha', 'Ipsita', 'Anjali', 'Kanya']

    # Start camera
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)

    if not cam.isOpened():
        print("❌ Cannot access camera")
        return 0

    # Define min window size
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

            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            id, accuracy = recognizer.predict(gray[y:y+h, x:x+w])

            # If confidence is good
            if accuracy < 100:
                name = names[id] if id < len(names) else "Unknown"
                confidence = f"{round(100 - accuracy)}%"
                flag = 1
            else:
                name = "Unknown"
                confidence = f"{round(100 - accuracy)}%"
                flag = 0

            cv2.putText(img, str(name), (x+5, y-5),
                        font, 1, (255, 255, 255), 2)

            cv2.putText(img, str(confidence), (x+5, y+h-5),
                        font, 1, (255, 255, 0), 1)

        cv2.imshow('Face Recognition', img)

        key = cv2.waitKey(10) & 0xff

        if key == 27:  # ESC key
            break

        # Optional: auto-exit when recognized
        if flag == 1:
             break

    # Cleanup
    cam.release()
    cv2.destroyAllWindows()

    return flag


# ✅ IMPORTANT: call function
#if __name__ == "__main__":
 #   result = AuthenticateFace()

  #  if result == 1:
   #     print("✅ Face recognized successfully")
    #else:
     #   print("❌ Face not recognized")