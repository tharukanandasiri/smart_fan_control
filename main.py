import cv2
import mediapipe as mp
import time
import controller


class HandPoses:
    def __init__(self):

        self.tip_ids = [4, 8, 12, 16, 20]

    def count_fingers(self, lmlist, is_right_hand):

        finger_count = 0

        if is_right_hand:
            if lmlist[self.tip_ids[0]][1] < lmlist[self.tip_ids[0] - 1][1]:
                finger_count += 1
        else:
            if lmlist[self.tip_ids[0]][1] > lmlist[self.tip_ids[0] - 1][1]:
                finger_count += 1

        for i in range(1, 5):
            if lmlist[self.tip_ids[i]][2] < lmlist[self.tip_ids[i] - 2][2]:
                finger_count += 1

        return finger_count

    def control_action(self, finger_count):

        if finger_count == 5:
            return "ON"
        elif finger_count == 0:
            return "OFF"

        elif finger_count == 4:
            return ""
        else:
            return f"Speed {finger_count}"


ctime = 0
ptime = 0


cap = cv2.VideoCapture(0)


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
draw = mp.solutions.drawing_utils


hand_poses = HandPoses()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = hands.process(imgrgb)

    lmlist = []

    cv2.rectangle(img, (20, 350), (250, 440), (0, 255, 204), cv2.FILLED)
    cv2.rectangle(img, (20, 350), (250, 440), (0, 0, 0), 5)

    if res.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(res.multi_hand_landmarks):

            hand_label = res.multi_handedness[idx].classification[0].label
            is_right_hand = hand_label == "Right"

            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])

            if len(lmlist) >= 21:

                finger_count = hand_poses.count_fingers(lmlist, is_right_hand)

                cv2.putText(
                    img,
                    f"Fingers: {finger_count}",
                    (25, 410),
                    cv2.FONT_HERSHEY_PLAIN,
                    2,
                    (0, 0, 0),
                    2,
                )

                control_action = hand_poses.control_action(finger_count)

                cv2.putText(
                    img,
                    control_action,
                    (25, 450),
                    cv2.FONT_HERSHEY_PLAIN,
                    2,
                    (0, 0, 0),
                    2,
                )

                controller.control(control_action)

            draw.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
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
