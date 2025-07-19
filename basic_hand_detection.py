import cv2
import mediapipe as mp
import time


def main():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        exit()

    window_width = 600
    window_height = 600

    # cv2.namedWindow("Webcam Feed", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("Webcam Feed", window_width, window_height)

    # cv2.namedWindow("Webcam Feed", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("Webcam Feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    mpHands = mp.solutions.hands
    hands=mpHands.Hands()

    mpDraw=mp.solutions.drawing_utils

    pTime=0
    cTime=0


    while True:

        success, img = cap.read()
        if not success:
            print("Error: Failed to capture image.")
            break

        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        detected_hands = hands.process(rgb_img)

        if detected_hands.multi_hand_landmarks:
            for handLms in detected_hands.multi_hand_landmarks:

                for id,lm in enumerate(handLms.landmark):

                    h,w,c = img.shape
                    cx,cy = int(lm.x*w), int(lm.y*h)

                    print(id, cx, cy)

                    # cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        if fps > 30:
            color = (0, 255, 0)
        elif fps > 15:
            color = (0, 255, 255)
        else:
            color = (0, 0, 255)

        # cv2.putText(img, str(int(fps)), (10, 70),
        #     cv2.FONT_HERSHEY_PLAIN, 3,
        #     color, 3 )

        cv2.namedWindow("Webcam Feed", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Webcam Feed", window_width, window_height)

        # cv2.namedWindow("Webcam Feed", cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty("Webcam Feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        cv2.imshow("Webcam Feed", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()