import cv2
import numpy as np

def nothing(x):
	pass

def get_average_pixel_width(array):
	return np.average(np.array(array))

cv2.namedWindow('Trackbar')
cv2.createTrackbar('low_h','Trackbar',0,255,nothing)
cv2.createTrackbar('low_s','Trackbar',0,255,nothing)
cv2.createTrackbar('low_v','Trackbar',0,255,nothing)

cv2.createTrackbar('up_h','Trackbar',255,255,nothing)
cv2.createTrackbar('up_s','Trackbar',255,255,nothing)
cv2.createTrackbar('up_v','Trackbar',255,255,nothing)

cap = cv2.VideoCapture(1)
pixel_width_array = [-1]
is_saving_pixel_width = False
while True:
	ret,picture = cap.read()
	hsv = cv2.cvtColor(picture,cv2.COLOR_BGR2HSV)
	low_h = cv2.getTrackbarPos('low_h','Trackbar')
	low_s = cv2.getTrackbarPos('low_s','Trackbar')
	low_v = cv2.getTrackbarPos('low_v','Trackbar')

	up_h = cv2.getTrackbarPos('up_h','Trackbar')
	up_s = cv2.getTrackbarPos('up_s','Trackbar')
	up_v = cv2.getTrackbarPos('up_v','Trackbar')
	#lower_hsvRange = np.array([low_h,low_s,low_v])
	#upper_hsvRange = np.array([up_h,up_s,up_v])

	lower_hsvRange = np.array([40, 58, 129])
	upper_hsvRange = np.array([77, 255, 255])
	hsv = cv2.inRange(hsv,lower_hsvRange,upper_hsvRange)
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

	hsv = cv2.morphologyEx(hsv,cv2.MORPH_CLOSE,kernel)
	hsv = cv2.medianBlur(hsv,5)
	blurred = cv2.GaussianBlur(hsv,(5,5),0)
	contours, hierarchy = cv2.findContours(blurred,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
	c = max(contours, key = cv2.contourArea)
	rect = cv2.minAreaRect(c)
	box = cv2.boxPoints(rect)
	box = np.int0(box)
	picture = cv2.drawContours(picture,[box],0,(0,0,255),2)
	try:
		KNOWN_DISTANCE = 300
		KNOWN_WIDTH = 130
		r = rect[1][0]
		f = 686.8700232872596
		print(is_saving_pixel_width)
		if(cv2.waitKey(1) == ord('s') and not is_saving_pixel_width):
			is_saving_pixel_width = True
		elif(cv2.waitKey(1) == ord('s') and is_saving_pixel_width):
			is_saving_pixel_width = False
		if(is_saving_pixel_width):
			print("saving info")
			pixel_width_array.append(r)
		else:
			d = (f * KNOWN_WIDTH) / get_average_pixel_width(pixel_width_array)
			print("The distance from camera is:" + str(d + 10) + " millimeters")
		#f = (rect[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
		#print("The focal distance from camera is:" + str(f))
		#d = (f * KNOWN_WIDTH) / r
		#print("The distance from camera is:" + str(d + 10) + " millimeters")
	except:
		print('error')
		pass
	cv2.imshow('picture', picture)
	cv2.imshow('hsv', hsv)
	cv2.imshow('blurred', blurred)
	if(cv2.waitKey(1) == ord('q')):
		break
cv2.destroyAllWindows()

