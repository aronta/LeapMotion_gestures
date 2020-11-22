import speech_recognition,  keyboard, time
import MyUtils
import pyautogui
from playsound import playsound
from pynput.mouse import Button, Controller

mouse = Controller()
start_time = 0
on_time = time.time()
done = False
spaceFlag = False

recognizer = speech_recognition.Recognizer()


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
    recognizer.energy_threshold = 1500
    audio = recognizer.energy_threshold
    MyUtils.create_file("VoiceControlTest/")
    print("Threshold Value After calibration:" + str(recognizer.energy_threshold))
    print("Reci naredbu:")
    while not done:
        with speech_recognition.Microphone() as src:
            try:
                audio = recognizer.listen(src, phrase_time_limit=0.5)
                speech_to_txt = recognizer.recognize_google(audio, language="sr-SP").lower()
                print(speech_to_txt)

                if 'dup' in speech_to_txt:
                    pyautogui.click(clicks=2)
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time),
                                         "Double Click")

                elif'lije' in speech_to_txt:
                    pyautogui.click(button='left')
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time),
                                         "Left Click")
                elif 'esn' in speech_to_txt:
                    pyautogui.click(button='right')
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time),
                                         "Right Click")

                elif 'naz'in speech_to_txt:
                    mouse.click(Button.x1)
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time),
                                         "Back")
                elif 'napri' in speech_to_txt:
                    mouse.click(Button.x2)
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time),
                                         "Forward")

                elif 'gore' in speech_to_txt:
                    pyautogui.scroll(800)
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time),
                                         "Scroll Up")
                elif 'dolje' in speech_to_txt or'dole' in speech_to_txt:
                    pyautogui.scroll(-800)
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time),
                                         "Scroll Down")

                elif 'win' in speech_to_txt:
                    keyboard.press_and_release("windows + tab")
                    MyUtils.time_convert(time.time() - (start_time if start_time > 0 else on_time),
                                         "Tab")
                else:
                    playsound("sound/beep boop.mp3")

            except Exception as ex:
                print("Sorry. Could not understand.")
                playsound("sound/beep boop.mp3")


if __name__ == "__main__":
    main()