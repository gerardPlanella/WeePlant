import robot_vision as rvis
import com_URScript as script
import cv2
import socket
import time
import math as m

ROBOT_STATUS_BITS = "robot_status_bits"
ROBOT_JOINT_POSITIONS = "get_all_joint_positions"

UNKNOWN_HUMAN = "Unknown"

class UR():

	__slots__ = ('address', 'port_Data', 'port_Move', 'positions')

	def __init__ (self, address):
		self.address = address
		self.port_Data = 30100
		self.port_Move = 30002
		self.positions = {
			"Starting position": [-268.95, -90, 0, 0, 90, 90],
			"Salute 1": [-188.6, -9.81, -77, 11.54, 149.42, 0],
			"Salute 2": [-188.6, -9.81, -77, 11.54, 33.3, 0],
			"swipe acquisition 1": [-110.23,-122.89,119.76,-73.48,10.25,219.37],
			"swipe acquisition 2": [-173.3,-57.6,82,-111,-12,204],#-167.96,-94.8,118.5,-104.96,-12.54,204],#-158.22,-62.42,105.28,-111.47,-7,211.48],
			"before any acquisition": [-109.15,-109.24,110,-1,79,185], #pinca oberta
			"before acquisition bottle 1": [-85.97,-78.43,146.7,-68.91,96.2,179.95], #pinca oberta
			"before acquisition bottle 2": [-127.43,-74.4,140,-66.3,54.75,180.6],
			"before acquisition bottle 3": [-153.76,-71,134.11,-64.55,28.43,181.63],
			"acquisition bottle 1":[-87.37,-61.53,116.01,-55.12,94.81,180], #tancar pincaS
			"acquisition bottle 2":[-112.53,-55.35,103.9,-49.24,69.67,180.36],
			"acquisition bottle 3":[-130.66,-52.55,98.48,-46.9,51.55,180.77],
			"before delivery" : [-145.56, -40.21, 75.39, -35.91, 127.19, 179.55], #pinca tancada
			"after delivery" :[-152.17, -23.64, 40.91, -17.92, 120.61, 179.70] #obrim pinca
			}


	def FreeMode(self):
		script.freedrive_mode(self.address)

	def anyoneInCamera(self):
		return rvis.anyoneInCamera();


	def NotFreeMode(self):
		script.end_freedrive_mode(self.address)

	def getAddress(self):
		return self.address

	def get_actual_joint_positions(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.address, self.port_Data))
		sock.send(ROBOT_JOINT_POSITIONS.encode())
		msg = sock.recv(4096).decode()

		print(msg + "\n")
		sock.close()

	def moveJoints(self, position_name, a, v):
		joint_angles = self.positions[position_name]
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.address, self.port_Data))
		script.movej(self.address, m.radians(joint_angles[0]), m.radians(joint_angles[1]), m.radians(joint_angles[2]),
		m.radians(joint_angles[3]), m.radians(joint_angles[4]), m.radians(joint_angles[5]), a, v, 0, 0)
		time.sleep(0.5)
		cnt = 0
		headerDone = 0
		while True:
			sock.send(ROBOT_STATUS_BITS.encode())
			msg = sock.recv(4096).decode()
			cnt = cnt + 1
			print(msg + "\n")
			if int(msg) == 1:
				if headerDone == 1 and cnt >=5 :
					break
				headerDone = 1
			time.sleep(0.1)
		sock.close()


	def moveLJoints(self, position_name, a, v):
		joint_angles = self.positions[position_name]
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.address, self.port_Data))
		script.movel(self.address, m.radians(joint_angles[0]), m.radians(joint_angles[1]), m.radians(joint_angles[2]),
		m.radians(joint_angles[3]), m.radians(joint_angles[4]), m.radians(joint_angles[5]), a, v, 0, 0)
		time.sleep(0.5)
		cnt = 0
		headerDone = 0
		while True:
			sock.send(ROBOT_STATUS_BITS.encode())
			msg = sock.recv(4096).decode()
			cnt = cnt + 1
			print(msg + "\n")
			if int(msg) == 1:
				if headerDone == 1 and cnt >=5 :
					break
				headerDone = 1
			time.sleep(0.1)
		sock.close()

	def operateGripper(self, open = True):
		GRIPPER_PIN = 1
		if open is True:
			script.open_gripper(self.address, GRIPPER_PIN)
		else:
			script.close_gripper(self.address, GRIPPER_PIN)



	def face_detect(self, threshold):
		"""
		Function that waits to detect a face

		Args:
			threshold(int) number that dictates how many frames a face should be detected before the function ends
		Returns:
			recon_result(name str, face image)

		"""
		recon_result =  rvis.recognize_face(threshold)
		if recon_result[0] == UNKNOWN_HUMAN:
			cv2.imwrite("faces/tmp.jpg", recon_result[1])
		else:
			cv2.imwrite("faces/" + recon_result[0] + ".jpg", recon_result[1])


		return recon_result[0]

	def emotional_wait(self, emotion, threshold):
		if rvis.waitForEmotion(emotion, threshold) < 0:
			print("Error emotion param")
		else:
			print(emotion + " state achieved")

	def gesture_detect(self, gesture_type, threshold):
		rvis.recognize_gesture(gesture_type, threshold)
		print("Gesture with " + str(gesture_type) + "fingers recognized")
"""
if __name__ == "__main__":
	robot = UR("192.168.1.104")
	robot.NotFreeMode()
	#robot.FreeMode()

	robot.moveJoints("Salute 2", 0.5, 0.5)
	a = 0
	while a < 2:
		a = a + 1
		robot.moveJoints("swipe acquisition 1", 0.5, 0.5)
		robot.moveJoints("swipe acquisition 2", 0.5, 0.5)
	#robot.moveJoints("before acquisition bottle 1", 0.5, 0.5)


	robot.moveJoints("before delivery", 0.5, 0.5)
	robot.moveLJoints("delivery point", 0.5, 0.5)
	robot.moveJoints("after delivery", 0.5, 0.5)

	robot.moveJoints("swipe acquisition 2", 0.5, 0.5)
	robot.moveJoints("before any acquisition", 0.5, 0.5)
	robot.moveJoints("before acquisition bottle 3", 0.5, 0.5)
	robot.moveLJoints("acquisition bottle 3", 0.5, 0.5)
"""
