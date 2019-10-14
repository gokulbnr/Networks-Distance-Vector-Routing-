import socket
import os
import json

host = ""
UDP_port = 7999

def relax(sourc,dest):
    UDP_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDP_s.bind((host, UDP_port))
    pid = os.fork()
    if pid == 0:
        message, clientAddress = UDP_s.recvfrom(1024)
	print paths[dest]
        data = json.dumps(paths[dest])
        UDP_s.sendto(data, clientAddress)
        UDP_s.close()
        os._exit(0)
    else:
        receive_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receive_s.sendto("handshake",(host, UDP_port))
        data, serverAddress = receive_s.recvfrom(1024)
        datalist = json.loads(data)
        receive_s.close()

    for i in range(node_no):
        if i == sourc:
            continue
        if datalist[i][0] > 0:
            if paths[sourc][i][0] < 0 or paths[sourc][i][0] > datalist[i][0] + lengths[dest][sourc]:
                paths[sourc][i][0] = datalist[i][0] + lengths[dest][sourc]
                paths[sourc][i][1] = dest

def Bellman_Ford():
    for i in range(node_no):
	#print i
	for j in range(node_no):
            if lengths[i][j] > 0:
                relax(i,j)

def show_paths():
    print node_no
    for i in range(node_no):
        neighbours = ''
        no = 0
        for j in range(node_no):
            if paths[i][j][0]>0:
                neighbours += str(j+1) + ' '
                neighbours += str(paths[i][j][0]) + ' '
                no += 1
        neighbours = str(no) + ' ' + neighbours
        print neighbours

def input_data():
    global node_no,lengths,paths
    node_no = input()
    lengths = [[ -1 for i in range(node_no) ] for j in range(node_no)]
    paths = [[ [-1,i] for i in range(node_no) ] for j in range(node_no)]
    for i in range(node_no):
        in_string = raw_input()
        neighbours = in_string.split()
        neighbours.pop(0)
        while len(neighbours)>0:
            a = int(neighbours.pop(0))-1
            if a >= node_no:
                print "node number exceeded\n"
                return -1
            b = int(neighbours.pop(0))
            lengths[i][a] = b
            lengths[a][i] = b
            paths[i][a][0] = b
            paths[i][a][1] = a
    return 1

node_no = 0
lengths = []
paths = []

x = input_data()
while x < 0:
    x = input_data()
Bellman_Ford()
show_paths()
