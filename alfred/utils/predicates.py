from utils.classes import *

def atLocation(a: Agent, l: Location) -> bool:
	return a.location == l

def receptacleAtLocation(r: Receptacle, l: Location) -> bool:
	return r.location == l

def objectAtLocation(o: Object, l: Location) -> bool:
	return o.location == l

def openable(r: Receptacle) -> bool:
	return not r.opened == None

def opened(r: Receptacle) -> bool:
	return r.opened

def holds(a: Agent, o: Object) -> bool:
	return a.holding == o

def holdsAny(a: Agent) -> bool:
	return not a.holding == None

def isClean(o: Object) -> bool:
	return o.clean

def cleanable(o: Object) -> bool:
	return not o.clean == None

def isHot(o: Object) -> bool:
	return o.hot

def heatable(o: Object) -> bool:
	return not o.hot == None

def isToggled(o: Object) -> bool:
	return o.toggled

def toggleable(o: Object) -> bool:
	return not o.toggled == None

def isSliced(o: Object) -> bool:
	return o.sliced

def sliceable(o: Object) -> bool:
	return not o.sliced == None

#Maybe put all of these inside a class to extract more easily?
PREDICATES = [
atLocation,
receptacleAtLocation,
objectAtLocation,
openable,
opened,
holds,
holdsAny,
isClean,
cleanable,
isHot,
heatable,
isToggled,
toggleable,
isSliced,
sliceable
]

def lift_grounded_predicates(high_level_state):
	'''
	Takes in a high-level state (lifted predicates with associated arguments), and returns a list of lifted predicates and arguments. This function essentially replaces each object in the arguments with a standardized variable naming convention for the class.
	'''

	lifted_high_level_state = []

	agent_list = []
	object_list = []
	receptacle_list = []
	location_list = []

	for pred, args in high_level_state:
		lifted_arguments = []
		for arg in args:
			if type(arg) == Agent:
				if arg not in agent_list:
					agent_list.append(arg)
				lifted_arguments.append("agent_"+str(agent_list.index(arg)))
				continue

			elif type(arg) == Object:
				if arg not in object_list:
					object_list.append(arg)
				lifted_arguments.append("object_"+str(object_list.index(arg)))
				continue

			elif type(arg) == Receptacle:
				if arg not in receptacle_list:
					receptacle_list.append(arg)
				lifted_arguments.append("receptacle_"+str(receptacle_list.index(arg)))
				continue

			elif type(arg) == Location:
				if arg not in location_list:
					location_list.append(arg)
				lifted_arguments.append("location_"+str(location_list.index(arg)))
				continue


			raise Exception("lifted_grounded_predicates: {arg} is not a valid object class".format(arg=type(arg)))

		lifted_arguments = tuple(lifted_arguments)
		lifted_high_level_state.append((pred, lifted_arguments))

	return(lifted_high_level_state)


def generate_grounded_predicates(entities: list) -> list:
	'''
	Takes in a list of entities in the environment, and returns a list of grounded predicates based on the entities

	@entities (list): A list of instantiated entities in the environment

	@return (list): A two-tuple, where the first element in the tuple is a list of lifted predicates that are true, and the second element is a list of argument to those lifted predicates that define their grounding. All other predicates are assumed to be false
	'''

	#TODO: this in a better way?

	#TODO: I can't capture preconditions with not, should just extend high-level state to inclue those

	#1) Sort entities into the different classes they are represented by

	agent_list = [e for e in entities if type(e) == Agent]
	object_list = [e for e in entities if type(e) == Object]
	receptacle_list = [e for e in entities if type(e) == Receptacle]

	#2) For each possible predicate, check if they are true for any possible combinations
	lifted_predicates = []
	arguments = []
	#TODO: This should go based on arguments in PREDICATES
	#Receptacle predicates
	for re in receptacle_list:
		if openable(re):
			lifted_predicates.append(openable)
			arguments.append([re])
		if opened(re):
			lifted_predicates.append(opened)
			arguments.append([re])

	#Agent predicates
	for a in agent_list:
		if holdsAny(a):
			lifted_predicates.append(holdsAny)
			arguments.append([a])

	#Object predicates
	for o in object_list:
		if isClean(o):
			lifted_predicates.append(isClean)
			arguments.append([o])
		if cleanable(o):
			lifted_predicates.append(cleanable)
			arguments.append([o])
		if isHot(o):
			lifted_predicates.append(isHot)
			arguments.append([o])
		if heatable(o):
			lifted_predicates.append(heatable)
			arguments.append([o])
		if isToggled(o):
			lifted_predicates.append(isToggled)
			arguments.append([o])
		if toggleable(o):
			lifted_predicates.append(toggleable)
			arguments.append([o])
		if isSliced(o):
			lifted_predicates.append(isSliced)
			arguments.append([o])
		if sliceable(o):
			lifted_predicates.append(sliceable)
			arguments.append([o])

	#Agent, Location
	for a in agent_list:
		for l in Location:
			if atLocation(a, l):
				lifted_predicates.append(atLocation)
				arguments.append([a, l])

	#Receptacle, Location
	for re in receptacle_list:
		for l in Location:
			if receptacleAtLocation(re, l):
				lifted_predicates.append(receptacleAtLocation)
				arguments.append([re, l])

	#Receptacle, Location
	for o in object_list:
		for l in Location:
			if objectAtLocation(o, l):
				lifted_predicates.append(objectAtLocation)
				arguments.append([o, l])

	#Agent, Object
	for a in agent_list:
		for o in object_list:
			if holds(a, o):
				lifted_predicates.append(holds)
				arguments.append([a, o])

	high_level_state = list(zip(lifted_predicates, arguments))
	return(high_level_state)

if __name__ == "__main__":
	bread1 = Object(location = Location.KITCHEN,
					clean = None,
					hot = False,
					toggled = None,
					sliced = True,
					opened = None)

	agent1 = Agent(location = Location.KITCHEN,
				   holding = bread1)

	assert atLocation(agent1, Location.KITCHEN)

	#Write test cases
