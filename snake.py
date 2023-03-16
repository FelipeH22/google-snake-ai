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
        
        #Get the grid
        grey_image=cv2.Canny(org,20,30)
        edges=cv2.HoughLinesP(grey_image,1,np.pi/180,threshold=100,minLineLength=.5,maxLineGap=100)

        #Get apple
        apple=cv2.Canny(org,200,400)
        apple_cont=cv2.HoughCircles(apple,cv2.HOUGH_GRADIENT,4,100,minRadius=20,maxRadius=25)

        #Get contour of the snake
        snake=cv2.Canny(org,0,680)
        snake_contour,_=cv2.findContours(snake,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

        #Get contour of the board
        board=cv2.Canny(org,100,150)
        board_contour,_=cv2.findContours(board,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        
        #Draw
        cv2.drawContours(org,board_contour,-1,0,3)
        draw_circles(org,apple_cont)
        cv2.drawContours(org,snake_contour,-1,(0,0,255),3)
        cv2.imshow('original',org)
        if cv2.waitKey(25) & 0xff == ord('q'):  
            cv2.destroyAllWindows()
            break

def draw_edges(img,edges):
    for point in edges:
        x1,y1,x2,y2=point[0]
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)

def draw_circles(img,circles):
    if circles is not None:
        circles=np.round(circles[0,:]).astype('int')
        for (x,y,r) in circles:
            cv2.circle(img,(x,y),r,(50,205,50),3)
        
get_screen()