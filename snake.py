from PIL import ImageGrab
import numpy as np
import pyautogui as pkey
import time
import cv2

def screen():
    time.sleep(3)
    #pkey.keyDown('D')
    while True:
        org=cv2.cvtColor(np.array(ImageGrab.grab(bbox=(0,230,900,1000))),cv2.COLOR_BGR2RGB)
        final_img,board,snake_body,snake_head,apple_cont=get_edges(org)
        get_positions(snake_head,apple_cont)
        #Draw
        cv2.imshow('Processed Image',final_img)
        if cv2.waitKey(25) & 0xff == ord('q'):  
            cv2.destroyAllWindows()
            break

def get_edges(original):
    #Get apple and snake head contour
    apple=cv2.Canny(original,200,400)
    apple_cont=cv2.HoughCircles(apple,cv2.HOUGH_GRADIENT,4,100,minRadius=23,maxRadius=26)
    snake_head=cv2.HoughCircles(apple,cv2.HOUGH_GRADIENT,8,0.00001,maxRadius=12)

    #Get contour of the snake body
    snake=cv2.Canny(original,0,680)
    snake_contour,_=cv2.findContours(snake,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    #Get contour of the board
    board=cv2.Canny(original,100,150)
    board_contour,_=cv2.findContours(board,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    #Draw
    cv2.drawContours(original,board_contour,-1,0,3)
    draw_circles(original,apple_cont,1)
    draw_circles(original,snake_head,0)
    cv2.drawContours(original,snake_contour,-1,(0,0,255),3)

    return original,board_contour,snake_contour,snake_head,apple_cont


def draw_circles(img,circles,t):
    if circles is not None:
        circles=np.round(circles[0,:]).astype('int')
        for (x,y,r) in circles:
            if t==1:
                cv2.circle(img,(x,y),r,(50,205,50),3)
            else:
                cv2.circle(img,(x,y),r,(255,0,0),3)

def get_positions(snake,fruit):
    if snake is not None:
        snake_pos=np.mean(snake[0],axis=0)[:-1]
    if fruit is not None:
        fruit_pos=fruit[0][0][:-1]
        
screen()