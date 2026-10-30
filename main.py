import math as m

import cv2
import numpy as np


def find_qr(puck):
    gray_puck = cv2.cvtColor(puck, cv2.COLOR_BGR2GRAY)
    blurred_puck = cv2.GaussianBlur(gray_puck, (1, 1), 2)
    _, thresh_puck = cv2.threshold(blurred_puck, 100, 255, cv2.THRESH_BINARY)
    detector = cv2.wechat_qrcode_WeChatQRCode()
    data, points = detector.detectAndDecode(thresh_puck) 

    if data is not None:
        box_points = np.int32(points).reshape((-1, 1, 2))
        return (data,box_points)

def find_center_qr(box_points):
        # Center qr code
        avg_x = int((box_points[0, 0, 0] + box_points[0, 1, 0]+ box_points[0,2,0] + box_points[0,3,0])/4)
        avg_y = int((box_points[0, 0, 0] + box_points[0, 1, 0]+ box_points[0,2,0] + box_points[0,3,0])/4)
        center_qr = np.array([avg_x, avg_y])

        return center_qr

def find_angle(box_points):
        dx = box_points[1,0,0] - box_points[0,0,0]
        dy = box_points[1,0,1] - box_points[0,0,1]
        ang = 0
        if dx < 0:
            ang = m.atan(dy/dx) +m.pi
        elif dx >0 and dy <0:
            ang = m.atan(dy/dx) + 2*m.pi
        else:
            ang = m.atan(dy/dx)
        
        ang_deg = int(m.degrees(ang))

        return (ang_deg, (dx,dy))


def draw_text(frame, data, x, y):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1  
        thickness = 1
        text_color = (0,0,255)
        cv2.putText(frame, str(data), (int(x + 1),int(y - 4)), font, font_scale, text_color, thickness=thickness, lineType=cv2.LINE_AA)

def find_puck(frame):
    img = frame.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 5)
    _, thresh = cv2.threshold(blurred, 125, 255, cv2.THRESH_BINARY)

    circles = cv2.HoughCircles(
                blurred,
                cv2.HOUGH_GRADIENT, 
                dp=0.9, 
                minDist=50,         # Keeps detections separated
                param1=212,           # Upper threshold for Canny edge detector
                param2=41,           # Sensitivity (Lower values find more faint/imperfect circles)
                minRadius=27,        # Minimum radius of the pucks in your image
                maxRadius=100        # Maximum radius of the pucks in your image
                )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        print(f"Successfully detected {len(circles[0])} pucks")
        
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            
            pnkt1 = (int(center[0]-radius), int(center[1]-radius))
            pnkt2 = (int(center[0]+radius), int(center[1]+radius))

            # cv2.rectangle(frame,pnkt1, pnkt2, (0,0,255), 3)
            cv2.circle(frame, center, int(radius), (0, 255, 0), 3)
            puck = frame[pnkt1[1]:pnkt2[1], pnkt1[0]:pnkt2[0]]

            data, box_points = find_qr(puck)
            ang = 0

            if len(box_points) > 0:

                ang, pnkt = find_angle(box_points)

                print(f"DATA: {data} - angle: {ang}")

                cv2.polylines(puck, [box_points], isClosed=True, color=(0, 255, 0), thickness=3)
                cv2.circle(puck, box_points[0,0], 10, (255, 0, 255), -1)
                cv2.circle(puck, box_points[1,0], 10, (255, 0, 255), -1)
                cv2.line(puck, box_points[0,0],box_points[0,0] +pnkt, (0,0,255), 5 )

                draw_text(frame, data, int(center[0]),int(center[1]))

    return frame


image = cv2.imread('images/300mm.jpg')
mask = find_puck(image)
cv2.imshow('Pop-up Display Window', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

