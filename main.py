import math as m

import cv2
import numpy as np

WIDTH = 1280
HEIGHT = 720

def find_qr(puck):
    """Kode for å ta inn en puck og returnerer dataen til pucken og hjørnene"""
    gray_puck = cv2.cvtColor(puck, cv2.COLOR_BGR2GRAY)
    blurred_puck = cv2.GaussianBlur(gray_puck, (3, 3), 2)
    _, thresh_puck = cv2.threshold(blurred_puck, 100, 255, cv2.THRESH_BINARY)
    detector = cv2.wechat_qrcode_WeChatQRCode()
    data, points = detector.detectAndDecode(thresh_puck) 

    if data is not None:
        box_points = np.int32(points).reshape((-1, 1, 2))
        return (data,box_points)


def find_angle(box_points):
        """Finder hvor mye linjen fra hjørne oppe i høyre og hjøre oppe i venstre har rotert,
        returnerer grader og hvor lang linjen er
        """
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
        text_color = (250,0,250)
        cv2.putText(frame, str(data), (int(x + 1),int(y - 4)), font, font_scale, text_color, thickness=thickness, lineType=cv2.LINE_AA)

def find_puck(frame):
    """Finder puckene og markere de med en firkant"""
    img = frame.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 5)

    circles = cv2.HoughCircles(
                blurred,
                cv2.HOUGH_GRADIENT, 
                dp=1, 
                minDist=50,         # Keeps detections separated
                param1=143,           # Upper threshold for Canny edge detector
                param2=36,           # Sensitivity (Lower values find more faint/imperfect circles)
                minRadius=50,        # Minimum radius of the pucks in your image
                maxRadius=150        # Maximum radius of the pucks in your image
                )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        print(f"Successfully detected {len(circles[0])} pucks")
        
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = int(i[2])
           
           # Handter hvis det går over 1280x720
            if int(center[1])-radius < 0 or int(center[0])-radius <0:
                print("Negative overflow")
                pnkt1 = (int(center[0]-radius),0)
                pnkt2 = (max(0, center[0]+radius), max(0, center[1]+radius))
            elif int(center[0]) + radius > WIDTH or int(center[1]) + radius > HEIGHT:
                print("Positive overflow")
                pnkt1 = (max(0, center[0]-radius), max(0, center[1]-radius))
                pnkt2 = (WIDTH,HEIGHT)
            else:
                pnkt1 = (max(0, center[0]-radius), max(0, center[1]-radius))
                pnkt2 = (max(0, center[0]+radius), max(0, center[1]+radius))
            #cv2.circle(frame, center, radius, (0, 255, 0), 3)
            puck = frame[pnkt1[1]:pnkt2[1], pnkt1[0]:pnkt2[0]]
            
            if puck is not None:
                data, box_points = find_qr(puck)
            ang = 0

            if len(box_points) > 0:

                ang, pnkt = find_angle(box_points)
                print(f"DATA: {data} - angle: {ang}")

                # Frame rundt puck
                # cv2.rectangle(frame,pnkt1, pnkt2, (0,0,255), 3)

                cv2.polylines(puck, [box_points], isClosed=True, color=(0, 255, 0), thickness=3)

                """Tegn linjen til find_angle"""
                # cv2.circle(puck, box_points[0,0], 10, (255, 0, 255), -1)
                # cv2.circle(puck, box_points[1,0], 10, (255, 0, 255), -1)
                # cv2.line(puck, box_points[0,0],box_points[0,0] +pnkt, (0,0,255), 5 )
                data = data[0]
                ang = f"{ang}°"
                draw_text(frame, data[6], int(center[0]+radius), int(center[1]))
                draw_text(frame, ang, int(center[0]- len(ang)*10), int(center[1]))

    return frame

images = ['images/250mm.jpg', 'images/300mm.jpg', 'images/400mm.jpg', 'images/500mm.jpg']
for image in images:
    frame = cv2.imread(image)
    puck_with_qr = find_puck(frame)
    cv2.imshow(image, puck_with_qr)
    cv2.waitKey(0)
cv2.destroyAllWindows()
