import os
import socket
import json
import sys

def disp_output(num,nei_len,pat_len):
	print num
	for i in range(num):
		output=''
		count=0
		for j in range(num):
			if pat_len[i+1][j+1]>0:
				output=output+str(j+1)+' '+str(pat_len[i+1][j+1])+' '
				count=count+1
		output=str(count)+' '+output
		print output
	return 1

def func_message(source_no,dest_no,num,nei_len,pat_len,pat_des):
	host=""
	base_port=7999
	soc=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	soc.bind((host,base_port))
	pid=os.fork()
	if pid==0:
		msg,cl_addr=soc.recvfrom(1024)
		pat_arr=[ [pat_len[dest_no][i],pat_des[dest_no][i]] for i in range(num+1) ]
		send_data=json.dumps(pat_arr)
		soc.sendto(send_data,cl_addr)
		soc.close()
		os._exit(0)
	else:
		rec=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		rec.sendto("handshake",(host,base_port))
		rec_data,ser_addr=rec.recvfrom(1024)
		rec_data=json.loads(rec_data)
		rec.close()
	for i in range(num):
		if i+1==source_no:
			continue
		if rec_data[i+1][0]>0:
			if pat_len[source_no][i+1]<0 or pat_len[source_no][i+1]>rec_data[i+1][0]+nei_len[dest_no][source_no]:
				pat_len[source_no][i+1]=rec_data[i+1][0]+nei_len[dest_no][source_no]
				pat_des[source_no][i+1]=dest_no
	ret_set=(num,nei_len,pat_len,pat_des)
	return ret_set


def bellman_ford_algo(num,nei_len,pat_len,pat_des):
	for i in range(num):
		for j in range(num):
			if nei_len[i+1][j+1]>0:
				op=func_message(i+1,j+1,num,nei_len,pat_len,pat_des)
				num=op[0]
				nei_len=op[1]
				pat_len=op[2]
				pat_des=op[3]
	ret_set=(num,nei_len,pat_len,pat_des)
	return ret_set

def func_input_file(filename):
	with open(filename) as fp:
		num=0
		num=int(fp.readline())
		nei_len=[[ -1 for i in range(num+1) ] for j in range(num+1)]
		pat_len=[[ -1 for i in range(num+1) ] for j in range(num+1)]
		pat_des=[[ i for i in range(num+1) ] for j in range(num+1)]
		node_no=1
		for line in fp:
			val=line.split()
			nei_no=int(val[0])
			while nei_no>0:
				it_no=(int(val[0])-nei_no)*2+1
				nei_node=int(val[it_no])
				cost=int(val[it_no+1])
				nei_len[node_no][nei_node]=nei_len[nei_node][node_no]=cost
				pat_len[node_no][nei_node]=cost
				pat_des[node_no][nei_node]=nei_node
				nei_no=nei_no-1
			node_no=node_no+1
	ret_set=(num,nei_len,pat_len,pat_des)
	return ret_set

def main(inp):
	ini_data=func_input_file(inp)
	fin_data=bellman_ford_algo(ini_data[0],ini_data[1],ini_data[2],ini_data[3])
	disp_output(fin_data[0],fin_data[1],fin_data[2])

main(sys.argv[1])