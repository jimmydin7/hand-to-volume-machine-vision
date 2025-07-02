import cv2
import mediapipe as mp
from pathlib import Path
from utils.logs import logs as lg
from utils.volume import controler as vc

lg.logInfo("Initializing MediaPipe...")
lg.logInfo("Loading human frontal face classifier...")
face_cascade = Path("./models") / "human" / "hc-frontalface.xml"
clsf = cv2.CascadeClassifier(str(face_cascade))

def draw_text(img, text, position=(10, 30), font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(255, 0, 0), thickness=2):
    cv2.putText(img, text, position, font, font_scale, color, thickness)

cap = cv2.VideoCapture(0)
lg.logInfo("Initialized Video Capture 0")


mphands = mp.solutions.hands
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils

while True:
    _, img = cap.read()
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgrgb)

    faces = clsf.detectMultiScale(imgrgb, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    
    for (x, y, w, h) in faces:
        #lg.logInfo(f'Face Detected ({x,y,w,h})')
        cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(img, f'Human', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        

    if results.multi_hand_landmarks:
        #lg.logInfo("Hand Detected!")

        try:

            setzero = False
            thumb_tip = handLms.landmark[4]
            index_tip = handLms.landmark[8]

            x = thumb_tip.y
            y = index_tip.y

            dist = abs(y-x)
            
            minval = 0.1
            maxval = 0.5

            perc = (dist / maxval)

            if perc < minval:
                vc.set_volume(0)
                full = 0
                setzero = True

            if setzero:
                full = 0
            else:
                full = perc * 100
                full = round(full, 1)

                maxfull = pow(10, 2) # = 100
                if full > maxfull:
                    full = maxfull

            draw_text(img, f'Volume: {full}%', position=(10, 30))

            cv2.line(img, (int(thumb_tip.x * img.shape[1]), int(thumb_tip.y * img.shape[0])), (int(index_tip.x * img.shape[1]), int(index_tip.y * img.shape[0])), (0, 255, 0), 2)
            if not setzero:
                currentVolume = vc.get_current_volume()
                if currentVolume != perc:
                    vc.set_volume(perc) 
            
        except Exception as e:
            lg.logError(e)
            #raise 
            
        # draw with cv2 on hand landmarks
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
            mpdraw.draw_landmarks(img, handLms, mphands.HAND_CONNECTIONS)

            

    cv2.namedWindow("Video Feed", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Video Feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Video Feed", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        lg.logError("Closing Video Capture... - BREAK!")
        break

cap.release()

cv2.destroyAllWindows()
