import neural_net, unittest, copy



# test_net = neural_net.NeuralNet()

# for i in range(0,5):
# 	test_net.createSensorNode(0)
# 	test_net.createOutputNode(2)
# 	test_net.createConnection(1,test_net.sensorNodes[i], test_net.outputNodes[i], True)

# print test_net.process([1,1,5,1,1])

# test_net.createHiddenNode(0)
# test_net.createConnection(1,test_net.sensorNodes[0],test_net.hiddenNodes[0], True)
# test_net.createConnection(1,test_net.hiddenNodes[0],test_net.outputNodes[0], True)

# print test_net.process([1,1,1,1,1])

# print test_net

# test_net.mutate_connection(-1, 1)

# print "mutate connection"
# print test_net

# test_net.mutate_node(-1,1)
# print "mutate node"
# print test_net

# test_net.mutate_weight(-1000, -990)
# print "mutate weight"
# print test_net


print "testing deep copy"
test_net1 = neural_net.NeuralNet()
test_net1.createSensorNode(0)
test_net1.createOutputNode(0)
test_net1.createConnection(1, test_net1.sensorNodes[0], test_net1.outputNodes[0], True)

print test_net1

test_net2 = copy.deepcopy(test_net1)

test_net1.mutate_node(-1, 1)
test_net2.mutate_connection(-1, 1)

test_net2.sensorNodes[0].setWeight(2)


print test_net1
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print test_net2

merged_net = neural_net.NEAT_merge_nets(test_net1, test_net2)
print "merged_net"
print merged_net
