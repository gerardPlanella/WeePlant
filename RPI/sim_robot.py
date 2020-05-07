import com_URScript as script
import socket
import time
import math as m


#Trama: speed.interpolation_steps.angle_base.angle_hombro.angle_colze.angle_endeffector\n

#PORT = 25852

class UR_SIM():

    __slots__ = ('address','port','s','positions')

    def __init__ (self, address,port):
        self.address = address 
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        err = self.s.connect((self.address, self.port))
        
        if err == 0:
            print("Error connectant amb la simulacio")

        self.positions = {
            "starting position": [90,90,90,90],
            "second position" : [0,90,0,90]
        }

    def getAddress(self):
        return self.address

    def move(self,position_name,speed,interpolationSteps):
        trama = str(speed) + "." + str(interpolationSteps) + "."

        for e in self.positions[position_name]:
            trama += str(e) + "."
        #Ara una mica de Magia negra...
        trama = "\n".join(trama.rsplit(".", 1))
        
        self.s.sendall(trama.encode('ascii'))

        #Response ignored. Its used to block the program untill the simulation reaches its goal
        self.s.recv(1024).decode('ascii')

if __name__ == "__main__":
    sim = UR_SIM("localhost", 25852)
    sim.move("starting position",20,50)
    sim.move("second position",20,50)