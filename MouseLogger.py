import sys

from pynput import mouse
from pynput import keyboard
import time

import MyUtils

start_time = 0
on_time = time.time()
done = False
spaceFlag = False


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

def on_click(x, y, button, pressed):
    if pressed:
        if str(button) == "Button.left":
            MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time), "Left Click")
        else:
            MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time), "Right Click")


mlistener = mouse.Listener(
    on_click = on_click)
mlistener.start()

def main():
    global klistener
    global mlistener
    MyUtils.create_file("EviacamTest/")

    while not done:
        continue
    sys.exit()

if __name__ == "__main__":
    main()
