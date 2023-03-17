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
        get_positions(snake_head,apple_cont,board,snake_body)
        #Draw
        cv2.imshow('Processed Image',final_img)
        if cv2.waitKey(25) & 0xff == ord('q'):  
            cv2.destroyAllWindows()
            break

def get_edges(original):

    #Get contour of the snake body
    original=cv2.cvtColor(original,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(original,np.array([110,50,50]),np.array([130,255,255]))
    body=cv2.bitwise_and(original,original,mask=mask)
    body=cv2.Canny(body,20,100)
    snake_contour,_=cv2.findContours(body,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

    #Get apple contour
    mask=cv2.inRange(original,np.array([-10,100,100]),np.array([10,225,255]))
    apple=cv2.bitwise_and(original,original,mask=mask)
    apple=cv2.Canny(apple,20,100)
    apple_cont,_=cv2.findContours(apple,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    
    #Get contour of the eyes
    mask=cv2.inRange(original,np.array([0,0,255-15]),np.array([255,15,255]))
    head=cv2.bitwise_and(original,original,mask=mask)
    head=cv2.Canny(head,0,100)
    snake_head,_=cv2.findContours(head,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

    #Get contour of the board
    board=cv2.Canny(original,100,150)
    board_contour,_=cv2.findContours(board,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    #Draw
    original=cv2.cvtColor(original,cv2.COLOR_HSV2RGB)
    #cv2.drawContours(original,board_contour,-1,0,3)
    cv2.drawContours(original,apple_cont,-1,(50,205,50),3)
    cv2.drawContours(original,snake_head,-1,(176,224,230),3)
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

def get_positions(snake,fruit,board,snake_b):
    snake_pos=get_relative_position(snake)
    fruit_pos=get_relative_position(fruit)
    if type(snake_pos) is np.ndarray and type(fruit_pos) is np.ndarray:#40
        if fruit_pos[0]-snake_pos[0]>40: pkey.keyDown("D")
        if fruit_pos[0]-snake_pos[0]<-40: pkey.keyDown("A")
        if fruit_pos[1]-snake_pos[1]<-40: pkey.keyDown("W")
        if fruit_pos[1]-snake_pos[1]>40: pkey.keyDown("S")

def get_relative_position(contour):
    if contour is not None:
        pos=list()
        for i in contour:
            M=cv2.moments(i)
            if M['m00']!=0:
                x=int(M['m10']/M['m00'])
                y=int(M['m01']/M['m00'])
                if x>=0 and y>=0:
                    pos.append([x,y])
        pos=np.nanmean(np.asarray(pos),axis=0)
        return pos
    return np.nan
    
        
screen()