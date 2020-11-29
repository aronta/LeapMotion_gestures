import keyboard as kb
import pyautogui
import speech_recognition as sr
import time
from playsound import playsound
from pynput import keyboard
from pynput.mouse import Button, Controller

import MyUtils

mouse = Controller()
start_time = 0
on_time = time.time()
done = False
spaceFlag = False

recognizer = sr.Recognizer()


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


listener = keyboard.Listener(
    on_press=on_press)
listener.start()


def main():
    global done
    global start_time
    global on_time
    global recognizer
    recognizer.energy_threshold = 1500
    MyUtils.create_file("VoiceControlTest/")
    print("Threshold Value After calibration:" + str(recognizer.energy_threshold))
    print("Reci naredbu:")
    while not done:
        with sr.Microphone() as src:
            try:
                recognizer = sr.Recognizer()
                recognizer.energy_threshold = 1500
                recognizer.pause_threshold = 0.5
                audio = recognizer.listen(src, phrase_time_limit=0.5)
                speech_to_txt = recognizer.recognize_google(audio, key=None, language="sr-SP").lower()
                print(speech_to_txt)

                if 'dup' in speech_to_txt:
                    pyautogui.click(clicks=2)
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time),
                                         "Double Click")
                    playsound("sound/mouse-click.mp3")
                    playsound("sound/mouse-click.mp3")

                elif 'lije' in speech_to_txt or 'evo' in speech_to_txt:
                    pyautogui.click(button='left')
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time),
                                         "Left Click")
                    playsound("sound/mouse-click.mp3")

                elif 'esn' in speech_to_txt:
                    pyautogui.click(button='right')
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time),
                                         "Right Click")
                    playsound("sound/mouse-click.mp3")

                elif 'naz' in speech_to_txt:
                    mouse.click(Button.x1)
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time),
                                         "Back")
                    playsound("sound/mouse-click.mp3")

                elif 'napr' in speech_to_txt:
                    mouse.click(Button.x2)
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time),
                                         "Forward")
                    playsound("sound/mouse-click.mp3")

                elif 'gore' in speech_to_txt:
                    pyautogui.scroll(800)
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time),
                                         "Scroll Up")
                    playsound("sound/mouse-click.mp3")

                elif 'olje' in speech_to_txt or 'dole' in speech_to_txt:
                    pyautogui.scroll(-800)
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time),
                                         "Scroll Down")
                    playsound("sound/mouse-click.mp3")

                elif 'win' in speech_to_txt:
                    kb.press_and_release("windows + tab")
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time),
                                         "Tab")

                else:
                    print("Sorry. Could not understand.")
                    playsound("sound/beep boop.mp3")
                    continue

            except sr.UnknownValueError:
                #recognizer.energy_threshold= 5000
                #print("Google Speech Recognition could not understand audio")
                continue

            except sr.RequestError as e:

                print("Could not request results from Google Speech Recognition service; {0}".format(e))


if __name__ == "__main__":
    main()