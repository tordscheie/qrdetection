import time

import cv2
from rwsuis import RWS

from Conversion_funk import find_table_coords
from main import scan_for_qr

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

norbertIP = "http://152.94.160.198"
robot = RWS.RWS(norbertIP)
( tr , rot ) = robot.get_robtarget_variables("pyNextpos")
print(tr)

#help(RWS) # display useful help on package
while True:
    
    wrd = robot.get_rapid_variable("WRD")
    if (wrd==0): 
        print(" Robot is waiting for Python to set ’ WPW ’ ")

        # Nytt bilde
        (ret, frame)=cap.read()

        new_frame, qr_codes = scan_for_qr(frame)
    
        code = qr_codes[0]
        new_rt = find_table_coords(code.center_x, code.center_y, 300)
        print(new_rt)
        robot.set_robtarget_translation("pyNextpos",new_rt)
        robot.set_rapid_variable("WPW",1)
    # robot.request_rmmp() # mastership manual mode , GRANT on
    time.sleep(1)
# robot.request_mastership () # automatic mode


