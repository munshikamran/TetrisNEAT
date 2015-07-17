# A class to represent a neural net for the NEAT algorithm




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
		self.hiddenNodes.append(Node(threshold, self.node_num))
		self.node_num += 1

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


	def setThreshold(self, threshold):
		self.threshold = threshold

	def getThreshold(self):
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
			if tot >= self.getThreshold():
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
		self.genetic_marker_control += 1

		end.addInput(self)
		start.addOutput(self)

	def __str__(self):
		return "start: " + str(self.start.node_num) + " end:" + str(self.end.node_num) + " weight: " + str(self.weight) + " on: " + str(self.enabled) + "\n"

	def setWeight(self, weight):
		self.weight = weight

	def getWeight(self):
		return self.weight

	def send(self, package):
		if self.enabled:
			self.end.receive(package*self.getWeight())
		else:
			self.end.receive(0)
