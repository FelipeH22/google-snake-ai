from PIL import ImageGrab
import numpy as np
import pyautogui as pkey
import time
import cv2

def get_screen():
    time.sleep(3)
    pkey.keyDown('D')
    while True:
        org=cv2.cvtColor(np.array(ImageGrab.grab(bbox=(0,230,900,1000))),cv2.COLOR_BGR2RGB)
        grey_image=cv2.Canny(org,20,30)
        edges=cv2.HoughLinesP(grey_image,1,np.pi/180,threshold=100,minLineLength=.5,maxLineGap=100)
        external_edges=cv2.HoughLinesP(grey_image,1,np.pi/180,threshold=30,minLineLength=50,maxLineGap=.0001)
        draw_edges(org,edges,1)
        draw_edges(org,external_edges,0)
        cv2.imshow('original',org)
        cv2.imshow('edges',grey_image)
        if cv2.waitKey(25) & 0xff == ord('q'):  
            cv2.destroyAllWindows()
            break

def draw_edges(img,edges,pos):
    for point in edges:
        x1,y1,x2,y2=point[0]
        if pos==1:
            cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)
        else:
            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
        
get_screen()