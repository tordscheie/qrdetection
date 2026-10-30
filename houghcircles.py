import cv2
import numpy as np


def nothing(x):
    pass

# Load image and convert to grayscale
img = cv2.imread('images/300mm.jpg')
if img is None:
    raise ValueError("Image not found")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Blurring is critical for Hough Circles to remove edge noise
gray = cv2.medianBlur(gray, 5)

cv2.namedWindow('Hough Circles Finder')

# Create trackbars for HoughCircles parameters
# dp: Inverse ratio of the accumulator resolution to the image resolution (scaled by 10)
cv2.createTrackbar('dp (x10)', 'Hough Circles Finder', 10, 50, nothing) 
# minDist: Minimum distance between the centers of the detected circles
cv2.createTrackbar('minDist', 'Hough Circles Finder', 50, 500, nothing)
# param1: Higher threshold passed to the Canny edge detector
cv2.createTrackbar('param1', 'Hough Circles Finder', 100, 300, nothing)
# param2: Accumulator threshold for the circle centers at the detection stage
cv2.createTrackbar('param2', 'Hough Circles Finder', 30, 200, nothing)
# minRadius: Minimum circle radius
cv2.createTrackbar('minRadius', 'Hough Circles Finder', 10, 200, nothing)
# maxRadius: Maximum circle radius
cv2.createTrackbar('maxRadius', 'Hough Circles Finder', 100, 500, nothing)

while True:
    # Clone the original image so we draw circles on a clean canvas each frame
    display_img = img.copy()
    
    # Get current trackbar positions
    dp = cv2.getTrackbarPos('dp (x10)', 'Hough Circles Finder') / 10.0
    min_dist = cv2.getTrackbarPos('minDist', 'Hough Circles Finder')
    p1 = cv2.getTrackbarPos('param1', 'Hough Circles Finder')
    p2 = cv2.getTrackbarPos('param2', 'Hough Circles Finder')
    min_r = cv2.getTrackbarPos('minRadius', 'Hough Circles Finder')
    max_r = cv2.getTrackbarPos('maxRadius', 'Hough Circles Finder')
    
    # Safeguards: OpenCv will crash if dp, minDist, or param1 are 0
    if dp == 0: dp = 0.1
    if min_dist == 0: min_dist = 1
    if p1 == 0: p1 = 1
    if p2 == 0: p2 = 1
    if max_r <= min_r: max_r = min_r + 1

    # Run the circle detection
    circles = cv2.HoughCircles(
        gray, 
        cv2.HOUGH_GRADIENT, 
        dp=dp, 
        minDist=min_dist, 
        param1=p1, 
        param2=p2, 
        minRadius=min_r, 
        maxRadius=max_r
    )
    
    # Draw detected circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Draw outer circle (green)
            cv2.circle(display_img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Draw center point (red)
            cv2.circle(display_img, (i[0], i[1]), 2, (0, 0, 255), 3)
            
    cv2.imshow('Hough Circles Finder', display_img)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
