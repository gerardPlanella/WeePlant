import data as dat
import comunicaction as com
import signal
import sys
import os
import argparse
import logging
from time import sleep

server = None
parser = argparse.ArgumentParser()
parser.add_argument('--host', default='localhost', help='name of host to connect to (localhost)')
parser.add_argument('--robot_port', type=int, default=30004, help='port number (30004)')
parser.add_argument('--working_path', default='./', help='data configuration file to use (record_configuration.xml)')
parser.add_argument("--clients_port", default=30100, help='client port')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)

def main():
    global server

    os.chdir(args.working_path)
    HOST = args.host
    ROBOT_PORT = args.robot_port
    CLIENTS_PORT = args.clients_port

    data = dat.Data()
    robot_c = com.RobotComunication(data)
    server = com.Server(robot_c, data, CLIENTS_PORT)
    signal.signal(signal.SIGTERM, goodbye)
    signal.signal(signal.SIGINT, goodbye)
    server.daemon = True
    server.start()
    
    while (True):
        robot_c.init_robot_com(HOST, ROBOT_PORT)
        
        if robot_c.robot_connected:
            logging.info("Robot connected, starting server")
            robot_c.update_robot_data()
            
        logging.info("Restarting service...")
        sleep(0.1)
    
def goodbye(SIGNUM, frame):
    global server
    print("See you soon!")
    server.close()
    sys.exit(0)


if __name__ == '__main__':
    main()
