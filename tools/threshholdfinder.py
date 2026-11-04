import cv2
import numpy as np


def nothing(x):
    pass

# Load your QR code image in grayscale
# REPLACE 'your_image.jpg' with the actual path to your image file
img_gray = cv2.imread('images/300mm.jpg', cv2.IMREAD_GRAYSCALE)
if img_gray is None:
    raise ValueError("Image not found. Please check your file path.")

# Convert back to BGR for drawing color boxes later
img_bgr = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

# Create the window and threshold sliders
cv2.namedWindow('QR Image Sliders')
cv2.createTrackbar('Global Val', 'QR Image Sliders', 125, 255, nothing)
cv2.createTrackbar('Block Size', 'QR Image Sliders', 11, 99, nothing)
cv2.createTrackbar('C Constant', 'QR Image Sliders', 2, 30, nothing)

# Use '0' for Global Thresholding mode, '1' for Adaptive Thresholding mode
cv2.createTrackbar('Mode (0:Glob, 1:Adap)', 'QR Image Sliders', 0, 1, nothing)

# Initialize OpenCV's QR Decoder
qr_detector = cv2.QRCodeDetector()

print("Adjust sliders. A green box will appear when the QR code successfully decodes.")

while True:
    # Read slider parameters
    g_val = cv2.getTrackbarPos('Global Val', 'QR Image Sliders')
    b_size = cv2.getTrackbarPos('Block Size', 'QR Image Sliders')
    c_val = cv2.getTrackbarPos('C Constant', 'QR Image Sliders')
    mode = cv2.getTrackbarPos('Mode (0:Glob, 1:Adap)', 'QR Image Sliders')
    
    # Enforce adaptive rules (Must be odd and >= 3)
    b_size = max(b_size, 3)
    if b_size % 2 == 0: b_size += 1

    # Apply both options
    if mode == 0:
        _, thresh_img = cv2.threshold(img_gray, g_val, 255, cv2.THRESH_BINARY)
    else:
        thresh_img = cv2.adaptiveThreshold(
            img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, b_size, c_val
        )
    
    # Run the QR decoder on your thresholded processing frame
    data, bbox, _ = qr_detector.detectAndDecode(thresh_img)
    
    # Prepare a display matrix (convert threshold to color so we can draw green lines)
    display_canvas = cv2.cvtColor(thresh_img, cv2.COLOR_GRAY2BGR)
    
    # If the threshold is clean enough to decode, highlight it!
    if bbox is not None and len(bbox) > 0:
        bbox = np.int32(bbox)
        for i in range(len(bbox)):
            pt1 = tuple(bbox[i][0])
            pt2 = tuple(bbox[(i + 1) % len(bbox)][0])
            cv2.line(display_canvas, pt1, pt2, (0, 255, 0), 3)
        if data:
            cv2.putText(display_canvas, f"Data: {data}", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
    # Print data directly to terminal line
    print(f"\rMode: {'Global' if mode==0 else 'Adaptive'} | G-Val: {g_val} | B-Size: {b_size} | C: {c_val} | Success: {True if data else False}  ", end="")
    
    # Show the active slider window
    cv2.imshow('QR Image Sliders', display_canvas)
    
    # Press 'q' to close
    if cv2.waitKey(30) & 0xFF == ord('q'):
        print("\nExiting script...")
        break

cv2.destroyAllWindows()
