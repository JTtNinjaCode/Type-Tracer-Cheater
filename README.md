# Type-Tracer-Cheater
This program is designed to cheat on TypeRacer by using right-click to capture image, OCR for text recognition, and outputting it.

TypeRacer:https://play.typeracer.com/

### Dependencies
This program depends on pynput, pyautogui, pytesseract, keyboard.
```console
pip install pynput pyautogui pytesseract keyboard
```
In addition to the Python dependencies mentioned above, it also requires Tesseract for OCR:https://tesseract-ocr.github.io/tessdoc/Downloads.html

### Run
To avoid detection when typing over 100 WPM, limit typing speed with the interval parameter in pyautogui.typewrite.
```python
pyautogui.typewrite(global_text, interval = 0.11) # Interval between each typing is 0.11 seconds.
```
After downloading Tesseract, use pytesseract.pytesseract.tesseract_cmd to specify the path to Tesseract.
```python
# main.py
pytesseract.pytesseract.tesseract_cmd = r'C:\\path\\tesseract.exe'
```
Once the setup is complete, you can run the program.
```console
py main.py
```
