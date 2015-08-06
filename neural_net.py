# A class to represent a neural net for the NEAT algorithm

import random, copy


def NEAT_merge_nets(net1, net2):
	new_net = copy.deepcopy(net1)

	genetic_marker_merge(new_net.connections, net2.connections)
	genetic_marker_merge(new_net.hiddenNodes, net2.hiddenNodes)
	genetic_marker_merge(new_net.sensorNodes, net2.sensorNodes)
	genetic_marker_merge(new_net.outputNodes, net2.outputNodes)

	return new_net



def genetic_marker_merge(new_net_list, list2):
	found = {}
	for el in list2:
		found[el.genetic_marker] = el
	for con in new_net_list:
		try:
			new_con = random.choice([con, found[con.genetic_marker]])
			con.setWeight(new_con.getWeight())
		except KeyError:
			found[con.genetic_marker] = con	




class NeuralNet:

	def __init__(self):
		self.hiddenNodes = []
		self.sensorNodes = []
		self.outputNodes = []
		self.connections = []
		self.node_num = 0

	def __str__(self):
		str_out = "sensorNodes: \n" 
		for node in self.sensorNodes:
			str_out += str(node)
		str_out += "hiddenNodes: \n" 
		for node in self.hiddenNodes:
			str_out += str(node) 
		str_out += "outputNodes: \n" 
		for node in self.outputNodes:
			str_out += str(node)   
		str_out += "connections: \n" 
		for con in self.connections:
			str_out += str(con)

		return str_out


	def createHiddenNode(self, threshold):
		newNode = Node(threshold, self.node_num)
		self.hiddenNodes.append(newNode)
		self.node_num += 1
		return newNode

	def createOutputNode(self, threshold):
		self.outputNodes.append(outputNode(threshold, self.node_num))
		self.node_num += 1

	def createSensorNode(self, threshold):
		self.sensorNodes.append(Node(threshold, self.node_num))
		self.node_num += 1

	def createConnection(self, weight, start, end, enabled):
		self.connections.append(Connection(weight, start, end, enabled))

	def process(self, sensor_readings):
		for i in range(0,len(self.sensorNodes)):
			self.sensorNodes[i].send(sensor_readings[i])
		return [node.out for node in self.outputNodes]

	def mutate_connection(self, a, b):
		choices = self.hiddenNodes+self.outputNodes+self.sensorNodes
		start = random.choice(choices)
		choices.remove(start)
		end = random.choice(choices)
		self.connections.append(Connection(random.uniform(a, b), start, end, True))


	def mutate_node(self, a, b):
		replaced = random.choice(self.connections)
		insertion = self.createHiddenNode(random.uniform(a,b))
		self.createConnection(1, insertion, replaced.end, True)
		replaced.end = insertion

	def mutate_weight(self, a, b):
		random.choice(self.hiddenNodes + self.sensorNodes + self.outputNodes + self.connections).setWeight(random.uniform(a,b))





class NEATComponent:
	genetic_marker_control = 0


class Node(NEATComponent):
	def __init__(self, threshold, node_num):
		self.threshold = threshold
		self.genetic_marker = self.genetic_marker_control
		NEATComponent.genetic_marker_control += 1
		self.input = []
		self.output = []

		self.mailbox = []

		self.ready = False

		self.node_num = node_num

	def __str__(self):
		return 'id: ' + str(self.node_num) + ' thresh:' + str(self.threshold) + ' genetic_marker:' + str(self.genetic_marker) + "\n"

	def __deepcopy__(self, memo):
		return copy.copy(self)


	def setWeight(self, threshold):
		self.threshold = threshold

	def getWeight(self):
		return self.threshold

	def addInput(self, x):
		self.input.append(x)

	def addOutput(self, x):
		self.output.append(x)

	def send(self, package):
		for connection in self.output:
			connection.send(package)

	def receive(self, package):
		self.mailbox.append(package)
		if len(self.mailbox) == len(self.input):
			tot = 0
			for mail in self.mailbox:
				tot += mail
			self.mailbox = []
			if tot >= self.getWeight():
				self.send(1)
			else:
				self.send(0)




class hiddenNode(Node):
	def send(self, package):
		for connection in self.output:
			connection.send(package)

class outputNode(Node):
	def __init__(self, threshold, node_num):
		Node.__init__(self, threshold, node_num)
		self.ready = False
		self.out = None

	def send(self, package):
		self.ready = True
		self.out = package






class Connection(NEATComponent):
	def  __init__(self, weight, start, end, enabled):
		self.weight = weight
		self.start = start
		self.end = end
		self.enabled = enabled
		self.genetic_marker = self.genetic_marker_control
		NEATComponent.genetic_marker_control += 1

		end.addInput(self)
		start.addOutput(self)

	def __str__(self):
		return "start: " + str(self.start.node_num) + " end:" + str(self.end.node_num) + " weight: " + str(self.weight) + " on: " + str(self.enabled) + ' genetic_marker:' + str(self.genetic_marker)  + "\n"

	def __deepcopy__(self, memo):
		return copy.copy(self)

	def setWeight(self, weight):
		self.weight = weight

	def getWeight(self):
		return self.weight

	def send(self, package):
		if self.enabled:
			self.end.receive(package*self.getWeight())
		else:
			self.end.receive(0)
