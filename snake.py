from PIL import ImageGrab
import numpy as np
import cv2

def get_screen():
    while True:
        org=cv2.cvtColor(np.array(ImageGrab.grab(bbox=(0,230,900,1000))),cv2.COLOR_BGR2RGB)
        grey_image=cv2.Canny(org,20,30)
        cv2.imshow('window',grey_image)
        if cv2.waitKey(25) & 0xff == ord('q'):
            cv2.destroyAllWindows()
            break

get_screen()