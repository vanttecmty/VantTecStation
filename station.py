import sys
import os
import xbee
import time
#import cv2
#import challenges as chall
import auvsiServerCommunication as auvsi
#import bluetoothServer as bt

x = xbee.xbee("/dev/ttyUSB0")
status = "waiting%"
#Timestamp		Latitude	Longitude	Challenge	Takeoff 	Flying Landing
#20170622012420, HDDD.DDDDDD, HDDD.DDDDDD, N, 0, 0 , 0%
challenges = ['Autonomous','speed', 'follow', 'path', 'docking', 'return']
courses = ['courseA', 'courseB', 'courseC']
'''
		Enable transmission 	0 = Waiting for Transmission 1 = Transmitting 
		R_KillSwitch = 0 , 1
		Status = 0, 1, 2		0 = OK , 1 = END , 3 = Manual
		Course = 0,1,2			0 = courseA , 1 = courseB , 2 = courseC
		Challenge = 0,1,2,3,4;  0 = Autonomous, 1 = SpeedChallenge, 2 = Follow, 3 = Path , 4 = Docking, 5 = Return
		Dock 					0 = notDefined yet 1 , 2 , 3
		'''
enable = 0;
R_KillSwitch = 0;
Status = 0;
course = 0;
challenge = 0;
dock = 0;
info2Boat = [enable,R_KillSwitch,Status,course,challenge,dock];
currCourse = '';
currChallenge = '';
challPos = 3;
timestamp = 0;
timePos = 0
latPos = 1
longPos = 2
cPos = 3
takePos = 4
flyingPos = 5
landPos = 6

data = ['','','','','','','','']

def send_course():
	for i in range(1,5):
		enable = 1;
		dock = 2;
		#Send the info to the boat
		info2Boat = [enable,R_KillSwitch,Status,course,challenge,dock];
		x.send2boat(info2Boat);
		time.sleep(1.05 )
		#Send the last heart_beat sended with the last info of docking
		auvsi.send_http_heartbeat(currCourse,t,currChallenge,la,lo);

def send_dock():
	#Send the information of the dock to the boat
	#Send several messages to be sure that message arrived.
	global data
	global currChallenge
	print(data)
	for i in range(1,6):
		enable = 1;
		dock = 2;

		#Send the info to the boat
		info2Boat = [enable,R_KillSwitch,Status,course,challenge,dock];
		x.send2boat(info2Boat);
		x.clean_buffer()
		time.sleep(1.05 )
		#Cast the values of the # values
		t  = int(data[timePos])
		la = float(data[latPos])
		lo = float(data[longPos])
		#Send the last heart_beat sended with the last info of docking()
		auvsi.send_http_heartbeat(currCourse,t,currChallenge,la,lo);
	
	x.clean_buffer()
	


def select_course():
	course = 0;
	#Get the actual course in which we are going to go in
	global currCourse;
	while course != 1:
		course = int(input("Select the Course \n1) courseA \n2) courseB \n3) courseC\n"))
		if(course == 1 or course == 2 or course == 3 ):
			currCourse = courses[course-1];
			course = 1
	print("Current Course = ",currCourse);

def wait_for_docking():
	global data
	global currCourse
	global currChallenge

	#Wait for boat to arrive to the docking challenge
	while data[challPos] != 'd':
		#Wait for the incomming data
		try:
			s = x.receive_from_boat();

			data = s.split(',');
			if(data[0].find('2') > 0):
				data[0] = data[0][data[0].find('2') : ]

			print(data)
			#Ask for the current challenge to submit to the server
			set_challenge(data)
			#Cast the values of the # values
			print(currChallenge)
			#Hearbeat speed, docking, path, follow, return
			if( currChallenge == 'speed' or currChallenge == 'return' or currChallenge == 'follow' or currChallenge == 'path'):
				t  = int(data[timePos])
				la = float(data[latPos])
				lo = float(data[longPos])
				#Send the heart_beat with the current information
				auvsi.send_http_heartbeat(currCourse,t,currChallenge,la,lo);
			elif(currChallenge == 'start'):
				auvsi.send_http_start(currCourse)
				t  = int(data[timePos])
				la = float(data[latPos])
				lo = float(data[longPos])
				#Send the heart_beat with the current information
				auvsi.send_http_heartbeat(currCourse,t,currChallenge,la,lo);
			elif(currChallenge == 'end'):
				auvsi.send_http_end(currCourse)
				t  = int(data[timePos])
				la = float(data[latPos])
				lo = float(data[longPos])
				#Send the heart_beat with the current information
				auvsi.send_http_heartbeat(currCourse,t,currChallenge,la,lo);
			elif(currChallenge == 'docking'):
				t  = int(data[timePos])
				la = float(data[latPos])
				lo = float(data[longPos])
				#Send the heart_beat with the current information
				auvsi.send_http_heartbeat(currCourse,t,currChallenge,la,lo);
				auvsi.send_http_docking(currCourse, "DronePhoto1.jpg");

		except ValueError:
			print("Error en la rececpción XBee")
		
