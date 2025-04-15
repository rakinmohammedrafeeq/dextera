import math

import cv2
import mediapipe as mp
import time
from hand_detector import handDetector
from gesture_recognition import fingers_folded, fingers_open
from gesture_recognition import is_scroll_mode
import pyautogui


def main():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        exit()

    detector = handDetector(maxHands=1)

    window_width = 1000
    window_height = 800

    cTime=0
    pTime=0

    last_click_time = 0
    clickDelay = 0.3

    pinch_threshold = 40

    drag_threshold = 40
    dragging = False

    pinch_start_time = None
    drag_hold_time = 0.4

    scroll_mode = False
    prev_scroll_y = None


    while True:

        success, img = cap.read()
        if not success:
            print("Error: Failed to capture image.")
            break


        img = detector.findHands(img, draw=True)
        lmList = detector.findPosition(img, draw=False)


        if len(lmList) != 0:

            # print(lmList[8])

            # fingerTips = [4, 8, 12, 16, 20]

            # for tipId in fingerTips:
            #     if tipId < len(lmList):
            #         x = lmList[tipId][1]
            #         y = lmList[tipId][2]
            #         print(f"Landmark ID (Tip): {tipId}, x={x}, y={y}")

            # print(f"Landmarks: {lmList}")


            h, w, _ = img.shape

            screen_w, screen_h = pyautogui.size()

            handLms_x, handLms_y = lmList[0][1], lmList[0][2]

            screen_x = int(handLms_x * screen_w /w)
            screen_y = int(handLms_y * screen_h /h)

            if 'prev_x' not in locals():
                prev_x, prev_y = screen_x, screen_y

            smooth_x = int(prev_x + (screen_x - prev_x) * 0.3)
            smooth_y = int(prev_y + (screen_y - prev_y) * 0.3)

            prev_x, prev_y = smooth_x, smooth_y

            pyautogui.moveTo(smooth_x, smooth_y)

            index_x, index_y = lmList[8][1], lmList[8][2]
            thumb_x, thumb_y = lmList[4][1], lmList[4][2]
            middle_x, middle_y = lmList[12][1], lmList[12][2]
            ring_x, ring_y = lmList[16][1], lmList[16][2]

            # distance_leftClick = math.sqrt((thumb_x - index_x)**2 + (thumb_y - index_y)**2)
            pinch_distance_leftClick = math.hypot((thumb_x - index_x), (thumb_y - index_y))

            if pinch_distance_leftClick < pinch_threshold and (time.time() - last_click_time) > clickDelay :
                pyautogui.click()
                last_click_time = time.time()


            # distance_rightClick = math.sqrt((thumb_x - middle_x) ** 2 + (thumb_y - middle_y) ** 2)
            pinch_distance_rightClick = math.hypot((thumb_x - middle_x), (thumb_y - middle_y))

            if pinch_distance_rightClick < pinch_threshold and (time.time()-last_click_time) > clickDelay:
                pyautogui.rightClick()
                last_click_time = time.time()


            pinch_distance_drag = math.hypot((thumb_x - ring_x), (thumb_y - ring_y))

            if pinch_distance_drag < drag_threshold:

                if pinch_start_time is None:
                    pinch_start_time = time.time()

                if time.time() - pinch_start_time > drag_hold_time:
                    if not dragging:
                        pyautogui.mouseDown()
                        dragging = True

            else:
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False
                pinch_start_time = None

            # if fingers_folded(lmList) and not dragging:
            #     pyautogui.mouseDown()
            #     dragging = True
            #
            # elif fingers_open(lmList) and dragging:
            #     pyautogui.mouseUp()
            #     dragging = False


            if is_scroll_mode(lmList):

                # if not scroll_mode:
                #     scroll_mode = True
                #
                # else:
                #     if scroll_mode:
                #         scroll_mode = False
                #
                # if scroll_mode:

                    if prev_scroll_y is None:
                        prev_scroll_y = lmList[0][2]

                    vertical_movement = prev_scroll_y - lmList[0][2]

                    if prev_scroll_y == 0:
                        prev_scroll_y = lmList[0][2]

                    # if vertical_movement > 0:
                    #     pyautogui.scroll(10)
                    #
                    # elif vertical_movement < 0:
                    #     pyautogui.scroll(-10)

                    scroll_amount = int(vertical_movement * 1)

                    if scroll_amount != 0:
                        pyautogui.scroll(scroll_amount)

                    prev_scroll_y = lmList[0][2]


        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        if fps > 30:
            color = (0, 255, 0)
        elif fps > 15:
            color = (0, 255, 255)
        else:
            color = (0, 0, 255)

        cv2.putText(img, str(int(fps)), (10, 70),
            cv2.FONT_HERSHEY_PLAIN, 3,
            color, 3 )

        if hasattr(detector, 'detected_hands') and detector.detected_hands.multi_hand_landmarks:
            cv2.putText(img, f"Hands: {len(detector.detected_hands.multi_hand_landmarks)}",
                        (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        cv2.namedWindow("Dextera Feed", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Dextera Feed", window_width, window_height)

        # cv2.namedWindow("Webcam Feed", cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty("Webcam Feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        cv2.imshow("Dextera Feed", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()