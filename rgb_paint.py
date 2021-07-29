#!/usr/bin/env	python3

# To create a paint application with adjustable colors and brush 
# radiius using trackbars. 

import numpy as np
import sys, time
import cv2 as cv

drawing = False		# to be tracked by mouse
radius = 0
color = [0, 0, 0]

def nothing(x):
	pass
class Trackme:
	def __init__(self, img_array, image, rgb_colors):
		self.img_array = img_array
		self.image = image
		self.rgb_colors = rgb_colors

	def create(self):			# creating Trackbars
		cv.createTrackbar('R', self.image, 0, 255, nothing)
		cv.createTrackbar('G', self.image, 0, 255, nothing)
		cv.createTrackbar('B', self.image, 0, 255, nothing)
		cv.createTrackbar('radius', self.image, 0, 255, nothing)

	def run(self):				# tracking position of trackbars
		global radius
		self.rgb_colors[0] = cv.getTrackbarPos('R', self.image)
		self.rgb_colors[1] = cv.getTrackbarPos('G', self.image)
		self.rgb_colors[2] = cv.getTrackbarPos('B', self.image)
		radius = cv.getTrackbarPos('radius', self.image)
		self.img_array[:] = [self.rgb_colors[0], self.rgb_colors[1], self.rgb_colors[2]]

# mouse callback function
def draw_circle(event, x, y, flags, param):
	global drawing, radius, color

	if event == cv.EVENT_LBUTTONDOWN:
		drawing = True
	elif event == cv.EVENT_MOUSEMOVE:
		if drawing == True:
			cv.circle(img, (x, y), radius, tuple(color), -1)
	elif event == cv.EVENT_LBUTTONUP:
		drawing = False
		cv.circle(img, (x, y), radius, tuple(color), -1)

length = 1024
breadth = 512

img = np.zeros((breadth ,length , 3), np.uint8)		# start with black background by commenting below this statement
img.view()[:,:,:] = 255				# start with white background 

# to design a userdefine screen
if sys.argv == 3:
	length, breadth = int(sys.argv[1]), int(sys.argv[2])
	img = np.zeros((512, 1024, 3), np.uint8)

painting_area = img.view()[:, 0:(length - 100)] # giving space to paint and color show
color_adjustment = img.view()[:, (length - 100): ]


# naming window
cv.namedWindow('image')
cv.setMouseCallback('image', draw_circle)			# calling mouse to draw image

tracked = Trackme(color_adjustment, 'image', color)
tracked.create()

while (1):
	cv.imshow('image', img)
	k = cv.waitKey(1) & 0xff
	if k == 27:						# exit if user press esc
		break
	elif k == ord('s'):				# save image if user press s
		image_name = time.ctime() + '.png'
		cv.imwrite(image_name, painting_area)
		break
	tracked.run()
	
cv.destroyAllWindows()
