import speech_recognition,  keyboard
import pyautogui
from playsound import playsound
from pynput.mouse import Button, Controller

mouse = Controller()

recognizer = speech_recognition.Recognizer()

def main():
    recognizer.energy_threshold = 1500
    audio = recognizer.energy_threshold
    print("Threshold Value After calibration:" + str(recognizer.energy_threshold))
    print("Reci naredbu:")
    while (1):
        with speech_recognition.Microphone() as src:
            try:
                audio = recognizer.listen(src, phrase_time_limit=0.5)
                speech_to_txt = recognizer.recognize_google(audio, language="sr-SP").lower()
                print(speech_to_txt)

                if 'dup' in speech_to_txt:
                    pyautogui.click(clicks=2)

                elif'lije' in speech_to_txt:
                    pyautogui.click(button='left')
                elif 'esn' in speech_to_txt:
                    pyautogui.click(button='right')

                elif 'naz'in speech_to_txt:
                    mouse.click(Button.x1)
                elif 'napri' in speech_to_txt:
                    mouse.click(Button.x2)

                elif 'gore' in speech_to_txt:
                    pyautogui.scroll(800)
                elif 'dolje' in speech_to_txt or'dole' in speech_to_txt:
                    pyautogui.scroll(-800)

                elif (speech_to_txt == 'windows'):
                    keyboard.press_and_release("windows + tab")
                else:
                    playsound("sound/beep boop.mp3")

            except Exception as ex:
                print("Sorry. Could not understand.")
                playsound("sound/beep boop.mp3")

if __name__ == "__main__":
    main()