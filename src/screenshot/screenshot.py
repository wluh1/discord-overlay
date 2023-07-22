from typing import Tuple
import win32gui
import win32ui
from ctypes import windll
from PIL import Image
from settings.settings import current_settings
import cv2
import numpy as np
from screenshot.find_window import find_window


def get_screenshot():
    window_name = current_settings.get_program_name()
    hwnd = find_window(window_name)
    if hwnd == 0:
        return None, "Could not find window with name: " + window_name
    # Change the line below depending on whether you want the whole window
    # or just the client area. 
    #left, top, right, bot = win32gui.GetClientRect(hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area. 
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    image = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if not result == 1:
        return None, "Error when saving image."

    image, errText = _crop_image_subimage(image)
    if errText != None:
        return None, errText

    image = _make_transparent(image)

    return image, None


def _make_transparent(image: Image):
    image = image.convert("RGBA")

    pixdata = image.load()
    imgWidth, imgHeight = image.size
    for y in range(imgHeight):
        for x in range(imgWidth):
            if _should_make_transparent(pixdata[x, y]):
                pixdata[x, y] = (255, 255, 255, 0)

    return image


def _crop_image_subimage(image):
    cv2_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    template = cv2.imread("./assets/template.png")
    result = cv2.matchTemplate(cv2_image, template, cv2.TM_CCOEFF_NORMED)

    (yCoords, xCoords) = np.where(result >= 0.8)
    if len(yCoords) == 0:
        return None, "Cannot find voice channel icon (window is probably minimized)."

    startY = yCoords[0] - 2 # Small offset to make it look nicer
    startX = xCoords[0] - 3 # Small offset to make it look nicer

    endY = -1
    if not current_settings.get_auto_height():
        endY = startY + current_settings.get_image_height()
    else:
        for c in yCoords:
            if c > startY + 10: # Check if it is another matching. Sometimes the same image gives multiple matches.
                endY = c - 8 # Small offset to make it look nicer
                break
        if endY == -1:
            return None, "Cannot find second voicechannel to use for bottom border. Try without autoHeight."

    width = current_settings.get_image_width()

    image = image.crop((startX, startY, startX + width, endY))
    
    return image, None


def _should_make_transparent(pixel: Tuple[int, int, int, int]):
    c = (47, 49, 54)
    leeway = 5
    for i in range(len(c)):
        if pixel[i] < c[i] - leeway or pixel[i] > c[i] + leeway:
            return False
    return True
