# A class to represent a neural net for the NEAT algorithm


class NEATComponent:
	genetic_marker_control = 0

class NeuralNet:

	def __init__(self):
		self.nodes = []
	 	self.connections = []


	class Node(NEATComponent):
		def __init__(self, weight, category):
			self.weight = weight
			self.category = category
			self.genetic_marker = self.genetic_marker_control
			self.genetic_marker_control += 1

		def setWeight(self, weight):
			self.weight = weight

		def getWeight(Self):
			return self.weight

	class Connection(NEATComponent):
		def  __init__(self, weight, start, end, enabled):
			self.weight = weight
			self.start = start
			self.end = end
			self.enabled = enabled
			self.genetic_marker = self.genetic_marker_control
			self.genetic_marker_control += 1

		def setWeight(self, weight):
			self.weight = weight

		 def getWeight(self):
		 	return self.weight

	def createNode(self, weight, category):
		self.nodes.append(self.Node(weight, category))

	def createConnection(self, weight, start, end, enabled):
		self.connections.append(self.Connection(weight, start, end, enabled))

	
