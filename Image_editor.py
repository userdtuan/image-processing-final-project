from email.policy import default
import PySimpleGUI as sg
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO
import cv2
from cv2 import threshold     # Thư viện OpenCV
import numpy
from lab1 import *


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

def update_image(windo,original,blur,contrast,emboss,contour,flipx,flipy,cat,thres,threshold):
	global image
	image = original.filter(ImageFilter.GaussianBlur(blur))
	image = image.filter(ImageFilter.UnsharpMask(contrast))

	if emboss:
		image = image.filter(ImageFilter.EMBOSS())
	if contour:
		image = image.filter(ImageFilter.CONTOUR())

	if flipx:
		image = ImageOps.mirror(image)
	if flipy:
		image = ImageOps.flip(image)

	if threshold:
		# print(image)
		# print(pil2cv(image))
		image = dao_anh(pil2cv(image))
		image = cv2pil(image)
	
	if cat:
		if(thres.isnumeric()):
			window['-Cat-'].update(True)
			image = cat_nguong(pil2cv(image),thres)
			image = cv2pil(image)
			print("done")
		else:
			window['-Cat-'].update(False)
			sg.popup('Threshold value is invalid!!!!')



	bio = BytesIO()
	image.save(bio, format = 'PNG')

	window['-IMAGE-'].update(data = bio.getvalue())

image_path = sg.popup_get_file('Open', file_types=(("ALL Files", "."),), default_path="/Users/thanhtuan/Desktop/Images/moon.png")

LAYOUT = sg.Column([
	[sg.Frame('Blur',layout = [[sg.Slider(range = (0,255), orientation = 'h', key = '-BLUR-')]])],
	[sg.Frame('Contrast',layout = [[sg.Slider(range = (0,10), orientation = 'h', key = '-CONTRAST-')]])],
	[sg.Frame('Cắt ngưỡng',layout = [[
		sg.Input(default_text = "", size = (12, 30), key='-Thres-'),
		sg.Checkbox('Apply', key = '-Cat-')
	]])],
	[sg.Checkbox('Emboss', key = '-EMBOSS-'), sg.Checkbox('Contour', key = '-CONTOUR-')],
	[sg.Checkbox('Threshold', key = '-THRESHOLD-')],

	[sg.Checkbox('Flip x', key = '-FLIPX-'), sg.Checkbox('Flip y', key = '-FLIPY-')],
	[sg.Button('Save image', key = '-SAVE-')],])
image_col = sg.Column([[sg.Image(image_path, key = '-IMAGE-')]])
layout = [[LAYOUT,image_col]]

original = Image.open(image_path)
window = sg.Window('Image Editor', layout)

while True:
	event, values = window.read(timeout = 50)
	if event == sg.WIN_CLOSED:
		break

	# if values['-Cat-']:
	# 	window['-Cat-'].update(True)

	update_image(
		window,
		original, 
		values['-BLUR-'],
		values['-CONTRAST-'], 
		values['-EMBOSS-'], 
		values['-CONTOUR-'],
		values['-FLIPX-'],
		values['-FLIPY-'],
		values['-Cat-'],
		values['-Thres-'],
		values['-THRESHOLD-'],
		)

	if event == '-SAVE-':
		save_path = sg.popup_get_file('Save',save_as = True) + '.png'
		image.save(save_path,'PNG')
		
window.close()