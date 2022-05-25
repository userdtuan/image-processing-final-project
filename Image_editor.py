from email.policy import default
from pickle import FALSE
import PySimpleGUI as sg
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO
import cv2
import numpy
from lab1 import *
import datetime

image_path = sg.popup_get_file('Open', file_types=(
    ("ALL Files", "."),), default_path="/Users/thanhtuan/Desktop/Images/moon.png")
check_cat_nguong = "null"
backup_cat_nguong = "null"
check_dao_anh = "null"
backup_dao_anh = "null"
check_tuong_phan = "null"
backup_tuong_phan = "null"
check_log_trans = "null"
backup_log_trans = "null"
check_pow_trans = "null"
backup_pow_trans = "null"
check_cat_lat_mat_bit = "null"
backup_cat_lat_mat_bit = "null"
check_cat_lat_mat_xam = "null"
backup_cat_lat_mat_xam = "null"
check_can_bang_histogram = "null"
backup_can_bang_histogram = "null"
change = False


def update():
    # global change
    # change = "sá"
    print("i")

# def perform_daoanh(image):


def log_time():
    log = str(datetime.datetime.now().time())
    return log


LAYOUT = sg.Column([
    [sg.Frame('Blur', layout=[
              [sg.Slider(range=(0, 255), orientation='h', key='-BLUR-')]])],
    [sg.Frame('Contrast', layout=[
              [sg.Slider(range=(0, 10), orientation='h', key='-CONTRAST-')]])],
    [sg.Frame('Cắt ngưỡng', layout=[[
        sg.Input(default_text="", size=(12, 30), key='-CatNguong-'),
        sg.Checkbox('Apply', key='-ActiveCatNguong-')
    ]])],
    [sg.Frame('Log Transform', layout=[[
        sg.Input(default_text="", size=(12, 30), key='-LogValue-'),
        sg.Checkbox('Apply', key='-ActiveLogTrans-')
    ]])],
    [sg.Frame('Pow Transform', layout=[
        [sg.Text(text="C:"), sg.Input(default_text="",
                                      size=(12, 30), key='-PowCValue-')],
        [sg.Text(text="Y:"), sg.Input(default_text="",
                                      size=(12, 30), key='-PowYValue-')],
        [sg.Checkbox('Apply', key='-ActivePowTrans-')]
    ])],
	[sg.Frame('Bit plane slicing', layout=[[
        # sg.Input(default_text="", size=(12, 30), key='-LogValue-'),
		sg.Combo(['1','2','3','4','5','6','7','8'],default_value='8', size=(10,10), key='-BitValue-'),
        sg.Checkbox('Apply', key='-ActiveBit-')
    ]])],
	[sg.Frame('Gray Plane Slicing', layout=[[
        sg.Input(default_text="", size=(12, 30), key='-GrayValue-'),
        sg.Checkbox('Apply', key='-ActiveGray-')
    ]])],
	
    [sg.Checkbox('Emboss', key='-EMBOSS-', visible=False),
     sg.Checkbox('Contour', key='-CONTOUR-', visible=False)],
    [sg.Checkbox('DaoAnh', key='-DaoAnh-'),
     sg.Checkbox('Keo dan dtp', key='-TuongPhan-')],
	[sg.Checkbox('Histogram Equalization', key='-Histogram-')],
    [sg.Checkbox('Flip x', key='-FLIPX-', visible=False),
     sg.Checkbox('Flip y', key='-FLIPY-', visible=False)],
    [sg.Button('Save image', key='-SAVE-')], ])
image_col = sg.Column([[sg.Image(image_path, key='-IMAGE-')]])
layout = [[LAYOUT, image_col]]


def pil2cv(pil_img):
    numpy_image = numpy.array(pil_img)

    # convert to a openCV2 image, notice the COLOR_RGB2BGR which means that
    # the color is converted from RGB to BGR format
    opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
    return opencv_image


def cv2pil(cv_img):
    color_coverted = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(color_coverted)
    return pil_image


