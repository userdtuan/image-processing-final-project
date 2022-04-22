# https://pythonexamples.org/python-opencv-read-image-cv2-imread/
# https://theailearner.com/2019/01/26/power-law-gamma-transformations/
import cv2
import math
import numpy as np

# print('Image Dimensions :', img.shape)
# Initialize&preparing area
L = 255


def tranf_to_bin(img):
    arr = []
    for i in range(img.shape[0]):
        row = []
        for j in range(img.shape[1]):
            row.append(np.binary_repr(img[i][j], width=8))  # width = no. of bits
        arr.append(row)
    return arr


def bit_plane_slicing(num, arr):
    img = tranf_to_bin(arr)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            bina = img[i][j]
            bit = int(bina[8 - num])
            # arr[i][j] = arr[i][j]*bit*math.pow(2,(8-num))
            # arr[i][j] = bit*math.pow(2,(8-num))
            arr[i][j] = bit * int(math.pow(2, num - 1))
    return arr


###########
def dao_anh(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    wid, hei = img.shape
    # print(img)
    for i in range(wid):
        for j in range(hei):
            # print(img[i][j], end=" ")
            r = img[i][j]
            img[i][j] = L - r
        # print('')
    return img


def cat_nguong(img, nguong):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    wid, hei = img.shape
    # threshold = 10.666
    threshold = float(nguong)
    # print(img)
    for i in range(wid):
        for j in range(hei):
            r = img[i][j]
            if r <= threshold:
                s = 0
            else:
                s = 255
            img[i][j] = s
        # print('')
    return(img)


def keo_dan_do_tuong_phan(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    wid, hei = img.shape
    # threshold = 133
    s_high = 180
    s_low = 136
    print(img)
    for i in range(wid):
        for j in range(hei):
            # print(img[i][j], end=" ")
            r = img[i][j]
            if r == s_high or r == s_low:
                s = r
            elif r < s_low:
                s = r - 65
            elif r > s_high:
                s = r + 10
            elif r > s_low and r < s_high:
                s = r + 30
            img[i][j] = s
        # print('')
    print(img)
    return(img)
    print('Done!')


def log_trans(img, ):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    wid, hei = img.shape
    c = 5
    # print(img)
    for i in range(wid):
        for j in range(hei):
            # print(img[i][j], end=" ")
            r = img[i][j]
            img[i][j] = (c * math.log(1 + r / 255)) * 255
            # temp = round(c*math.log(1+r))
            # print(r, end=" ")
        # print('')
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in img]))
    return(img)
    print('Done!')


def pow_trans(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    wid, hei = img.shape
    c = 1
    y = 0.4
    print(img.max())
    for i in range(wid):
        for j in range(hei):
            # print(img[i][j], end=" ")
            r = img[i][j]
            img[i][j] = (c * pow(r / 255, y)) * 255
        # print('')
    # print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
    #   for row in img]))
    return(img)
    print('Done!')


def cat_lat_mat_bit(img, bit):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # wid, hei = img.shape
    img = bit_plane_slicing(bit, img)
    return(img)
    print('Done!')


def cat_lat_mat_xam(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    wid, hei = img.shape
    threshold = 88
    # print(img)
    for i in range(wid):
        for j in range(hei):
            # print(img[i][j], end=" ")
            r = img[i][j]
            if r <= threshold:
                s = 0
            else:
                s = r
            img[i][j] = s
        # print('')
    return(img)
    print('Done!')


def can_bang_histogram(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # To display image before equalization
    # display(Image.fromarray(img))

    print(img)

    a = np.zeros((256,), dtype=np.float16)
    b = np.zeros((256,), dtype=np.float16)

    height, width = img.shape

    # finding histogram
    for i in range(width):
        for j in range(height):
            g = img[j, i]
            # print(g, end=" ")
            # print("")
            a[g] = a[g] + 1

    print(a)

    # performing histogram equalization
    tmp = 1.0 / (height * width)
    b = np.zeros((256,), dtype=np.float16)

    for i in range(256):
        for j in range(i + 1):
            b[i] += a[j] * tmp
        b[i] = round(b[i] * 255)

    # b now contains the equalized histogram
    b = b.astype(np.uint8)

    # print(b)

    # Re-map values from equalized histogram into the image
    for i in range(width):
        for j in range(height):
            g = img[j, i]
            img[j, i] = b[g]

    return(img)
    print('Done!')