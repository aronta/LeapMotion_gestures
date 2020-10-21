from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Listener, KeyCode
import pythoncom, pyHook

mouse = Controller()

def uMad(event):
    return False

hm = pyHook.HookManager()
hm.KeyAll = uMad
hm.HookKeyboard()
pythoncom.PumpMessages()

def on_press(key):
    print('{0} pressed'.format(
        key))

def on_release(key):
    print('{0} release'.format(
        key))
    if key == KeyCode.from_char("1"):
        mouse.click(Button.left)
    if key == KeyCode.from_char("2"):
        mouse.click(Button.right)
    if key == Key.esc:
        pass


# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()












