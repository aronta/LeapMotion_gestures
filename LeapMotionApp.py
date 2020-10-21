import Leap, sys, thread, time, math, keyboard
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import pyautogui
from pynput.mouse import Button, Controller

mouse = Controller()

class LeapMotionListener(Leap.Listener):
    finger_names= ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    handRollFlag = False
    pinchFlag = False
    indexFinger = (0, 0, 0)
    thumbFinger = (0, 0, 0)
    palmDist = 0
    lastGestureID = -1


    def on_init(self, controller):
        print "Initialized"

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
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()

        for hand in frame.hands:
            #handType = "Left Hand" if hand.is_left else "Right Hand"
            #print handType + " Hand ID: " + str(hand.id) + " Nesto: " + str(hand.palm_normal.roll)
            if (hand.palm_normal.roll >= 3 or hand.palm_normal.roll <= -3) and not self.handRollFlag:
                self.handRollFlag = True
                keyboard.press_and_release("windows + tab")
                print "Hand Twist / Windows + Tab"
            elif hand.palm_normal.roll < 2 and hand.palm_normal.roll > -2:
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

            #Calculating distance between tip of the index finger and thumb
            dist = pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2)

            if dist > 1000 and self.pinchFlag:
                self.pinchFlag = False

            if dist <= 1000 and not self.pinchFlag:
                self.pinchFlag = True
                self.palmDist = hand.palm_position[1]
                print "Pinch / Scroll"

            if self.pinchFlag:
                scrollSpeed = (hand.palm_position[1] - self.palmDist) * 0.002
                #print "(" + str(scrollSpeed) + ", " + str(round(scrollSpeed)) + ")"
                mouse.scroll(0, scrollSpeed)


        for gesture in frame.gestures():
            ##CIRCLE GESTURES (clockwise/counterclowise)
            if gesture.id == self.lastGestureID + 1:
                self.lastGestureID = gesture.id
                continue
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)
                if gesture.state is Leap.Gesture.STATE_STOP:
                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2:
                        clockwise = True
                        pyautogui.click(button="right")
                        print "Circle Right / Right Mouse Click"
                        # print "ID: " + str(circle.id) + " Progress: " + str(circle.progress) + " Radius: " + str(
                        #     circle.radius) + " " + str(clockwise) + " " + str(circle.state) + " " + str(circle.frame)
                        time.sleep(1.5)
                    else:
                        #print "KRUGnaLIJEVO"
                        clockwise = False
                        pyautogui.click(button="left")
                        print "Circle Left / Left Mouse Click"
                        # print "ID: " + str(circle.id) + " Progress: " + str(circle.progress) + " Radius: " + str(
                        #     circle.radius) + " " + str(clockwise)
                        time.sleep(1.5)

            ##KEY TAP GESTURE
            if gesture.type is Leap.Gesture.TYPE_KEY_TAP:
                key_tap = Leap.KeyTapGesture(gesture)
                pyautogui.click(clicks=2)
                print "KeyTap / Double Click"
                #print "Key Tap ID: " + str(key_tap.id) + " State " + self.state_names[key_tap.state] + " Position: " + str(key_tap.position) + " Direction: " + str(key_tap.direction)
                time.sleep(1.5)

            ##SWIPE GESTURES (left, right, up, down)
            if gesture.type is Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                if swipe.direction.x > 0 and gesture.state is Leap.Gesture.STATE_STOP and math.fabs(swipe.direction.x) > math.fabs(swipe.direction.y) :
                    print "SWIPE Left->Right / Go Forward"
                    #print "Swipe ID: " + str(swipe.id) + " State: " + self.state_names[gesture.state] + " Position: " + str(swipe.position) + " Direction Left->Right"
                    mouse.click(Button.x2)
                    time.sleep(1.5)
                elif swipe.direction.x < 0 and gesture.state is Leap.Gesture.STATE_STOP and math.fabs(swipe.direction.x) > math.fabs(swipe.direction.y):
                    print "SWIPE Right->Left / Go Back"
                    #print "Swipe ID: " + str(swipe.id) + " State: " + self.state_names[gesture.state] + " Position: " + str(swipe.position) + " Direction Right->Left"
                    mouse.click(Button.x1)
                    time.sleep(1.5)
                # elif swipe.direction.y > 0 and gesture.state is Leap.Gesture.STATE_STOP and math.fabs(swipe.direction.x) < math.fabs(swipe.direction.y) :
                #     print "SWIPE Down->Up"
                #     print "Swipe ID: " + str(swipe.id) + " State: " + self.state_names[gesture.state] + " Position: " + str(swipe.position) + " Direction Down->Up"
                #     #pyautogui.scroll(1000)
                #     time.sleep(1.5)
                # elif swipe.direction.y < 0 and gesture.state is Leap.Gesture.STATE_STOP and math.fabs(swipe.direction.x) < math.fabs(swipe.direction.y):
                #     print "SWIPE Up->Down"
                #     print "Swipe ID: " + str(swipe.id) + " State: " + self.state_names[gesture.state] + " Position: " + str(swipe.position) + " Direction Up->Down"
                #     #pyautogui.scroll(-1000)
                #     time.sleep(1.5)
            self.lastGestureID = gesture.id

def main():
    listener = LeapMotionListener()
    controller = Leap.Controller()

    controller.add_listener(listener)
    print "Press enter to quit"

    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
       pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()



