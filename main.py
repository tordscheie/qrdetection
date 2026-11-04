import math as m

import cv2
import numpy as np

WIDTH = 1280
HEIGHT = 720

def scan_for_qr(frame):
    puck_with_qr, qr_codes = find_puck(frame)
    cv2.circle(frame, (WIDTH//2, HEIGHT//2), 10, (0,0,255), -1)
    for qr in qr_codes:
        print("-------------")
        print(qr)
        print("-------------")
    return (puck_with_qr, qr_codes)

class QRCode:
    name:str
    center_x:int
    center_y:int
    ang:int
    quaternion: list()

    def __init__(self,name,center_x, center_y, ang):
        self.name = name
        self.center_x = -(WIDTH//2 - center_x)
        self.center_y = HEIGHT//2 - center_y
        self.ang = ang
        self.quaternion = self.z_degrees_to_quaternion(ang)

    def __str__(self):
        return (
            f"{'Name':<10}: {self.name}\n"
            f"{'Center X':<10}: {self.center_x}\n"
            f"{'Center Y':<10}: {self.center_y}\n"
            f"{'Angle':<10}: {self.ang}°\n"
            f"{'Quaternion':<10}: {self.quaternion}"
        )

    def z_degrees_to_quaternion(self, rotation_z_degrees):
        """Convert a rotation about the z-axis in degrees to Quaternion.
        """
        roll = m.pi
        pitch = 0
        yaw = m.radians(rotation_z_degrees)

        qw = round(m.cos(roll / 2) * m.cos(pitch / 2) * m.cos(yaw / 2) + m.sin(roll / 2) * m.sin(
            pitch / 2) * m.sin(yaw / 2))
        qx = round(m.sin(roll / 2) * m.cos(pitch / 2) * m.cos(yaw / 2) - m.cos(roll / 2) * m.sin(
            pitch / 2) * m.sin(yaw / 2))
        qy = round(m.cos(roll / 2) * m.sin(pitch / 2) * m.cos(yaw / 2) + m.sin(roll / 2) * m.cos(
            pitch / 2) * m.sin(yaw / 2))
        qz = round(m.cos(roll / 2) * m.cos(pitch / 2) * m.sin(yaw / 2) - m.sin(roll / 2) * m.sin(
            pitch / 2) * m.cos(yaw / 2))

        return [qw, qx, qy, qz]



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
        qr_codes = []
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
            puck = frame[pnkt1[1]:pnkt2[1], pnkt1[0]:pnkt2[0]]
            

            if puck is not None:
                data, box_points = find_qr(puck)
            ang = 0

            if len(box_points) > 0:

                ang, pnkt = find_angle(box_points)

                # Frame rundt puck
                # cv2.rectangle(frame,pnkt1, pnkt2, (0,0,255), 3)

                cv2.polylines(puck, [box_points], isClosed=True, color=(0, 255, 0), thickness=3)

                """Tegn linjen til find_angle"""
                # cv2.circle(puck, box_points[0,0], 10, (255, 0, 255), -1)
                # cv2.circle(puck, box_points[1,0], 10, (255, 0, 255), -1)
                # cv2.line(puck, box_points[0,0],box_points[0,0] +pnkt, (0,0,255), 5 )
                data = data[0]
                
                draw_text(frame, data[6], int(center[0]+radius), int(center[1]))

                entry = [data, int(center[0]),int(center[1]), ang]
                new_qr = QRCode(data, int(center[0]),int(center[1]), ang)
                qr_codes.append(new_qr)

                ang = f"{ang}°"
                draw_text(frame, ang, int(center[0]- len(ang)*10), int(center[1]))
    return (frame,(qr_codes))

if __name__ == '__main__':
    image = 'images/400mm.jpg'
    frame = cv2.imread(image)
    puck_with_qr, qr_codes = find_puck(frame)
    cv2.circle(frame, (WIDTH//2, HEIGHT//2), 10, (0,0,255), -1)
    for qr in qr_codes:
        print("-------------")
        print(qr)
        print("-------------")
    cv2.imshow(image, puck_with_qr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
