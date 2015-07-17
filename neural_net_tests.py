import neural_net, unittest



test_net = neural_net.NeuralNet()

for i in range(0,5):
	test_net.createSensorNode(0)
	test_net.createOutputNode(2)
	test_net.createConnection(1,test_net.sensorNodes[i], test_net.outputNodes[i], True)

print test_net.process([1,1,5,1,1])

test_net.createHiddenNode(0)
test_net.createConnection(1,test_net.sensorNodes[0],test_net.hiddenNodes[0], True)
test_net.createConnection(1,test_net.hiddenNodes[0],test_net.outputNodes[0], True)

print test_net.process([1,1,1,1,1])

print test_net