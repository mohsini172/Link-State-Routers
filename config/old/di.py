import threading
from threading import Thread,Lock
import time
import sys
import pickle
from socket import *
from collections import defaultdict
#from priodict import priorityDictionary

routdetail =[];		        # list containing everything from file
routnum=[];			#list with detail of one router as one value of list
routers=[];			# Router name only
costs=[];			# cost of router
ports=[];			# ports of router		
self = sys.argv[1]
neigh = {};
deadrouter={};

class Graph:
	def __init__(self):
		self.lock = Lock()
		self.nodes = set()
		self.edges = defaultdict(list)
		self.distances = {}
		self.time_holder = {}
		self.head = ""
    
	def add_node(self, value):
		self.lock.acquire()
		try:
			self.nodes.add(value)
			
		
		finally:
			self.lock.release()
			
	def update_time(self, value):
		self.time_holder[value] = time.time()
			
			
	def del_node(self, value):
		self.lock.acquire()
		try:
			self.nodes.discard(value)
			self.time_holder.pop(value)
		finally:
			self.lock.release()

	def add_edge(self, from_node, to_node, distance):
		self.lock.acquire()
		try:
			self.edges[from_node].append(to_node)
			self.edges[to_node].append(from_node)
			self.distances[(from_node, to_node)] = distance
			self.distances[(to_node, from_node)] = distance
		finally:
			self.lock.release()
	def setHead(self):
                self.head = sys.argv[1];
	def off(self):
		while True:
			try:
				print(self.time_holder)
				for fatiha in self.time_holder:
					print(fatiha)
					if(fatiha != self.head and time.time()- self.time_holder[fatiha] > 3):
						self.del_node(fatiha)
			except Exception as e:
				print(e)
			time.sleep(5)

	def th(self):
                t = Thread(target=self.off);
                t.start();

def dijkstra(graph, initial):
	seen = {initial: 0}
	path = {}
	nodes = set(graph.nodes)
	while nodes:
			min_node = None
			for router in nodes:
				if router in seen:
					if min_node is None:
						min_node = router
					elif seen[router] < seen[min_node]:
						min_node = router
			if min_node is None:
				break
			nodes.remove(min_node)
			current_weight = seen[min_node]
			for edge in graph.edges[min_node]:
				weight = current_weight + float(graph.distances[(min_node, edge)])
				if edge not in seen or weight < seen[edge]:
					seen[edge] = weight
					path[edge] = min_node
	return seen, path

def shortestPath(self,P,target):
  path = []
  while True:
    path.append(target)
    if target == self:
      break
    target = P[target]
  
  path.reverse()
  return path
	
	
def calldijkstra():
	i = 0;
	while i < 3:
		time.sleep(10)
		seen, path = dijkstra(graph, self)
		#print ("path: ", seen, path)
		for node in onRouters:
			string = ''
			route = shortestPath(self, path, node)
			for track in route:
				string = string+ track
			if string != node:
				print ("least-cost path to node %s: %s and the cost is %.1f" %(node,string,round(seen[node],1)))
		i+=1;
		
def configroute(route):
	print ("\nI am Router ", route, "\n");
	myfile = open('config'+route+'.txt', 'r')
	routnum = myfile.read().split('\n')
	myfile.close()
	for x in routnum:
		routdetail.append(x.split(' '));

	
def router():
	for x in routdetail[1:]:
		temp = "";
		for count,y in enumerate(x):
			if(count%3==0 and y != ""):
				routers.append(y);
				temp = y;
			if (count%3==1):
				costs.append(y);
				neigh[temp] = y
				#print ("router: ",temp, "cost: ", y)
			if (count%3==2):
				ports.append(y);
    
serverIP = "localhost"
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverPort = int(sys.argv[2])
#print ("serverPort: ", serverPort)
serverSocket.bind((serverIP, serverPort))
#print ("The server is ready to receive")
graph = Graph()
graph.add_node(self)
graph.setHead()
graph.th();

def sender():
	#print("Starting sender")
	temp = 1;
	i = 0;
	while i < 20:
		for count,y in enumerate(ports):
			clientSocket = socket(AF_INET, SOCK_DGRAM)
			msg = {'sentby':sys.argv[1],"start": sys.argv[1], "seq": str(temp), "neigh": neigh, 'on':onRouters}
			serverPort = int(y)
			time.sleep(1)
			packet = pickle.dumps(msg)
			clientSocket.sendto(packet,(serverIP, serverPort))
			i+=1;
		temp+=1;
    
def receiver():
	#print("Starting receiver")
	global onRouters
	onRouters = [];
	onRouters.append(sys.argv[1]);
	graph.add_node(sys.argv[1])
	i = 0;
	while i < 20:
		seen = [];
		
		try:
			message, clientAddress = serverSocket.recvfrom(2048)
			msg = pickle.loads(message)
			camefrom = msg['sentby']
			
			if (msg not in seen):
				seen.append(msg)
				keys = ['sentby', 'start']
				
				for key in keys:
					on = msg[key]
					#if (i%3 == 0):
					#	graph.nodes = set()
					#	graph.edges = defaultdict(list)
					#	onRouters = [];	
					if on not in onRouters:
						onRouters.append(on);
				
				for x in msg['on']:
					if x not in onRouters:
						onRouters.append(x);
                                                        
				
				for count, ro in enumerate(routers):
					if ro in onRouters:
						graph.add_node(msg['sentby'])
						graph.add_edge(sys.argv[1],ro,costs[count])
						#print("costs: ", costs[count],"coming from: ", sys.argv[1], "->", ro)
				for key, value in msg['neigh'].items():
					if (msg['start'] != key and key in onRouters):
						graph.add_node(msg['start'])
						graph.update_time(msg['sentby'])
						graph.add_edge(msg['start'],key,value)
						#print("costs: ", value,"coming from: ", msg['start'], "->", key)
						
				for count,y in enumerate(ports):
					if (routers[count] != camefrom and routers[count] != msg['start']):
						serverPort = int(y)
						try:
							msg['sentby'] = sys.argv[1]
							packet = pickle.dumps(msg)
							serverSocket.sendto(packet,(serverIP, serverPort))
							time.sleep(0.2)
						except:
							#print ("Not Sent")
                                                        pass
						i+=1;
				#print("onRouters: ",onRouters)
		except:
			pass

configroute(sys.argv[1])
router();
#threading
senderthread = threading.Thread(target=sender)
receiverthread = threading.Thread(target=receiver)
routingthread= threading.Thread(target=calldijkstra)
receiverthread.start()
senderthread.start()
routingthread.start()


		