def update_image(windo, original, blur, contrast, emboss, contour, flipx, flipy, activeCatNg, nguong, daoanh, tuongphan, logValue, activeLog, powCValue, powYValue, activePow, bitValue, activeBit, grayValue, activeGray, histogram):
    global image, backup_cat_nguong, backup_dao_anh, backup_tuong_phan, backup_log_trans, backup_pow_trans, backup_cat_lat_mat_bit, backup_cat_lat_mat_xam, backup_can_bang_histogram
    global check_cat_nguong, check_dao_anh, check_tuong_phan, check_log_trans, check_pow_trans, check_cat_lat_mat_bit, check_cat_lat_mat_xam, check_can_bang_histogram
    global change
    # change = False
    image = original.filter(ImageFilter.GaussianBlur(blur))
    image = image.filter(ImageFilter.UnsharpMask(contrast))

    if daoanh:
        if(change == True):
            temp = image
            temp = dao_anh(pil2cv(temp))
            temp = cv2pil(temp)

            image = temp
            backup_dao_anh = image

            check_dao_anh = True
            change = False
            print("da")
        elif(check_dao_anh != True):
            temp = image
            temp = dao_anh(pil2cv(temp))
            temp = cv2pil(temp)

            image = temp
            backup_dao_anh = image

            check_dao_anh = True
            change = True
            print("da")
        else:
            image = backup_dao_anh
    else:
        if(check_dao_anh != False):
            check_dao_anh = False
            change = True
	

    if histogram:
        if(change == True):
            temp = image
            temp = can_bang_histogram(pil2cv(temp))
            temp = cv2pil(temp)

            image = temp
            backup_can_bang_histogram = image

            check_can_bang_histogram = True
            change = False
            print("hi")
        elif(check_can_bang_histogram != True):
            temp = image
            temp = can_bang_histogram(pil2cv(temp))
            temp = cv2pil(temp)

            image = temp
            backup_can_bang_histogram = image

            check_can_bang_histogram = True
            change = True
            print("hi")
        else:
            image = backup_can_bang_histogram
    else:
        if(check_can_bang_histogram != False):
            check_can_bang_histogram = False
            change = True

    if activePow:
        if(change == True):
            temp = image
            if(powCValue.isnumeric()):
                if(powYValue != ""):
                    window['-ActivePowTrans-'].update(True)
                    temp = pow_trans(pil2cv(temp), powCValue, powYValue)
                    temp = cv2pil(temp)

                    image = temp
                    backup_pow_trans = image

                    check_pow_trans = True
                    change = False
                    print("pt")
            else:
                window['-ActivePowTrans-'].update(False)
                sg.popup('Check if C and Y value is valid!!!!')
        elif(check_pow_trans != True):
            temp = image
            if(powCValue.isnumeric()):
                window['-ActivePowTrans-'].update(True)
                temp = pow_trans(pil2cv(temp), powCValue, powYValue)
                temp = cv2pil(temp)

                image = temp
                backup_pow_trans = image

                check_pow_trans = True
                change = True
                print("pt")
            else:
                window['-ActivePowTrans-'].update(False)
                sg.popup('Check if C and Y value is valid!!!!')
        else:
            image = backup_pow_trans
    else:
        if(check_pow_trans == True):
            check_pow_trans = False
            change = True

    if activeGray:
        if(change == True):
            temp = image
            if(grayValue.isnumeric()):
                window['-ActiveGray-'].update(True)
                temp = cat_lat_mat_xam(pil2cv(temp), grayValue)
                temp = cv2pil(temp)

                image = temp
                backup_cat_lat_mat_xam = image

                check_cat_lat_mat_xam = True
                change = False
                print("gray")
            else:
                window['-ActiveGray-'].update(False)
                sg.popup('Gray value is invalid!!!!')
        elif(check_cat_lat_mat_xam != True):
            temp = image
            if(grayValue.isnumeric()):
                window['-ActiveGray-'].update(True)
                temp = cat_lat_mat_xam(pil2cv(temp), grayValue)
                temp = cv2pil(temp)

                image = temp
                backup_cat_lat_mat_xam = image

                check_cat_lat_mat_xam = True
                change = True
                print("gray")
            else:
                window['-ActiveGray-'].update(False)
                sg.popup('Gray value is invalid!!!!')
        else:
            image = backup_cat_lat_mat_xam
    else:
        if(check_cat_lat_mat_xam == True):
            check_cat_lat_mat_xam = False
            change = True


    if tuongphan:
        if(change == True):
            temp = image
            temp = keo_dan_do_tuong_phan(pil2cv(temp))
            temp = cv2pil(temp)

            image = temp
            backup_tuong_phan = image

            check_tuong_phan = True
            change = False
            print("tp")
        elif(check_tuong_phan != True):
            temp = image
            temp = keo_dan_do_tuong_phan(pil2cv(temp))
            temp = cv2pil(temp)

            image = temp
            backup_tuong_phan = image

            check_tuong_phan = True
            change = True
            print("tp")
        else:
            image = backup_tuong_phan
    else:
        if(check_tuong_phan != False):
            check_tuong_phan = False
            change = True

    if activeLog:
        if(change == True):
            temp = image
            if(logValue.isnumeric()):
                window['-ActiveLogTrans-'].update(True)
                temp = log_trans(pil2cv(temp), logValue)
                temp = cv2pil(temp)

                image = temp
                backup_log_trans = image

                check_log_trans = True
                change = False
                print("lt")
            else:
                window['-ActiveLogTrans-'].update(False)
                sg.popup('Logarit value is invalid!!!!')
        elif(check_log_trans != True):
            temp = image
            if(logValue.isnumeric()):
                window['-ActiveLogTrans-'].update(True)
                temp = log_trans(pil2cv(temp), logValue)
                temp = cv2pil(temp)

                image = temp
                backup_log_trans = image

                check_log_trans = True
                change = True
                print("lt")
            else:
                window['-ActiveLogTrans-'].update(False)
                sg.popup('Logarit value is invalid!!!!')
        else:
            image = backup_log_trans
    else:
        if(check_log_trans == True):
            check_log_trans = False
            change = True


    if activeBit:
        if(change == True):
            temp = image
            if(bitValue.isnumeric()):
                window['-ActiveBit-'].update(True)
                temp = cat_lat_mat_bit(pil2cv(temp), bitValue)
                temp = cv2pil(temp)

                image = temp
                backup_cat_lat_mat_bit = image

                check_cat_lat_mat_bit = True
                change = False
                print("bit")
            else:
                window['-ActiveBit-'].update(False)
                sg.popup('Bit value is invalid!!!!')
        elif(check_cat_lat_mat_bit != True):
            temp = image
            if(bitValue.isnumeric()):
                window['-ActiveBit-'].update(True)
                temp = cat_lat_mat_bit(pil2cv(temp), bitValue)
                temp = cv2pil(temp)

                image = temp
                backup_cat_lat_mat_bit = image

                check_cat_lat_mat_bit = True
                change = True
                print("bit")
            else:
                window['-ActiveBit-'].update(False)
                sg.popup('Bit value is invalid!!!!')
        else:
            image = backup_cat_lat_mat_bit
    else:
        if(check_cat_lat_mat_bit == True):
            check_cat_lat_mat_bit = False
            change = True


    if activeCatNg:
        if(change == True):
            temp = image
            if(nguong.isnumeric()):
                window['-ActiveCatNguong-'].update(True)
                temp = cat_nguong(pil2cv(temp), nguong)
                temp = cv2pil(temp)

                image = temp
                backup_cat_nguong = image

                check_cat_nguong = True
                change = False
                print("cn")
            else:
                window['-ActiveCatNguong-'].update(False)
                sg.popup('Threshold value is invalid!!!!')
        elif(check_cat_nguong != True):
            temp = image
            if(nguong.isnumeric()):
                window['-ActiveCatNguong-'].update(True)
                temp = cat_nguong(pil2cv(temp), nguong)
                temp = cv2pil(temp)

                image = temp
                backup_cat_nguong = image

                check_cat_nguong = True
                change = True
                print("cn")
            else:
                window['-ActiveCatNguong-'].update(False)
                sg.popup('Threshold value is invalid!!!!')
        else:
            image = backup_cat_nguong
    else:
        if(check_cat_nguong == True):
            check_cat_nguong = False
            change = True

        # change = False

    if emboss:
        image = image.filter(ImageFilter.EMBOSS())

    if contour:
        image = image.filter(ImageFilter.CONTOUR())

    if flipx:
        image = ImageOps.mirror(image)
    if flipy:
        image = ImageOps.flip(image)

    # print("check_cat_nguong: "+str(check_cat_nguong)+", check_dao_anh: "+str(check_dao_anh))
    # print(str(change))
    bio = BytesIO()
    image.save(bio, format='PNG')

    window['-IMAGE-'].update(data=bio.getvalue())


original = Image.open(image_path)
window = sg.Window('Image Editor', layout)

while True:
    event, values = window.read(timeout=50)
    if event == sg.WIN_CLOSED:
        break

    # if values['-ActiveCatNguong-']:
    # 	window['-ActiveCatNguong-'].update(True)

    update_image(
        window,
        original,
        values['-BLUR-'],
        values['-CONTRAST-'],
        values['-EMBOSS-'],
        values['-CONTOUR-'],
        values['-FLIPX-'],
        values['-FLIPY-'],
        values['-ActiveCatNguong-'],
        values['-CatNguong-'],
        values['-DaoAnh-'],
        values['-TuongPhan-'],
        values['-LogValue-'],
        values['-ActiveLogTrans-'],
        values['-PowCValue-'],
        values['-PowYValue-'],
        values['-ActivePowTrans-'],
		values['-BitValue-'],
        values['-ActiveBit-'],
		values['-GrayValue-'],
        values['-ActiveGray-'],
		values['-Histogram-'],
    )

    if event == '-SAVE-':
        save_path = sg.popup_get_file('Save', save_as=True) + '.png'
        image.save(save_path, 'PNG')

window.close()
