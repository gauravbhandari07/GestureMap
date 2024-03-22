import cv2
import mediapipe as mp
import pyautogui
import webbrowser
from pynput.mouse import Button, Controller
import time

class HandTracker:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, modelComplexity=1, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def handsFinder(self, image, draw=True):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image

    def positionFinder(self, image, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
            if draw:
                cv2.circle(image, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmlist
    
# mouse = Controller()
# mouse.press(Button.left)
                    # mouse.release(Button.left)

def navigate_google_maps(direction, distance):
    
    # Use pyautogui to simulate mouse movements
    if direction == "Right":
        # pyautogui.scroll(-500) # for zoom out use this
        pyautogui.mouseDown()  # Press and hold the left mouse button
        for x in range(distance):
            time.sleep(0.1)
            pyautogui.move(x, 0)  # Move mouse right when hand moves right
        pyautogui.mouseUp()  # Release the left mouse button
       
    elif direction == "Left":
        pyautogui.mouseDown()  # Press and hold the left mouse button
        for x in range(distance):
            time.sleep(0.1)
            pyautogui.move(-x, 0)   # Move mouse left when hand moves left
        pyautogui.mouseUp()  # Release the left mouse button
    elif direction == "Down":
        pyautogui.mouseDown()  # Press and hold the left mouse button
        for x in range(distance):
            time.sleep(0.1)
            pyautogui.move(0, x)  # Move mouse down when hand moves down
        pyautogui.mouseUp()  # Release the left mouse button
    elif direction == "Up":
        pyautogui.mouseDown()  # Press and hold the left mouse button
        for x in range(distance):
            time.sleep(0.1)
            pyautogui.move(0, -x)  # Move mouse up when hand moves up
        pyautogui.mouseUp()  # Release the left mouse button
    
    

def main():
    
    webbrowser.open("https://www.google.com/maps")

    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    prev_x = None  
    prev_y = None  
    while True:
        success, image = cap.read()
        image = tracker.handsFinder(image)
        lmList = tracker.positionFinder(image)

        if len(lmList) != 0:
            
            current_x = lmList[0][1]
            current_y = lmList[0][2]

            # If prev_x is not None, calculate the change in x-coordinate
            if prev_x is not None and prev_y is not None:
                delta_x = current_x - prev_x
                delta_y = current_y - prev_y

                # Define a threshold for movement (adjust as needed)
                threshold = 50

                
                if delta_x > threshold:
                    print("Left")  # Inverted control: moving hand right to go left
                    navigate_google_maps("Left",10)
                    
                elif delta_x < -threshold:
                    print("Right")  # Inverted control: moving hand left to go right
                    navigate_google_maps("Right",10)

                
                if delta_y > threshold:
                    print("Up")
                    navigate_google_maps("Up",10)
                elif delta_y < -threshold:
                    print("Down")
                    navigate_google_maps("Down",10)
            # Update prev_x with the current_x for the next frame
            prev_x = current_x
            prev_y = current_y

        cv2.imshow("Video", image)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
