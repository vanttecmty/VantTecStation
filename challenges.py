import Jetson.dbscan_contours
import math
import pathfindingv2 as pathfinding
from pathfinding import closest_node
from scipy import spatial
import numpy as np
import sys
sys.path.append('/usr/local/lib/python3.4/site-packages/')
import cv2

class Autonomous_Navigation:

	def __init__(self):
		self.red_lower_bounds=[]
		self.red_upper_bounds=[]
		with open('red_bounds.txt', 'r') as f:
			content = f.readlines()
		content = [x.strip('\n') for x in content]	
		for line in content:
			split=line.split(',')
			#print(split)
			if (len(split)>1):
				self.red_lower_bounds.append(np.array([float(split[0]),float(split[1]),float(split[2])]))
				self.red_upper_bounds.append(np.array([float(split[3]),float(split[4]),float(split[5])]))
		

		self.green_lower_bounds=[]
		self.green_upper_bounds=[]
		with open('green_bounds.txt', 'r') as f:
			content = f.readlines()
		content = [x.strip('\n') for x in content]	
		for line in content:
			split=line.split(',')
			if (len(split)>1):
				self.green_lower_bounds.append(np.array([float(split[0]),float(split[1]),float(split[2])]))
				self.green_upper_bounds.append(np.array([float(split[3]),float(split[4]),float(split[5])]))

	def get_destination(self,image):
		h,w,c=image.shape
		red_binary=np.zeros((h,w),dtype=np.uint8)
		green_binary=np.zeros((h,w),dtype=np.uint8)
		image2=image.copy()
		hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
		kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
		for i,lower in enumerate(self.green_lower_bounds):
			green_hsv_filtered=cv2.inRange(hsv,lower,self.green_upper_bounds[i])
			#print(lower)
			#print(self.green_upper_bounds[i])
			green1 = cv2.morphologyEx(green_hsv_filtered, cv2.MORPH_OPEN, kernel)
			green_binary=np.bitwise_or(green_binary,green1)


		for i,lower in enumerate(self.red_lower_bounds):
			#print(lower)
			#print(self.red_upper_bounds[i])
			red_hsv_filtered=cv2.inRange(image,lower,self.red_upper_bounds[i])
			red1 = cv2.morphologyEx(red_hsv_filtered, cv2.MORPH_OPEN, kernel)
			red_binary=np.bitwise_or(red_binary,red1)

		red_contours=cv2.findContours(red_binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		green_contours=cv2.findContours(green_binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		binary=np.bitwise_or(green_binary,red_binary)
		foundRed=False
		foundGreen=False
		if len(red_contours[1])>=1:

			red_area_max=0
			#Find 2 biggest areas
			biggest_red=None
			for contorno in red_contours[1]:
				#print('Contour len:',len(contorno))
				area=cv2.contourArea(contorno)
				x1,y1,dx1,dy1 = cv2.boundingRect(contorno)
				#print('Area:',area)
				if area>2 and y1>120:
					if area>red_area_max:
						red_area_max=area
						biggest_red=contorno
						foundRed=True

		if len(green_contours[1])>=1:

			green_area_max=0
			#Find 2 biggest areas
			biggest_green=None
			for contorno in green_contours[1]:
				#print('Contour len:',len(contorno))
				area=cv2.contourArea(contorno)
				#print('Area:',area)
				if area>20:
					if area>green_area_max:
						green_area_max=area
						biggest_green=contorno
						foundGreen=True
					

		if foundRed:
			x1,y1,dx1,dy1 = cv2.boundingRect(biggest_red)
			#print(x1+dx1,y1+dy1)
			cv2.rectangle(image2,(x1,y1),(x1+dx1,y1+dy1),(0,0,255),-1,8)
			
		if foundGreen:
			x2,y2,dx2,dy2=cv2.boundingRect(biggest_green)
			#print(x2+dx2,y2+dy2)
			cv2.rectangle(image2,(x2,y2),(x2+dx2,y2+dy2),(0,255,0),-1,8)

		#cv2.waitKey(0)
		if foundRed and foundGreen:
			x=int((x1+x2)/2)
			y=int((y1+y2)/2)
			cv2.circle(image2,(x,y),10,(255,255,255),-1,8)
			#cv2.imshow('image2',image2)
			return foundRed,foundGreen,x,y,image2
		else:
			if foundRed:
				x=x1
				y=y1
				cv2.circle(image2,(x,y),10,(255,255,255),-1,8)
				#cv2.imshow('image2',image2)
			elif foundGreen:
				x=x2
				y=y2
				cv2.circle(image2,(x,y),10,(255,255,255),-1,8)
				#cv2.imshow('image2',image2)
				return foundRed,foundGreen,x,y,image2

				

		return False,False,0,0,image2
		
class Speed_Challenge:

	def get_entrance(self,image):
		obstacles,centroid=dbscan_contours.get_obstacles(image,'rg',True,'A2') #Get a centroid of all red and green obstacles	
		x=int(centroid[0]*math.cos(centroid[1]))
		y=int(centroid[0]*math.sin(centroid[1]))
		return [centroid[0],centroid[1],(x,y)] #return distance, degrees and pixels for map image

	def get_blue_buoy(self,image):
		obstacles,centroid=dbscan_contours.get_obstacles(image,'b',False,'A2') #Get a centroid of all red and green obstacles	
		x=int(centroid[0]*math.cos(centroid[1]))
		y=int(centroid[0]*math.sin(centroid[1]))
		return [centroid[0],centroid[1],(x,y)] #return distance, degrees and pixels for map image

class Find_The_Path:
	
	def get_route_from_obstacles(self,boat_map):
		mapa=cv2.cvtColor(boat_map, cv2.COLOR_BGR2GRAY)
		contornos=cv2.findContours(array,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		distance_matrix=np.zeros((len(contours),len(contours)),dtype=np.float32)
		if len(contours)>1:
			centroids=np.zeros((len(contours),2),dtype=np.uint32)
			for i,contorno in enumerate(contours):
				#agregar condicion de area aqui para filtrar muy pequenos?
				M1 = cv2.moments(contorno)
				if (M1['m00']==0):
					M1['m00']=1
				cx1 = int(M1['m10']/M1['m00'])
				cy1 = int(M1['m01']/M1['m00'])
				centroids[i]=[cy1,cx1]

			distance_matrix=np.zeros((len(contours),len(contours)),dtype=np.float32)
			#print centroids
			for A in range(0,len(contours)):
				for B in range(A+1,len(contours)):
				
					pointA=centroids[A]
					pointB=centroids[B]
					#print pointA, pointB
					dist=spatial.distance.chebyshev(pointA, pointB)
					distance_matrix[A][B]=dist
					distance_matrix[B][A]=dist
		
				distance_matrix[A][A]=999

			#print(distance_matrix)

			links=np.argwhere(distance_matrix<epsylon)
		
			segmentation_vector=np.zeros(len(contours),dtype=np.uint8)

			counter=1
			for i,link in enumerate(links):
				#print 'iteration ', i
				point1=centroids[link[0]]
				point2=centroids[link[1]]
				cv2.line(mapa,(pointA[0],pointA[1]),(pointA[0],pointA[1]),255,2,8)


			destination=np.average(centroids,0)

			if (mapa[destination[0]][destination[1]]==255):
				free=np.argwhere(mapa==0)
				destination=closest_node(destination,free)

			h,w=mapa.shape
			ruta=pathfinding.a_star([int(h/2),int(w/2)],destination,mapa)

			return ruta

class Automated_Docking:


	def __init__(self):
		#Load the hu moments of the numbers.
		self.number1=np.load('one.npy')
		self.number2=np.load('two.npy')
		self.number3=np.load('three.npy')
		self.display1=np.load('display_one.npy')
		self.display2=np.load('display_two.npy')
		self.display3=np.load('display_three.npy')

	def search_dock(self,image,number):
		#gauss_blur = cv2.GaussianBlur(image,(3,3),0)
		'''
		whilte_lower=np.array([178.221468975,136.299067782,121.926975594])
		white_upper=np.array([213.790676774,170.637504418,156.587194446])
		white_image=cv2.inRange(image,whilte_lower,white_upper)
		median_blur = cv2.medianBlur(image,5)
		#cv2.imshow('white',white_image)
		'''
		
		gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		#gaussian_adaptive5 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,30)
		#gaussian_adaptive7 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,19,30)
		#gaussian_adaptive9 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,30)
		gaussian_adaptive11 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,30)
		##cv2.imshow('Adaptive 5',gaussian_adaptive5)
		##cv2.imshow('Adaptive 7',gaussian_adaptive7)
		##cv2.imshow('Adaptive 9',gaussian_adaptive9)
		#cv2.imshow('Adaptive 11',gaussian_adaptive11)
		kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
		gaussian_open = cv2.morphologyEx(gaussian_adaptive11, cv2.MORPH_OPEN, kernel)
		#cv2.imshow('opening',gaussian_open)
		#cv2.imshow('image',image)

		contours=cv2.findContours(gaussian_open,cv2.RETR_LIST ,cv2.CHAIN_APPROX_NONE)
		copy=np.full(image.shape,255,dtype=np.uint8)
		#print(contours[1])

		best_one=10
		best_two=10
		best_three=10
		if len(contours[1])>1:
			for contorno in contours[1]:
				save=False
				if save:
					copy=np.full(image.shape,255,dtype=np.uint8)
				epsilon = 0.1*cv2.arcLength(contorno,True)
				approx = cv2.approxPolyDP(contorno,epsilon,True)
				#print(len(approx))
				area=cv2.contourArea(contorno)
				#print('area:',area)
				value1=cv2.matchShapes(contorno, self.number1, 3, 0.0)
				value2=cv2.matchShapes(contorno, self.number2, 3, 0.0)
				value3=cv2.matchShapes(contorno, self.number3, 3, 0.0)
				
				
				if area>100 and save:
					cv2.drawContours(copy, contorno, -1, (0,0,255), 1)
					#cv2.imshow('copy',copy)
					tecla=cv2.waitKey(0)
					if tecla==49:
						np.save('one',contorno)
					if tecla==50:
						np.save('two',contorno)
					if tecla==51:
						np.save('three',contorno)
				
				#For method 1, <0.2 is really good
				x,y,dx,dy=cv2.boundingRect(contorno)
				y_threshold=250
				y_threshold2=320 #p #pixels
				area_threshold=80
				cv2.line(copy,(0,y_threshold),(640,y_threshold),(255,0,0),1,8)
				cv2.line(copy,(0,y_threshold2),(640,y_threshold2),(255,0,0),1,8)
				if value1<0.1 and y>y_threshold and y<y_threshold2 and area>area_threshold:
					print('Area',area)
					x,y,dx,dy=cv2.boundingRect(contorno)
					if (dx/dy)>0.5 and (dy/dx)<1.5:
						if value1<best_one:
							best_one=value1
							cv2.rectangle(image,(x,y),(x+dx,y+dy),(0,0,255),1,8)
							print('Found 1:',value1)				
							cv2.drawContours(copy, contorno, -1, (0,0,255), 1)
							#cv2.imshow('copy',copy)

				if value2<0.36 and y>y_threshold and y<y_threshold2 and area>area_threshold:
					print('Area',area)
					x,y,dx,dy=cv2.boundingRect(contorno)
					if (dx/dy)>0.5 and (dy/dx)<1.5:
						if value2<best_two:
							best_two=value2
							cv2.rectangle(image,(x,y),(x+dx,y+dy),(0,0,255),1,8)
							print('Found 2:',value2)
							cv2.drawContours(copy, contorno, -1, (0,0,255), 1)
							#cv2.imshow('copy',copy)

				if value3<0.3 and y>y_threshold and y<y_threshold2 and area>area_threshold:
					print('Area',area)
					x,y,dx,dy=cv2.boundingRect(contorno)
					if (dx/dy)>0.5 and (dy/dx)<1.5:
						if value3<best_three:
							best_three=value3
							cv2.rectangle(image,(x,y),(x+dx,y+dy),(0,0,255),1,8)
							print('Found 3:',value3)				
							cv2.drawContours(copy, contorno, -1, (0,0,255), 1)
							#cv2.imshow('copy',copy)
		print('Next image')
		#cv2.imshow('image',image)
		#cv2.waitKey(0)




	def search_number(self,image):
			#gauss_blur = cv2.GaussianBlur(image,(3,3),0)
			display_lower=np.array([29.8650178473,36.675463695,199.112560985])
			display_upper=np.array([86.0516488194,72.1023140828,264.304105682])
			hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
			display_image=cv2.inRange(hsv,display_lower,display_upper)
			median_blur = cv2.medianBlur(image,5)
			#cv2.imshow('Display',display_image)
			
			
			gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
			#gaussian_adaptive5 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,30)
			#gaussian_adaptive7 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,19,30)
			#gaussian_adaptive9 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,30)
			gaussian_adaptive11 = cv2.adaptiveThreshold(display_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,30)
			##cv2.imshow('Adaptive 5',gaussian_adaptive5)
			##cv2.imshow('Adaptive 7',gaussian_adaptive7)
			##cv2.imshow('Adaptive 9',gaussian_adaptive9)
			#cv2.imshow('Adaptive 11',gaussian_adaptive11)
			kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
			gaussian_open = cv2.morphologyEx(gaussian_adaptive11, cv2.MORPH_OPEN, kernel)
			#cv2.imshow('opening',gaussian_open)
			#cv2.imshow('image',image)

			
			contours=cv2.findContours(gaussian_adaptive11,cv2.RETR_LIST ,cv2.CHAIN_APPROX_NONE)
			copy=np.full(image.shape,255,dtype=np.uint8)
			#print(contours[1])
			best_one=100
			best_two=100
			best_three=100
			best_one_contour=[]
			best_two_contour=[]
			best_three_contour=[]
			one_true=False
			two_true=False
			three_true=False
			if len(contours[1])>1:
				for contorno in contours[1]:
					save=False
					if save:
						copy=np.full(image.shape,255,dtype=np.uint8)
					epsilon = 0.1*cv2.arcLength(contorno,True)
					approx = cv2.approxPolyDP(contorno,epsilon,True)
					#print(len(approx))
					area=cv2.contourArea(contorno)
					#print('area:',area)
					value1=cv2.matchShapes(contorno, self.display1, 3, 0.0)
					value2=cv2.matchShapes(contorno, self.display2, 3, 0.0)
					value3=cv2.matchShapes(contorno, self.display3, 3, 0.0)
					
					
					if save and area>100:
						cv2.drawContours(copy, contorno, -1, (0,0,255), 1)
						#cv2.imshow('copy',copy)
						tecla=cv2.waitKey(0)
						if tecla==49:
							cv2.drawContours(copy, contorno, -1, (255,0,0), 1)
							print('Saved 1')
							np.save('display_one',contorno)
							#cv2.imshow('numero 1',copy)
						if tecla==50:
							cv2.drawContours(copy, contorno, -1, (255,0,0), 1)
							print('Saved 2')
							np.save('display_two',contorno)
							#cv2.imshow('numero 2', copy)
						if tecla==51:
							cv2.drawContours(copy, contorno, -1, (255,0,0), 1)
							print('Saved 3')
							np.save('display_three',contorno)
							#cv2.imshow('numero 3',copy)
					
					#For method 1, <0.2 is really good
					x,y,dx,dy=cv2.boundingRect(contorno)
					y_threshold=0
					y_threshold2=480 #p #pixels
					area_threshold=10
					#cv2.line(copy,(0,y_threshold),(640,y_threshold),(255,0,0),1,8)
					#cv2.line(copy,(0,y_threshold2),(640,y_threshold2),(255,0,0),1,8)

					if value1<0.2 and area>150 and area<1000000:
						print('one:',value1)
						cv2.drawContours(copy, contorno, -1, (255,0,0), 1)
						print('Area',area)
						if value1<best_one:
							best_one=value1
							best_one_contour=contorno
							one_true=True
					if value2<0.4 and area>150 and area<1000000:
						print('two:',value2)
						cv2.drawContours(copy, contorno, -1, (255,0,0), 1)
						print('Area',area)
						if value2<best_two:
							best_two=value2
							best_two_contour=contorno
							two_true=True

					if value3<0.4 and area>150 and area<1000000:
						print('three:',value3)
						cv2.drawContours(copy, contorno, -1, (255,0,0), 1)
						print('Area',area)
						if value3<best_three:
							best_three_contour=contorno
							best_three=value3
							three_true=True

			if (one_true):
				x,y,dx,dy=cv2.boundingRect(best_one_contour)
				cv2.rectangle(image,(x,y),(x+dx,y+dy),(0,0,255),1,8)
				print('Found 1:')
				return 1
				
			if (two_true):
				x,y,dx,dy=cv2.boundingRect(best_two_contour)
				cv2.rectangle(image,(x,y),(x+dx,y+dy),(0,0,255),1,8)
				print('Found 2:')
				return 2
			if (three_true):
				x,y,dx,dy=cv2.boundingRect(best_three_contour)
				cv2.rectangle(image,(x,y),(x+dx,y+dy),(0,0,255),1,8)
				print('Found 3:')
				return 3


			#cv2.imshow('copy',copy)
			print('Next image')
			#cv2.imshow('image',image)
