from email.policy import default
from pickle import FALSE
import PySimpleGUI as sg
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO
import cv2
import numpy
from lab1 import *
import datetime

image_path = sg.popup_get_file('Open', file_types=(("ALL Files", "."),), default_path="/Users/thanhtuan/Desktop/Images/moon.png")
c_nguong = "null"
backup_cat_nguong = "null"
d_anh = "null"
img_d_anh = "null"
image_temp = ""
# change = False

def update():
	# global change
	# change = "sá"
	print("i")

# def perform_daoanh(image):

	

def log_time():
	log = str(datetime.datetime.now().time())
	return log

LAYOUT = sg.Column([
	[sg.Frame('Blur',layout = [[sg.Slider(range = (0,255), orientation = 'h', key = '-BLUR-')]])],
	[sg.Frame('Contrast',layout = [[sg.Slider(range = (0,10), orientation = 'h', key = '-CONTRAST-')]])],
	[sg.Frame('Cắt ngưỡng',layout = [[
		sg.Input(default_text = "", size = (12, 30), key='-CatNguong-'),
		sg.Checkbox('Apply', key = '-ActiveCatNguong-')
	]])],
	[sg.Checkbox('Emboss', key = '-EMBOSS-'), sg.Checkbox('Contour', key = '-CONTOUR-')],
	[sg.Checkbox('DaoAnh', key = '-DaoAnh-')],

	[sg.Checkbox('Flip x', key = '-FLIPX-'), sg.Checkbox('Flip y', key = '-FLIPY-')],
	[sg.Button('Save image', key = '-SAVE-')],])
image_col = sg.Column([[sg.Image(image_path, key = '-IMAGE-')]])
layout = [[LAYOUT,image_col]]
def pil2cv(pil_img):
	numpy_image=numpy.array(pil_img)  

	# convert to a openCV2 image, notice the COLOR_RGB2BGR which means that 
	# the color is converted from RGB to BGR format
	opencv_image=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR) 
	return opencv_image
def cv2pil(cv_img):
	color_coverted = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
	pil_image=Image.fromarray(color_coverted)
	return pil_image

def update_image(windo,original,blur,contrast,emboss,contour,flipx,flipy,activeCatNg,nguong,daoanh):
	global image, c_nguong, d_anh, backup_cat_nguong, img_d_anh
	# global change
	change = False
	image = original.filter(ImageFilter.GaussianBlur(blur))
	image = image.filter(ImageFilter.UnsharpMask(contrast))

	if daoanh:
		if(change==True):
			temp = image
			temp = dao_anh(pil2cv(temp))
			temp = cv2pil(temp)

			image = temp
			img_d_anh = image

			d_anh = True
			change = False
			print("da")
		elif(d_anh!=True):
			temp = image
			temp = dao_anh(pil2cv(temp))
			temp = cv2pil(temp)

			image = temp
			img_d_anh = image

			d_anh = True
			change = True
			print("da")
		else:
			image = img_d_anh
	else:
		if(d_anh!=False):
			d_anh = False
			change = True
			
	
	if activeCatNg:
		if(change==True):
			temp = image
			if(nguong.isnumeric()):
				window['-ActiveCatNguong-'].update(True)
				temp = cat_nguong(pil2cv(temp),nguong)
				temp = cv2pil(temp)

				image = temp
				backup_cat_nguong = image

				c_nguong = True
				change = False
				print("cn")
			else:
				window['-ActiveCatNguong-'].update(False)
				sg.popup('Threshold value is invalid!!!!')
		elif(c_nguong!=True):
			temp = image
			if(nguong.isnumeric()):
				window['-ActiveCatNguong-'].update(True)
				temp = cat_nguong(pil2cv(temp),nguong)
				temp = cv2pil(temp)

				image = temp
				backup_cat_nguong = image

				c_nguong = True
				change = True
				print("cn")
			else:
				window['-ActiveCatNguong-'].update(False)
				sg.popup('Threshold value is invalid!!!!')
		else:
			image = backup_cat_nguong
	else:
		if(c_nguong!=False):
			c_nguong = False
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



	# print("c_nguong: "+str(c_nguong)+", d_anh: "+str(d_anh))
	# print(str(change))
	bio = BytesIO()
	image.save(bio, format = 'PNG')
	image_temp = image

	window['-IMAGE-'].update(data = bio.getvalue())


original = Image.open(image_path)
window = sg.Window('Image Editor', layout)

while True:
	event, values = window.read(timeout = 50)
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
		)

	if event == '-SAVE-':
		save_path = sg.popup_get_file('Save',save_as = True) + '.png'
		image.save(save_path,'PNG')
		
window.close()