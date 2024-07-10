from pynput.mouse import Listener as MouseListener, Button
from pynput.keyboard import Listener as KeyListener, Key
import pyautogui
import pytesseract
import sys
import threading
import keyboard

start_x = 0
start_y = 0
end_x = 0
end_y = 0
selecting = False

loop_flag = True
global_text = ""

# The callback function that is triggered after the mouse is clicked
def on_mouse_click(x, y, button, pressed):
    global start_x, start_y, end_x, end_y, selecting
    if pressed:
        if button == Button.right: # When mouse right button clicked, capture start position
            start_x, start_y = x, y
            selecting = True
            print(f'Start Position: ({start_x}, {start_y})')
        elif button == Button.left and keyboard.is_pressed('f2'): # After pressing F2 + left click, use typewrite to type out the text
            global global_text
            pyautogui.typewrite(global_text, interval = 0.11)
    else:
        if selecting and button == Button.right: # When mouse right button released, capture end position
            end_x, end_y = x, y
            selecting = False
            print(f'End Position: ({end_x}, {end_y})')
            return False

# The callback function that is triggered after the ESC key is pressed
def on_key_press(key):
    if key == Key.esc:
        print("The ESC key has been pressed, exiting the program...")
        global loop_flag
        loop_flag = False
        return False

def start_mouse_listener():
    while True:
        with MouseListener(on_click=on_mouse_click) as listener:
            if (not loop_flag):
                break
            print("Please use the right mouse button to select the screen area, and right-click again to end the selection.")
            listener.join() # Wait to Triggered
            screen_area = select_screen_area(start_x, start_y, end_x, end_y)
            text = take_screenshot_and_ocr(*screen_area)
            print("Image captured, press F2 + left click to paste")
            global global_text
            global_text = text
            global_text = global_text.replace('\n', ' ')

def start_key_listener():
    with KeyListener(on_press=on_key_press) as listener:
        listener.join()

# Capture the screen and perform text recognition.
def take_screenshot_and_ocr(x, y, width, height):
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    recognized_text = pytesseract.image_to_string(screenshot)
    return recognized_text

# calculate the position of the top-left corner and the dimensions (width and height) of the rectangle
def select_screen_area(start_x, start_y, end_x, end_y):
    if start_x > end_x:
        start_x, end_x = end_x, start_x
    if start_y > end_y:
        start_y, end_y = end_y, start_y

    width = end_x - start_x
    height = end_y - start_y

    print(f'Selected Area: Position({start_x}, {start_y}), Size({width}, {height})')
    return (start_x, start_y, width, height)

# "You must specify the execution path for Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\path\\tesseract.exe'
mouse_thread = threading.Thread(target=start_mouse_listener)
key_thread = threading.Thread(target=start_key_listener)

mouse_thread.start()
key_thread.start()

mouse_thread.join()
key_thread.join()
