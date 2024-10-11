import cv2
import mediapipe as mp
import time
import controller

ctime = 0
ptime = 0

cap = cv2.VideoCapture(0)

medhands = mp.solutions.hands
hands = medhands.Hands(max_num_hands=1, min_detection_confidence=0.7)
draw = mp.solutions.drawing_utils

pose_dict = {
    (0, 1, 0, 0, 0): "Speed 1",          
    (1, 1, 0, 0, 0): "Speed 2",          
    (0, 1, 1, 0, 0): "Speed 2",          
    (1, 1, 1, 0, 0): "Speed 3",          
    (0, 1, 1, 1, 0): "Speed 3",          
    (1, 1, 1, 1, 1): "ON",               
    (0, 0, 0, 0, 0): "OFF"               
}

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = hands.process(imgrgb)

    lmlist = []
    tipids = [4, 8, 12, 16, 20]

    cv2.rectangle(img, (20, 350), (250, 440), (0, 255, 204), cv2.FILLED)
    cv2.rectangle(img, (20, 350), (250, 440), (0, 0, 0), 5)

    if res.multi_hand_landmarks:
        for handlms in res.multi_hand_landmarks:
            for id, lm in enumerate(handlms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])

            if len(lmlist) != 0 and len(lmlist) == 21:
                fingerlist = []

                
                if lmlist[9][2] < lmlist[0][2]:
                    
                    
                    if lmlist[tipids[0]][1] > lmlist[tipids[0] - 1][1]:
                        fingerlist.append(1)
                    else:
                        fingerlist.append(0)

                    
                    for id in range(1, 5):
                        if lmlist[tipids[id]][2] < lmlist[tipids[id] - 2][2]:
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)
                else:
                    
                    
                    if lmlist[tipids[0]][1] < lmlist[tipids[0] - 1][1]:
                        fingerlist.append(1)
                    else:
                        fingerlist.append(0)

                    
                    for id in range(1, 5):
                        if lmlist[tipids[id]][2] > lmlist[tipids[id] - 2][2]:
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)

                fingerpose = tuple(fingerlist)
                pose_name = pose_dict.get(fingerpose, None)

                if pose_name is not None:
                    cv2.putText(
                        img,
                        pose_name,
                        (25, 430),
                        cv2.FONT_HERSHEY_PLAIN,
                        2,
                        (0, 0, 0),
                        2,
                    )
                    controller.control(pose_name)

            draw.draw_landmarks(
                img,
                handlms,
                medhands.HAND_CONNECTIONS,
                draw.DrawingSpec(color=(0, 255, 204), thickness=2, circle_radius=2),
                draw.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=3),
            )

    
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    
    cv2.putText(
        img, f"FPS: {str(int(fps))}", (0, 12), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1
    )

    
    cv2.imshow("Hand Gestures", img)

    
    if cv2.waitKey(1) == ord("q"):
        break


controller.control("OFF")
cap.release()
cv2.destroyAllWindows()
