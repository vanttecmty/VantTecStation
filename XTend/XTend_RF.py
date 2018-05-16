import json
import time
from digi.xbee.devices import XBeeDevice

###Class#
class XTend():
	###Main communication Function####
	port = "COM7"
	baudrate = 9600
	device = XBeeDevice(port, baudrate)
	station_json = ""
	json_messsage = ""
	text_message = ""
	#Could be VanTTec Boat or VanTTec Station
	#If cant stablish communication -> check on XCTU the NodeID of the XTend RFs
	REMOTE_NODE_ID = ""

	def __init__(self,PORT,BAUDRATE,remote_node_id = "VanTTec Boat"):
		self.port = PORT
		self.baudrate = BAUDRATE
		self.REMOTE_NODE_ID = remote_node_id

	def data_receive_callback(self,dev, xbee_message):
		self.text_message = xbee_message.data.decode()
		self.json_message = json.loads(xbee_message.data.decode())	
		print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(), xbee_message.data.decode()))
		#return json_message
		# Procesa los datos aquí.
	 

	def start_station():
		#Open Communication
		device.open()

		start = time.time()
		end = time.time()

		while(True):
			###Main communication Function####
			self.device.add_data_received_callback(data_receive_callback)	

			if(self.json_message["Challenge"] != "NAVIGATING"):
				send_auvsi_server_challenge(self.json_message)

			## Do stuff with Json Message
			if(curr_time >= transmission_timeout):
				start = time.time()
				end = time.time()

				send_heart_beat_auvsi()

			else:
				end = time.time()


	def start_boat(self,transmission_timeout):
		self.device.open()

		start = time.time()
		end = time.time()

		while(True):
			###Main communication Function####
			self.device.add_data_received_callback(data_receive_callback)	

			#Get curr info
			heartbeat_info = get_hearbeat_info()
			
			curr_time = end-start
			if(curr_time >= transmission_timeout):
				start = time.time()
				end = time.time()

				send_hearbeat(heartbeat_info)
			else:
				end = time.time()


	def send_hearbeat(self,heartbeat_info):
		js_to_send = generate_json(heartbeat_info)
		XTend_send_data(js_to_send)


	def XTend_send_data(self,json_message):
		# Obtain the remote XBee device from the XBee network.
		xbee_network = self.device.get_network()
		remote_device = xbee_network.discover_device(self.REMOTE_NODE_ID)
		if remote_device is None:
			print("Could not find the remote device")
			exit(1)

		print("Sending data asynchronously to %s >> %s..." % (remote_device.get_64bit_addr(), message))

		self.device.send_data_async(remote_device, message)

	def send_auvsi_server_start_challenge(self,json_message):
		print("Send to auvsi")

	def set_port(self,port):
		self.port = port

	def get_port(self):
		return self.port

	def set_baudrate(self,baudrate):
		self.baudrate = baudrate

	def get_baudrate(self):
		return self.baudrate

	def set_nodeid(self,nodeid):
		self.REMOTE_NODE_ID = nodeid

	def get_nodeid(self):
		return self.REMOTE_NODE_ID