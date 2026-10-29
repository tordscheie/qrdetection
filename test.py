import cv2
import numpy as np

from main import find_qr_code


def find(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detector = cv2.wechat_qrcode_WeChatQRCode()
    blur = cv2.GaussianBlur(gray, (5, 5), 2.0)
    _, filtered = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#    detector.setScaleFactor(1.0) 
    data_list, points_list = detector.detectAndDecode(filtered) 

    if len(data_list) > 0:
        for i, points in enumerate(points_list):
            # Convert the float32 points from WeChat into integer coordinates
            box_points = np.int32(points).reshape((-1, 1, 2))
            
            # Draw the bounding square
            cv2.polylines(frame, [box_points], isClosed=True, color=(0, 255, 0), thickness=3)
            
            # Write decoded text on screen
            x, y = int(points[0][0]), int(points[0][1])
            cv2.putText(frame, f"Data: {data_list[i]}", (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        return frame

image = cv2.imread('images/300mm.jpg')
frame = find_qr_code(image)
cv2.imshow('Pop-up Display Window', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
