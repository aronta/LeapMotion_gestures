import keyboard as kb
import pyautogui
from pynput import keyboard
from pynput.mouse import Button, Controller

import Leap
import MyUtils
import math
import time
from Leap import CircleGesture, SwipeGesture

mouse = Controller()
spaceFlag = False
done = False
on_time = time.time()
start_time = 0


def on_press(key):
    global start_time
    global spaceFlag
    global done
    if str(key) == "Key.space" and not spaceFlag:
        if start_time == 0:
            start_time = time.time()
            MyUtils.time_convert(0, "----------Test start!----------")
        else:
            MyUtils.time_convert(time.time() - start_time, "---------- Test end! ----------")
            spaceFlag = True
            MyUtils.f.close()
            done = True


klistener = keyboard.Listener(
    on_press=on_press)
klistener.start()


class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    handRollFlag = False
    pinchFlag = False
    indexFinger = (0, 0, 0)
    thumbFinger = (0, 0, 0)
    palmDist = 0
    lastGestureTime = time.time()
    gesture_done = False

    def on_init(self, controller):
        print "Initialized!"

    def on_connect(self, controller):
        print "Motion Sensor Connected!"

        controller.config.set("Gesture.Circle.MinRadius", 40.0);
        controller.config.save();
        controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES);
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected!"

    def on_exit(self, controller):
        print "Exited!"

    def on_frame(self, controller):
        global start_time
        global on_time
        frame = controller.frame()
        last_frame = controller.frame(1)

        for hand in frame.hands:
            if (hand.palm_normal.roll >= 3 or hand.palm_normal.roll <= -3) and not self.handRollFlag:
                self.handRollFlag = True
                kb.press_and_release("windows + tab")
                MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time), "Hand Twist / Windows + Tab")
            elif 2 > hand.palm_normal.roll > -2:
                self.handRollFlag = False

            for finger in hand.fingers:
                if finger.type == 0:
                    self.thumbFinger = finger.stabilized_tip_position
                if finger.type == 1:
                    self.indexFinger = finger.stabilized_tip_position

            x1 = self.indexFinger[0]
            y1 = self.indexFinger[1]
            z1 = self.indexFinger[2]

            x2 = self.thumbFinger[0]
            y2 = self.thumbFinger[1]
            z2 = self.thumbFinger[2]

            dist = pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2)

            if dist > 1000 and self.pinchFlag:
                self.pinchFlag = False

            if dist <= 1000 and not self.pinchFlag:
                self.pinchFlag = True
                self.palmDist = hand.palm_position[1]
                MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time), "Pinch / Scroll")

            if self.pinchFlag:
                scrollSpeed = (hand.palm_position[1] - self.palmDist) * 0.002
                mouse.scroll(0, scrollSpeed)

        #MyUtils.time_convert(time.time() - on_time, "test")
        for gesture in frame.gestures():

            if 2 > time.time() - self.lastGestureTime > 1.5:
                continue

            # CIRCLE GESTURES (clockwise/counterclockwise)
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                self.gesture_done = True
                circle = CircleGesture(gesture)
                if gesture.state is Leap.Gesture.STATE_STOP:
                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2:
                        pyautogui.click(button="right")
                        MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time), "Circle Right / Right Click")
                        self.lastGestureTime = time.time()
                        time.sleep(1.5)
                    else:
                        pyautogui.click(button="left")
                        MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time), "Circle Left / Left Click")
                        self.lastGestureTime = time.time()
                        time.sleep(1.5)

            # KEY TAP GESTURE
            if gesture.type is Leap.Gesture.TYPE_KEY_TAP:
                self.gesture_done = True
                pyautogui.click(clicks=2)
                MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time), "KeyTap / Double Click")
                self.lastGestureTime = time.time()
                time.sleep(1.5)

            # SWIPE GESTURES (left, right)
            if gesture.type is Leap.Gesture.TYPE_SWIPE:
                self.gesture_done = True
                swipe = SwipeGesture(gesture)
                if swipe.direction.x > 0 and gesture.state is Leap.Gesture.STATE_STOP and math.fabs(
                        swipe.direction.x) > math.fabs(swipe.direction.y):
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time), "SWIPE Left->Right / Go Back")
                    mouse.click(Button.x1)
                    self.lastGestureTime = time.time()
                    time.sleep(1.5)
                elif swipe.direction.x < 0 and gesture.state is Leap.Gesture.STATE_STOP and math.fabs(
                        swipe.direction.x) > math.fabs(swipe.direction.y):
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time), "SWIPE Right->Left / Go Forward")
                    mouse.click(Button.x2)
                    self.lastGestureTime = time.time()
                    time.sleep(1.5)


def main():
    global klistener
    global done
    MyUtils.create_file("LeapMotionTest/")
    listener = LeapMotionListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    while not done:
        continue
    controller.remove_listener(listener)

if __name__ == "__main__":
    main()
