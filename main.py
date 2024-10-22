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


def count_fingers(lmlist):
    tipids = [4, 8, 12, 16, 20]
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

    return fingerlist.count(1)


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = hands.process(imgrgb)

    lmlist = []

    cv2.rectangle(img, (20, 350), (250, 440), (0, 255, 204), cv2.FILLED)
    cv2.rectangle(img, (20, 350), (250, 440), (0, 0, 0), 5)

    if res.multi_hand_landmarks:
        for handlms in res.multi_hand_landmarks:

            for id, lm in enumerate(handlms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])

            if len(lmlist) == 21:

                finger_count = count_fingers(lmlist)

                cv2.putText(
                    img,
                    f"Fingers: {finger_count}",
                    (25, 410),
                    cv2.FONT_HERSHEY_PLAIN,
                    2,
                    (0, 0, 0),
                    2,
                )

                if finger_count == 5:
                    controller.control("ON")
                elif finger_count == 0:
                    controller.control("OFF")
                else:
                    controller.control(f"Speed {finger_count}")

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
