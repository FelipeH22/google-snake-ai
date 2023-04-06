import pygetwindow as window
from PIL import ImageGrab
from astar import a_star
import pyautogui as pkey
import numpy as np
import math
import time
import cv2

def screen():
    path=list()
    obj=(3,7)
    win=window.getWindowsWithTitle('Google - Google Chrome')[0]
    win.activate()
    #win.maximize()
    time.sleep(0.5)
    pkey.press("Enter")
    time.sleep(0.2)
    while window.getActiveWindow().title=="Google - Google Chrome":
        snake,fruit,snake_contour=extraction()
        if snake is None or fruit is None or snake_contour is None: continue
        if not path: path=a_star(tuple(snake),tuple(fruit),[[0 if cv2.pointPolygonTest(snake_contour[0],(48*(i)+56,48*(j)+54),False)!=1.0 else 1 for j in range(16)] for i in range(18)])
        move(snake,path)
        for pos in path:
            if cv2.pointPolygonTest(snake_contour[0],(48*(pos[0])+56,48*(pos[1])+54),False)==1.0:
                path.remove(pos)
                print(f"position {pos} removed. The path now is {path}. Snake is now at {snake}")
        
        

def move(snake,path):
    obj=path[0]
    if snake[0]==obj[0] and snake[1]==obj[1]: return obj
    if snake[0]<obj[0]:
        pkey.press("D")
    if snake[0]>obj[0]:
        pkey.press("A")
    if snake[1]>obj[1]:
        pkey.press("W")
    if snake[1]<obj[1]:
        pkey.press("S")
    

def extraction():
    org=cv2.cvtColor(np.array(ImageGrab.grab(bbox=(10,230,900,1000))),cv2.COLOR_BGR2RGB)
    _,snake_body,snake_head,apple_cont=get_edges(org)
    snake,fruit=get_positions(snake_head,apple_cont)
    return snake,fruit,snake_body

def get_positions(snake,fruit):
    snake_pos=get_relative_position(snake).astype(int)
    fruit_pos=get_relative_position(fruit).astype(int)
    if snake_pos.any()==False or fruit_pos.any()==False: return None,None
    snake_square=[math.ceil((snake_pos[0]-80)/48.1),math.ceil((snake_pos[1]-78)/48.1)]
    fruit_square=[math.ceil((fruit_pos[0]-80)/48.1),math.ceil((fruit_pos[1]-78)/48.1)]
    return snake_square,fruit_square
    
def get_relative_position(contour):
    if contour is not None:
        pos=list()
        for i in contour:
            M=cv2.moments(i)
            if M['m00']!=0:
                x=M['m10']/M['m00']
                y=M['m01']/M['m00']
                if x>=0 and y>=0:
                    pos.append([x,y])
        if len(pos)>0:
            pos=np.nanmean(np.asarray(pos),axis=0)
        return np.asarray(pos)
    return np.array([])
    
def get_edges(original):
    #Get contour of the snake body
    original=cv2.cvtColor(original,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(original,np.array([110,50,50]),np.array([130,255,255]))
    body=cv2.bitwise_and(original,original,mask=mask)
    body=cv2.Canny(body,200,500)
    snake_contour,_=cv2.findContours(body,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

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
    board=cv2.Canny(original,100,300)
    board=cv2.GaussianBlur(board,(5,5),7)
    board_contour,_=cv2.findContours(board,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    return board_contour,snake_contour,snake_head,apple_cont
    

       
screen()
