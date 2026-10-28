import math as m

import cv2


def main():
    cap = cv2.VideoCapture(0)
    cap.set (3 , 1280)
    cap.set (4 , 960)
    
    if not cap.isOpened():
        print("Not able to open")
        exit()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Cant get fram")

        frame = find_qr_code(frame)
        cv2.imshow("Camera feed", frame)

        if cv2.waitKey(1) == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

def find_qr_code(frame):
    """Finds qrkodes in the frame. the input must be 
    a frame cv2 frame bgr format. it returns the frame with the qr kodes marked
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, filtered = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    detector = cv2.QRCodeDetector()
    
    retVal, decoded_info, decoded_points,  _ = detector.detectAndDecodeMulti(filtered)

    if retVal:
        for i, data in enumerate(decoded_info):
            if data:
                pts = decoded_points[i].astype(int).reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=3)

                corners = decoded_points[i].astype(int)
                top_left = corners[0]

                lower_left = corners[3]

                top_right = corners[1]
                lower_right = corners[2]
                
                avg_x = int((top_left[0] + lower_left[0] + top_right[0] + lower_right[0])/4)
                avg_y = int((top_left[1] + lower_left[1] + top_right[1] + lower_right[1])/4)

                dx = top_right[0] - top_left[0]
                dy = top_left[1] - top_right[1]

                ang = 0

                if dx < 0:
                    ang = m.atan(dy/dx) +m.pi
                elif dx >0 and dy <0:
                    ang = m.atan(dy/dx) + 2*m.pi
                else:
                    ang = m.atan(dy/dx)
                
                ang_deg = int(m.degrees(ang))
                print(ang_deg)

                # Text
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 2  
                thickness = 1
                text_color = (0,0,255)
                (text_width, text_height), baseline = cv2.getTextSize(str(ang_deg), font, fontScale=font_scale, thickness=thickness)

                cv2.circle(frame, (avg_x, avg_y), radius=20, color=(0, 0, 255), thickness=-1)
                cv2.line(frame, (top_left), (top_left[0] + dx, top_left[1] - dy), (255, 0, 0), 5)
                cv2.putText(frame, str(ang_deg), (top_left[0] + 1, top_left[1] - 4), font, font_scale, text_color, thickness=thickness, lineType=cv2.LINE_AA)




    return frame

if __name__ == "__main__":
    main()
