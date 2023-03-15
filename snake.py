from PIL import ImageGrab
import numpy as np
import pyautogui as pkey
import time
import cv2

def get_screen():
    #Initialize the game by pressing enter and moving the snake to the right
    time.sleep(3)
    pkey.keyDown('Enter')
    pkey.keyDown('D')
    while True:
        org=cv2.cvtColor(np.array(ImageGrab.grab(bbox=(0,230,900,1000))),cv2.COLOR_BGR2RGB)
        grey_image=cv2.Canny(org,20,30)
        cv2.imshow('window',grey_image)
        if cv2.waitKey(25) & 0xff == ord('q'):  
            cv2.destroyAllWindows()
            break
        
get_screen()