def wait_for_end():
	global data
	global currCourse
	global currChallenge
	while data[challPos] != 'e':
		s = x.receive_from_boat();
		time.sleep(.1)
		x.clean_buffer()
		data = s.split(',');

		if(data[0].find('2') > 0):
				data[0] = data[0][data[0].find('2') : ]

		print(data)

		set_challenge(data)
		#Cast the values of the # values
		t  = int(data[timePos])
		la = float(data[latPos])
		lo = float(data[longPos])
		#Send the heart_beat with the current information
		auvsi.send_http_heartbeat(currCourse,t,currChallenge,la,lo);	

def start_autnonmous():
	s = '123412341234123412341234123412341234123412341234123412'
	global dock
	global info2Boat
	global currCourse
	global data
	global currChallenge
	###Read HeartBeat Untill End 
	select_course()

	#Init the process to wait for the autodocking position
	wait_for_docking();
	print("Wait For Docking")
	x.clean_buffer()
	#Ask for the current challenge to submit to the server
	set_challenge(data)
	#Send the heart_beat with the current information
	auvsi.send_http_heartbeat(currCourse,int(data[timePos]),currChallenge,float(data[latPos]),float(data[longPos]));


	#Ask the dock from drone by BT
	d = read_dock_from_drone()
	print("read_dock_from_drone")
	dock = d
	
	send_dock();
	print("send_dock")

	x.clean_buffer()
	#Wait for the end of the run
	wait_for_end();
	#bt.disconnect();

def read_dock_from_drone():
	#bt.beginMission()
	# To Do: Image process Image
	#img = cv2.imread("DronePhoto1.jpg");
	#cv2.imshow(img)
	#dock_object=chall.Automated_Docking(img)
	#dock_object.search_number()
	return 2

#Get the challenge from the Heart_beat
def set_challenge(s):
	#challPos = 3
	global currChallenge ;
	global challPos

	#print("Set_Challenge: ", s , s[challPos]);
	if s[challPos] == 's' or  s[challPos] == 'S':
		currChallenge = 'start'	
	elif s[challPos] == 'd' or  s[challPos] == 'D':
		currChallenge = 'docking';
		#print("Docking");
		if data[takePos] == '1':
			print("Drone Taking Off");
		if data[flyingPos] == '1':
			print("Drone Flying");
		if data[landPos] == '1':
			print("Drone landing");
	elif s[challPos] == 'f' or  s[challPos] == 'F':
		currChallenge = 'follow';
		#print("Follow the leader");
	elif s[challPos] == 'r' or  s[challPos] == 'R':
		currChallenge = 'return';
		#print("Returning");
	elif s[challPos] == 'v' or  s[challPos] == 'V':
		currChallenge = 'speed';
		#print("Speed Challenge");
	elif s[challPos] == 'a' or  s[challPos] == 'A':
		currChallenge = 'speed';
		#print("Autonomous");
	elif s[challPos] == 'p' or  s[challPos] == 'P':
		currChallenge = 'path';
		#print("Path Planning");
	elif s[challPos] == 'n' or  s[challPos] == 'N':
		currChallenge = 'speed';
		#print("Between challenges");
	elif s[challPos] == 'e' or  s[challPos] == 'E':
		currChallenge = 'end';
		#print("END of communication");




def read_heart_beat():
	s = '123412341234123412341234123412341234123412341234123412'
	###Read HeartBeat Untill End 
	select_course()
	global currChallenge

	while s[challPos] != 'e':
		s = x.receive_from_boat();
		data = s.split(',');
		if s[challPos] == 's' or  s[challPos] == 'S':
			print("Starting");
			print(data)
			#Send first target point to the boat
			#Report to http sever
		elif s[challPos] == 'd' or  s[challPos] == 'D':
			currChallenge = 'dock';
			print("Docking");
			if data[takePos] == '1':
				print("Drone Taking Off");
			if data[flyingPos] == '1':
				print("Drone Flying");
			if data[landPos] == '1':
				print("Drone landing");
		elif s[challPos] == 'f' or  s[challPos] == 'F':
			currChallenge = 'follow';
			print("Follow the leader");
		elif s[challPos] == 'r' or  s[challPos] == 'R':
			currChallenge = 'return';
			print("Returning");
		elif s[challPos] == 'v' or  s[challPos] == 'V':
			currChallenge = 'speed';
			print("Speed Challenge");
		elif s[challPos] == 'r' or  s[challPos] == 'R':
			currChallenge = 'return';
			print("Returning home");
		elif s[challPos] == 'p' or  s[challPos] == 'P':
			currChallenge = 'path';
			print("Path Planning");
		elif s[challPos] == 'n' or  s[challPos] == 'N':
			currChallenge = 'speed';
			print("Transition");


	print("Boat ended")

def testing3():
	send_dock();

def send_return_data():
	global status
	while True:
		x.send2boat(info2Boat);
		time.sleep(1.05)

if __name__ == '__main__':
	start_autnonmous()
	#testing3()
