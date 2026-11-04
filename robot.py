import time

import cv2
from rwsuis import RWS

from main import find_codes

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

norbertIP = "http://152.94.160.198"
robot = RWS.RWS(norbertIP)
robot.request_rmmp()
time.sleep(5)
( tr , rot ) = robot.get_robtarget_variables("pyNextpos")
print(tr)

#help(RWS) # display useful help on package
while True:
    wrd = robot.get_rapid_variable("WRD")
    if (wrd==0): 
        print(" Robot is waiting for Python to set ’ WPW ’ ")
        # Nytt bilde
        (ret, frame)=cap.read()
        codes = find_codes(frame) 
         
        if codes:
            new_rt = codes[0].coordinates
            print(new_rt)
            robot.set_robtarget_translation("pyNextpos",new_rt)
            robot.set_rapid_variable("WPW",1)
    time.sleep(1)
# robot.request_mastership () # automatic mode


