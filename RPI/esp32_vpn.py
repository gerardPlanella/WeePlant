import socket
import threading

ADDR = '192.168.1.36' 
PORT = 8021

DEST_ADDR = '25.120.131.106'
DEST_PORT = 8017

runThread = True

def connect_serv(addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    # Create socket on port
    try:
        sock.bind((addr, port))
    except socket.error as msg:
        print('# Bind failed. ')
        return False
    
    # Start listening on socket
    sock.listen(10)
    print('# Socket now listening')
    

    # Wait for ESP32 client
    conn, addr = sock.accept()
    print('# Connected to ' + addr[0] + ':' + str(addr[1]) + " Client Successfully!")

    return conn


def connect_cli(addr, port):
    sock = socket.socket()

    sock.connect((addr, port))

    print("# Connected to " + str(addr) + ':' + str(port) + " Server Successfully!")

    return sock

def pingpong(conn1, conn2):
    global runThread

    while runThread:
        rx = conn1.recv(1024)
        conn2.sendall(rx)


def main():
    global runThread
    
    conn1 = connect_serv(ADDR, PORT)
    if not conn1:
        print("Connection Failed")
        return False

    conn2 = connect_cli(DEST_ADDR, DEST_PORT)

    thread_cli = threading.Thread(target = pingpong, args = (conn1, conn2, ))
    thread_cli.start()

    try:
        pingpong(conn2, conn1)
    except KeyboardInterrupt:
        runThread = False
        thread_cli.join()
        print("Execution terminated successfully")
        
if __name__ == "__main__":
    main()