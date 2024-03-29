import neural_net, random

class Tetris_NEAT_Agent:

	def __init__(self):
		self.net_species = {}
		self.species_delta = 3
		self.cur_species = 0
		self.cur_net = -1
		self.all_nets = self.net_species.items()
		self.num_species = len(self.net_species.keys())


	def get_state(self, board, stone, next_stone):
		heights = []
		for x in range(0, len(board[0])):
			count = 0
			for y in range(0, len(board)):
				count+=1
				if board[y][x] == 1:
					heights.append(count)
					break

		stone_num = [0, 0, 0, 0, 0, 0, 0]
		next_stone_num = [0, 0, 0, 0, 0, 0, 0]
		for y in range(0, len(stone)):
			if stone[y][0] > 0:
				stone_num[stone[y][0]-1] = 10
				break
		for y in range(0, len(next_stone)):
			if next_stone[y][0] > 0:
				next_stone_num[next_stone[y][0]-1] = 10
				break

		return heights + stone_num + next_stone_num

	def next_net(self):
		self.cur_net += 1
		if self.cur_net == len(self.all_nets[self.cur_species][1]):
			self.cur_net = 0
			self.cur_species += 1
		if self.cur_species == self.num_species:
			self.cur_species = 0
			self.cur_net = -1
			return None
		
		else:
			try:
				return (self.all_nets[self.cur_species][0], self.all_nets[self.cur_species][1][self.cur_net])
			except IndexError:
				print self.all_nets
				print self.cur_species
				print self.cur_net


	def output_to_move(self, output):
		# Translate the net output into a move (pos, rot)
		# The first 10 are the position, the next 4 are the rotation
		pos_choices = output[0:10]
		rot_choices = output[10:14]

		pos = pos_choices.index(max(pos_choices))
		rot = rot_choices.index(max(rot_choices))

		return (pos, rot)



	def create_initial_nets(self, sensors, output, pop, a, b):
		net_list = []
		for i in range(0, pop):
			neural_net.NEATComponent.genetic_marker_control = 0
			new_net = neural_net.NeuralNet()
			for s in range(0, sensors):
				new_net.createSensorNode(random.uniform(a,b))
			for o in range(0, output):
				new_net.createOutputNode(random.uniform(a,b))

			for s in range(0, sensors):
				for o in range(0, output):
					new_net.createConnection(random.uniform(a,b), new_net.sensorNodes[s], new_net.outputNodes[o], True)
			net_list.append(new_net)
		self.net_species[random.choice(net_list)] = net_list
		self.all_nets = self.net_species.items()
		self.num_species = len(self.net_species.keys())


	def create_new_generation(self, scores):
		#Take in a list of scores and nets and return the new generation

		# Pick a random net from each species to be the representative
		new_net_species = {}
		for species in self.net_species:
			new_net_species[random.choice(self.net_species[species])] = []

		new_nets = []
		# Now create children and add mutations
		for species in self.net_species.items():
			species_key = species[0]
			species_members = species[1]
			species_scores = scores[species_key]
			species_start = len(new_nets)
			species_size = len(species_members)

			while len(species_scores) > 1: # Make a limit of the number of new ones that can be added
				# Grab the top two nets
				first = max(species_scores)
				first_net = species_members[species_scores.index(first)]
				species_scores.remove(first)
				species_members.remove(first_net)

				second = max(species_scores)
				second_net = species_members[species_scores.index(second)]
				species_scores.remove(second)
				species_members.remove(second_net)

				# Make 1 kid wih the top two nets
				baby_net = neural_net.NEAT_merge_nets(first_net, second_net)

				# Add the new family to the list
				new_nets += [first_net, second_net, baby_net]
			new_nets = new_nets[:species_start + species_size-1]
			species_start += species_size

		# Mutate the nets
		for net in new_nets:
			if random.random() < .05:
				mutation_type = random.choice(["node", "weight", "connection"])
				if mutation_type == "node":
					net.mutate_node(-100, 100)
				if mutation_type == "weight":
					net.mutate_weight(-100, 100)
				if mutation_type == "connection":
					net.mutate_connection(-100, 100)

		# Sort all new nets into their species
		for net in new_nets:
			for species_id in new_net_species.keys():
				placed = False
				print self.calculate_difference(species_id, net)
				if self.calculate_difference(species_id, net) < self.species_delta:
					new_net_species[species_id].append(net)
					placed = True
					break
				if not placed:
					new_net_species[net] = [net]

		self.net_species = new_net_species
		self.all_nets = self.net_species.items()
		self.num_species = len(self.net_species.keys())



	def calculate_difference(self, net1, net2):
		net1_genes = net1.sensorNodes+net1.hiddenNodes+net1.outputNodes+net1.connections
		net2_genes = net2.sensorNodes+net2.hiddenNodes+net2.outputNodes+net2.connections

		num_genes = max(len(net1_genes), len(net2_genes))

		net1_genetics = []
		for gene in net1_genes:
			net1_genetics.append(gene.genetic_marker)
		net1_genetics.sort()
		net2_genetics = []
		for gene in net2_genes:
			net2_genetics.append(gene.genetic_marker)
		net2_genetics.sort()


		loop_length = len(net1_genetics) + len(net2_genetics)
		excess = 0
		disjoint = 0
		curr = 1
		average_weight_diff = 0
		n = 0
		while True:
			if len(net1_genetics) == 0 or len(net2_genetics) == 0:
				disjoint += excess
				excess = len(net1_genetics) + len(net2_genetics)
				break
			elif net1_genetics[0] < net2_genetics[0]:
				net1_genetics.pop(0)
				if curr == 1:
					excess += 1
				else:
					disjoint += excess
					excess = 1
				curr = 1
			elif net1_genetics[0] > net2_genetics[0]:
				net2_genetics.pop(0)
				if curr == 2:
					excess += 1
				else:
					disjoint += excess
					excess = 1
				curr = 2
			elif net1_genetics[0] == net2_genetics[0]:
				n += 1
				weight_diff = 0
				for gene in net1_genes:
					if gene.genetic_marker == net1_genetics[0]:
						weight_diff += gene.getWeight()
				for gene in net2_genes:
					if gene.genetic_marker == net2_genetics[0]:
						weight_diff -= gene.getWeight()
				average_weight_diff += abs(weight_diff)
				net1_genetics.pop(0)
				net2_genetics.pop(0)

		if n == 0:
			average_weight_diff = 0
		else:
			average_weight_diff = average_weight_diff/n

		c1 = 1.0
		c2 = 1.0
		c3 = 1.0/50.0

		return (c1*excess)/num_genes + (c2*disjoint)/num_genes + c3*average_weight_diff



