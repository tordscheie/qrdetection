import math as m

import cv2
from pyzbar.pyzbar import decode

from Conversion_funk import find_table_coords

WIDTH = 1280
HEIGHT = 720

class QRCode:
    name:str
    center_x:int
    _center_x:int
    center_y:int
    _center_y:int
    top_left_x:int
    top_left_y:int
    ang:int
    coordinates: list[int]

    def __init__(self,name,points):
        self.name = name
        self._center_x = sum(p.x for p in points) / len(points)
        self._center_y = sum(p.y for p in points) / len(points)
        self.center_x = -(WIDTH//2 - self._center_x)
        self.center_y = HEIGHT//2 - self._center_y
        self.ang = self.find_angle(points[1].x, points[1].y, points[0].x, points[0].y)
        self.coordinates  = find_table_coords(self.center_x, self.center_y, 300)

    def __str__(self):
        return (
            f"{'Name':<10}: {self.name}\n"
            f"{'Center X':<10}: {self.center_x}\n"
            f"{'Center Y':<10}: {self.center_y}\n"
            f"{'Angle':<10}: {self.ang}°\n"
            f"{'Center':<10}: {self.coordinates}\n"
        )

    def find_angle(self, x1,y1, x2,y2):
            """Finder hvor mye linjen fra hjørne oppe i høyre og hjøre oppe i venstre har rotert,
            returnerer grader og hvor lang linjen er
            """
            dx = x2 - x1
            dy = y2 - y1
            ang = 0
            if dx < 0:
                ang = m.atan(dy/dx) +m.pi
            elif dx >0 and dy <0:
                ang = m.atan(dy/dx) + 2*m.pi
            else:
                ang = m.atan(dy/dx)
            
            ang_deg = int(m.degrees(ang))
            return ang_deg

def find_codes(cv2image) -> list[QRCode]:
    codes =[]
    gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    binary_image = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        51,  # Block size (must be an odd number, e.g., 3, 5, 11, 21...)
        5,   # Constant subtracted from the mean
    )
    cv2.imshow("img", binary_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    for barcode in decode(binary_image):
        points = barcode.polygon
        name = barcode.data.decode('utf-8')            
        code = QRCode(name, points)
        codes.append(code)

    return codes




def draw_text(frame, data, x, y):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1  
        thickness = 1
        text_color = (250,0,250)
        cv2.putText(frame, str(data), (int(x + 1),int(y - 4)), font, font_scale, text_color, thickness=thickness, lineType=cv2.LINE_AA)


if __name__ == '__main__':
    images = ['images/250mm.jpg', 'images/300mm.jpg', 'images/400mm.jpg', 'images/500mm.jpg']
   #puck_with_qr, qr_codes = find_puck(frame)
    for image in images:
        frame = cv2.imread(image)
        cv2.circle(frame, (WIDTH//2, HEIGHT//2), 10, (0,0,255), -1)
        codes = find_codes(frame)
        for qr in codes:
            cv2.circle(frame, (int(qr._center_x),int(qr._center_y)), 10, (0,150,150), -1)
            print("-------------")
            print(qr)
            print("-------------")
        cv2.imshow(image, frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
