import sys
from socket import * 
from threading import Thread
import time
import random
import json
f_dict = {}
packet = {}
command_list = []
port_num = []
cost_list = []
neighbour_list = []
active_neighbour_list =[]
init = sys.argv[1]


for x in range (0,4):
 command_list =command_list + (sys.argv[x].split()) 

with open(command_list[3],'r') as file:
  next(file)
  for line in file:
    spl = line.split()
    key, values = (spl[0]), spl[1:]
    f_dict.setdefault(key,[]).extend(values)
    port_num= port_num + [values[1]]
    cost_list= cost_list + [values[0]]
    neighbour_list= f_dict.keys()

serverIP = '127.0.0.1'
serverPort= command_list[2]
clientSocket=socket(AF_INET,SOCK_DGRAM)
clientSocket.bind(("",int(serverPort))) 

count=0

def c_socket():
 while True:
  try:
   for x in port_num:
    packet = {'sender': init , 'receiver': command_list[1], 'neighbour':neighbour_list,'seq_num':seq}
    message=json.dumps(packet)
    message = message.encode(packet)

    clientSocket.sendto(message,(serverIP,int(x)))
   time.sleep(1.5)
  except:
   pass

 clientSocket.close()
   

def s_socket():
 print (" The server is ready to receive ")
 while 1:
  try:
    message, clientAddress = clientSocket.recvfrom(2048)
    modifiedMessage = message.decode('utf-8')
    modifiedMessage=json.load(message)
    print(modifiedMessage)
    
    message = json.dumps(packet)
    clientSocket.sendto(message.encode('utf-8'),clientAddress)
    time.sleep(1.5)
  except:
   pass

def main():
  t1= Thread (target = s_socket)
  t1.start()
  t= Thread (target = c_socket)
  t.start()
  #t2 = Thread( target = lsp )
  #t2.start()
  
main()
  