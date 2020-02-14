import com_URScript as script
import socket
import time
import math as m

DEBUG = False

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
			"before acquisition bottle 1": [-85.99,-91.15,142.61,-52.1,96.2,179.95], #pinca oberta
			"before acquisition bottle 2": [-127.45,-87.98,135.05,-47.75,54.75,180.6],
			"before acquisition bottle 3": [-153.77,-81.65,130,-50,28.43,181.63],
			"acquisition bottle 1":[-87.35,-51.99,117,-65.68,94.8,180], #pinca oberta
			"acquisition bottle 2":[-112.5,-47.35,104.85,-58.2,69.7,180],
			"acquisition bottle 3": [-129,-46,100.8,-56,53.25,180],
			"before delivery" : [-145.56, -40.21, 75.39, -35.91, 127.19, 179.55], #pinca tancada
			"after delivery" :[-152.17, -19.57, 41.93, -23.01, 120.6, 179.7], #obrim pinca
			"removal point" : [-152.17,-16.72,41.61,-25.55,120.6,180]
			}

	def FreeMode(self):
		global DEBUG
		if DEBUG: return
		script.freedrive_mode(self.address)

	def NotFreeMode(self):
		global DEBUG
		if DEBUG: return
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
		global DEBUG
		if DEBUG: return
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
		global DEBUG
		if DEBUG: return
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
		global DEBUG
		if DEBUG: return
		GRIPPER_PIN = 1
		if open is True:
			script.open_gripper(self.address, GRIPPER_PIN)
		else:
			script.close_gripper(self.address, GRIPPER_PIN)
		time.sleep(1)