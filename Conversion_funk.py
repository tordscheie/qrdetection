
import cv2
import numpy as np


def find_table_coords (x_image, y_image, z):
    P1_table = [100, 100]
    P2_table = [0, 100]
    P3_table = [0, 0]
    P4_table = [100, -100]

    # --- 250mm ---
    img_250_puck5_1 = [-436, 236]
    img_250_puck5_2 = [-416, -216]
    img_250_puck3   = [32, -200]
    img_250_puck7   = [472, 274]

    # --- 300mm ---
    img_300_puck5_1 = [-370, 210]
    img_300_puck5_2 = [-354, -178]
    img_300_puck3   = [32, -168]
    img_300_puck7   = [408, 238]

    # --- 400mm ---
    img_400_puck5_1 = [-280, 170]
    img_400_puck5_2 = [-264, -128]
    img_400_puck3   = [30, -120]
    img_400_puck7   = [318, 190]

    # --- 500mm ---
    img_500_puck5_1 = [-226, 144]
    img_500_puck5_2 = [-214, -94]
    img_500_puck3   = [30, -90]
    img_500_puck7   = [268, 166]


    # Table coordinates
    P_t_chad = np.array([
        P1_table,
        P2_table,
        P3_table,
        P4_table
    ], dtype=np.float32)

    # Image coordinates
    P_i_250 = np.array([
        img_250_puck5_1,
        img_250_puck5_2,
        img_250_puck3,
        img_250_puck7
    ], dtype=np.float32)

    P_i_300 = np.array([
        img_300_puck5_1,
        img_300_puck5_2,
        img_300_puck3,
        img_300_puck7
    ], dtype=np.float32)

    P_i_400 = np.array([
        img_400_puck5_1,
        img_400_puck5_2,
        img_400_puck3,
        img_400_puck7
    ], dtype=np.float32)

    P_i_500 = np.array([
        img_500_puck5_1,
        img_500_puck5_2,
        img_500_puck3,
        img_500_puck7
    ], dtype=np.float32)

    # Calculate projective transformation matrices
    H250, _ = cv2.findHomography(P_i_250, P_t_chad)
    H300, _ = cv2.findHomography(P_i_300, P_t_chad)
    H400, _ = cv2.findHomography(P_i_400, P_t_chad)
    H500, _ = cv2.findHomography(P_i_500, P_t_chad)

    # Finding Table coords
    if z == 250:
        H = H250
    elif z== 300:
        H = H300
    elif z== 400:
        H = H400
    elif z== 500:
        H= H500
    else:
        print('Not very accurate positions, due to lack of calibration at this z-level')
        H = ((500-z)/(500-300))*H300 + ((z-300)/(500-300))*H500;
    # Regner ut x og y på bordet
    puck_pixel = np.array([[[x_image, y_image]]], dtype=np.float32)  # shape must be (1, 1, 2)
    table_coord = cv2.perspectiveTransform(puck_pixel, H)
    table_coord = np.round(table_coord, 2)
    table_coord = table_coord[0,0]

    table_coord = [int(table_coord[0]), int(table_coord[1]), 0]
    ## Kan returnere disse heller
    # x_table = table_coord[0]
    # y_table = table_coord[1]
    return table_coord



if __name__ == '__main__':
    x = find_table_coords(472, 274, 250)
    # print(f'x: {x} \n y: {y}')
    print(f'table coordinate: {x}')
