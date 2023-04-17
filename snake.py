import pygetwindow as window
from PIL import ImageGrab
from astar import a_star
import pyautogui as pkey
import numpy as np
import math
import time
import cv2

def screen():
    win=window.getWindowsWithTitle('Google - Google Chrome')[0]
    win.activate()
    #win.maximize()
    time.sleep(0.5)
    pkey.press("Enter")
    time.sleep(0.2)
    snake,apple,body=get_snake(),get_apple(),get_body_contour()
    f_board=np.array([[0 if cv2.pointPolygonTest(body[0],(48*(i)+56,48*(j)+54),False)!=1.0 else 1 for j in range(15)] for i in range(17)]).transpose()
    f_board[apple[1],apple[0]]=2
    while window.getActiveWindow().title=="Google - Google Chrome":
        apple=get_apple()
        path=a_star(snake,apple,f_board)
        if path==list() or path is None: continue
        last_key=move(snake,path)
        body=get_body_contour()
        a=[len(x) for x in body]
        board=np.array([[0 if cv2.pointPolygonTest(body[a.index(max(a))],(48*(i)+56,48*(j)+54),False)!=1.0 else 1 for j in range(15)] for i in range(17)]).transpose()
        if np.any(board-f_board==1)==False or np.array_equal(f_board,board): continue
        else:
            snake=tuple(changes(np.where(board-f_board==1),last_key,snake))
            f_board=board
        #print(snake,path)

def move(snake,path):                
    #Average movement
    if snake[0]<path[0][0]:
        pkey.press("D")
        return "D"
    elif snake[1]<path[0][1]:
        pkey.press("S")
        return "S"
    elif snake[0]>path[0][0]:
        pkey.press("A")
        return "A"
    elif snake[1]>path[0][1]: 
        pkey.press("W")
        return "W"

def check_crash(snake,path,last_key):
    #Imminent crash
    if snake[0]==0 or snake[0]==16:
        print("Aiuda me estrello")
        if path[-1][1]>=snake[1]:
            pkey.press("S")
            return "S"
        elif path[-1][1]<snake[1]:
            pkey.press("W")
            return "W"
    if snake[1]==0 or snake[1]==14:
        print("Aiuda me estrello")
        if path[-1][0]>=snake[0]:
            pkey.press("D")
            return "D"
        elif path[-1][0]<snake[0]:
            pkey.press("A")
            return "A"
    return last_key

def changes(diff,last_key,snake):
    if len(diff[0])==0:
        print("Esto no debe aparecer!")
        return get_snake(snake)
    if len(diff[0])>1:
        if last_key=="D": return [int(max(diff[1])),int(diff[0][list(diff[1]).index(max(diff[1]))])]
        if last_key=="A": return [int(min(diff[1])),int(diff[0][list(diff[1]).index(max(diff[1]))])]
        if last_key=="W": return [int(diff[1][list(diff[0]).index(min(diff[0]))]),int(min(diff[0]))]
        if last_key=="S": return [int(diff[1][list(diff[0]).index(min(diff[0]))]),int(max(diff[0]))]
    if len(diff[0])==1: return [int(diff[1]),int(diff[0])]


def get_snake(last=(4,7)):
    eyes=get_eyes_contour()
    snake=get_snake_position(eyes,last)
    return tuple(snake)

def get_apple(last=(12,7)):
    fruit=get_apple_contour()
    apple=get_apple_position(fruit,last)
    return tuple(apple)

def get_snake_position(eyes_contour,last_snake):
    snake_pos=get_relative_position(eyes_contour).astype(int)
    if snake_pos.any()==False: return last_snake
    snake_square=[math.ceil((snake_pos[0]-80)/48.1),math.ceil((snake_pos[1]-78)/48.1)]
    return snake_square

def get_apple_position(apple_contour,last_apple):
    apple_pos=get_relative_position(apple_contour).astype(int)
    if apple_pos.any()==False: return last_apple
    apple_square=[math.ceil((apple_pos[0]-80)/48.1),math.ceil((apple_pos[1]-78)/48.1)]
    return apple_square
    
def get_body_contour():
    original=cv2.cvtColor(np.array(ImageGrab.grab(bbox=(10,230,900,1000))),cv2.COLOR_BGR2RGB)
    original=cv2.cvtColor(original,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(original,np.array([110,50,50]),np.array([130,255,255]))
    body=cv2.bitwise_and(original,original,mask=mask)
    body=cv2.Canny(body,0,100)
    snake_contour,_=cv2.findContours(body,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    return snake_contour

def get_apple_contour():
    original=cv2.cvtColor(np.array(ImageGrab.grab(bbox=(10,230,900,1000))),cv2.COLOR_BGR2RGB)
    original=cv2.cvtColor(original,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(original,np.array([-10,100,100]),np.array([10,225,255]))
    apple=cv2.bitwise_and(original,original,mask=mask)
    apple=cv2.Canny(apple,20,100)
    apple_contour,_=cv2.findContours(apple,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    return apple_contour

def get_eyes_contour():
    original=cv2.cvtColor(np.array(ImageGrab.grab(bbox=(10,230,900,1000))),cv2.COLOR_BGR2RGB)
    original=cv2.cvtColor(original,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(original,np.array([0,0,255-15]),np.array([255,15,255]))
    head=cv2.bitwise_and(original,original,mask=mask)
    head=cv2.Canny(head,0,100)
    eyes_contour,_=cv2.findContours(head,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    return eyes_contour

def get_relative_position(contour):
    pos=list()
    for c in contour:
        M=cv2.moments(c)
        if M['m00']==0: continue
        x=int(M['m10']/M['m00'])
        y=int(M['m01']/M['m00'])
        pos.append([x,y])
    if len(pos)>0:
        pos=np.nanmean(np.asarray(pos),axis=0)
    return np.asarray(pos)
        
screen()
