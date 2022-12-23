from utils.classes import *
from utils.predicates import *
from utils.actions import *

from llm import predicates_and_arguments_from_llm

import random
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tqdm import tqdm

def intersection_over_union(action, predicted_preconditions):
	'''
	Given an action and the set of predicted predicates for it, calculate the intersection over union metric.
	'''

	intersection_count = 0
	union_count = 0


	#TODO: make it so that action is a class (or something) so that predicates of preconditions can be directly grabbed from it rather than hardcoded here
	if action == "CloseObject":
		real_precondition= [(openable, ('receptacle_0',)), (opened, ('receptacle_0',)), (atLocation, ('agent_0', 'location_0')), (receptacleAtLocation, ('receptacle_0', 'location_0'))]

	#Calculate intersection
	for prec in real_precondition:
		if prec in predicted_preconditions:
			intersection_count += 1

	#Calculate union
	union_count = len(list(set(real_precondition+predicted_preconditions)))

	return(float(intersection_count)/float(union_count))

def generate_random_state():
	'''
	Generates a random low-level state.

	@return: a list of entities in low-level state
	'''

	#TODO: Make this more expressive and interesting. For, now generate a single object, receptacle and agent.

	#1) Generate the receptacle
	r = Receptacle(location = random.choice(list(Location)),
		opened = bool(random.choice([0,1])))

	#2) Generate the object
	o = Object(location = random.choice(list(Location)),
		clean = random.choice([True,False,None]),
		hot = random.choice([True,False,None]),
		toggled = random.choice([True,False,None]),
		sliced = random.choice([True,False,None]))

	#3) Generate robot
	a = Agent(location = random.choice(list(Location)),
		holding = random.choice([None, o]))

	return([r,o,a])


def generate_informed_state_predicates_and_arguments(predicates, arguments, epsilon=1.0):
	'''
	Generates a low-level state that, with some probability, satisfies the predicates and arguments

	@predicates: list of lifted predicates that we want to sample states from potentially
	@arguments: linked arguments we want to satisfy
	@epislon: the probability we gurantee a sample that satisifies predicates_arguments
	@return: a list of entities in low-level state
	'''

	#TODO: Make this more expressive and interesting. For, now generate a single object, receptacle and agent. This means the only things that can be linked are:
	#	-atLocaton, receptacleAtLocation and objectAtLocation (location)
	#TODO: currentl limited to not be able to deal with not preconditions but that is a limitation of high-level state description

	if random.random() <= epsilon: #gurantee predicates argument satiscation:
		receptacle_dict = {
		"opened": None,
		"location": None
		}

		agent_dict = {
		"holding": None,
		"location": None
		}

		object_dict = {
		"clean": None,
		"hot": None,
		"toggled": None,
		"sliced": None,
		"location": None
		}

		args_entities = {} #keys are unique names for arguments, values are entities

		if atLocation in predicates:
			atLocation_idx = predicates.index(atLocation)
			atLocation_arg = arguments[atLocation_idx][1] #location is second argument to this predicate
			if atLocation_arg in args_entities.keys():
				args_entities[atLocation_arg].append(agent_dict)
			else:
				args_entities[atLocation_arg] = [agent_dict]
		else:
			agent_dict['location'] = random.choice(list(Location))

		if receptacleAtLocation in predicates:
			reLocation_idx = predicates.index(receptacleAtLocation)
			reLocation_arg = arguments[reLocation_idx][1] #location is second argument to this predicate
			if reLocation_arg in args_entities.keys():
				args_entities[reLocation_arg].append(receptacle_dict)
			else:
				args_entities[atLocation_arg] = [receptacle_dict]
		else:
			receptacle_dict['location'] = random.choice(list(Location))

		if objectAtLocation in predicates:
			objLocation_idx = predicates.index(objectAtLocation)
			objLocation_arg = arguments[objLocation_idx][1] #location is second argument to this predicate
			if objLocation_arg in args_entities.keys():
				args_entities[objLocation_arg].append(object_dict)
			else:
				args_entities[objLocation_arg] = [object_dict]
		else:
			object_dict['location'] = random.choice(list(Location))

		#TODO: this part could be done in conjunction with previous part
		args_locations = {}
		for arg_name in args_entities.keys():
			args_locations[arg_name] = random.choice(list(Location))


		for _, (arg_name, list_of_entities) in enumerate(args_entities.items()):
			for entity in list_of_entities:
				entity['location'] = args_locations[arg_name]

		#Receptacle-only predicates
		if opened in predicates:
			receptacle_dict["opened"] = True
		elif openable in predicates:
			receptacle_dict["opened"] = random.choice([True,False])
		else:
			receptacle_dict["opened"] = random.choice([True, False, None])

		#Object-only predicates
		if isClean in predicates:
			object_dict["clean"] = True
		elif cleanable in predicates:
			object_dict["clean"] = random.choice([True, False])
		else:
			object_dict["clean"] = random.choice([True, False, None])

		if isHot in predicates:
			object_dict["hot"] = True
		elif heatable in predicates:
			object_dict["hot"] = random.choice([True, False])
		else:
			object_dict["hot"] = random.choice([True, False, None])

		if isToggled in predicates:
			object_dict["toggled"] = True
		elif toggleable in predicates:
			object_dict["toggled"] = random.choice([True, False])
		else:
			object_dict["toggled"] = random.choice([True, False, None])

		if isSliced in predicates:
			object_dict["sliced"] = True
		elif sliceable in predicates:
			object_dict["sliced"] = random.choice([True, False])
		else:
			object_dict["sliced"] = random.choice([True, False, None])

		#TODO: unpack these in smarter way using *?
		#Make receptacle object
		r = Receptacle(location = receptacle_dict["location"],
		opened = receptacle_dict["opened"])

		#Generate the object
		o = Object(location = object_dict["location"],
			clean = object_dict["clean"],
			hot = object_dict["hot"],
			toggled = object_dict["toggled"],
			sliced = object_dict["sliced"])

		if holdsAny in predicates:
			agent_dict["holding"] = o

		#Make agent
		a = Agent(location = agent_dict["location"],
			holding = agent_dict["holding"])





	else:
		#1) Generate the receptacle
		r = Receptacle(location = random.choice(list(Location)),
			opened = bool(random.choice([0,1])))

		#2) Generate the object
		o = Object(location = random.choice(list(Location)),
			clean = random.choice([True,False,None]),
			hot = random.choice([True,False,None]),
			toggled = random.choice([True,False,None]),
			sliced = random.choice([True,False,None]))

		#3) Generate robot
		a = Agent(location = random.choice(list(Location)),
			holding = random.choice([None, o]))

	return([r,o,a])


def generate_informed_state_predicates_only(predicates, epsilon=1.0):
	'''
	Generates a low-level state that, with some probability, satisfies the predicates.

	@predicates: list of lifted predicates that we want to sample states from potentially
	@epislon: the probability we gurantee a sample that satisifies predicates_arguments
	@return: a list of entities in low-level state
	'''

	#TODO: Make this more expressive and interesting. For, now generate a single object, receptacle and agent.
	#TODO: Should take into account arguments as an additional component to leverage
	#TODO: currentl limited to not be able to deal with not preconditions but that is a limitation of high-level state description
	#TODO: location for all entities is weirdly hard-coded right now. Since arguments can't be passed in, and every entity has to have a location, it's just hardcoded into object instatation that they have a random location

	if random.random() <= epsilon: #gurantee predicates argument satiscation:
		receptacle_dict = {
		"opened": None,
		"location": random.choice(list(Location))
		}

		agent_dict = {
		"holding": None,
		"location": random.choice(list(Location))
		}

		object_dict = {
		"clean": None,
		"hot": None,
		"toggled": None,
		"sliced": None,
		"location": random.choice(list(Location))
		}

		#Receptacle-only predicates
		if opened in predicates:
			receptacle_dict["opened"] = True
		elif openable in predicates:
			receptacle_dict["opened"] = random.choice([True,False])
		else:
			receptacle_dict["opened"] = random.choice([True, False, None])

		#Object-only predicates
		if isClean in predicates:
			object_dict["clean"] = True
		elif cleanable in predicates:
			object_dict["clean"] = random.choice([True, False])
		else:
			object_dict["clean"] = random.choice([True, False, None])

		if isHot in predicates:
			object_dict["hot"] = True
		elif heatable in predicates:
			object_dict["hot"] = random.choice([True, False])
		else:
			object_dict["hot"] = random.choice([True, False, None])

		if isToggled in predicates:
			object_dict["toggled"] = True
		elif toggleable in predicates:
			object_dict["toggled"] = random.choice([True, False])
		else:
			object_dict["toggled"] = random.choice([True, False, None])

		if isSliced in predicates:
			object_dict["sliced"] = True
		elif sliceable in predicates:
			object_dict["sliced"] = random.choice([True, False])
		else:
			object_dict["sliced"] = random.choice([True, False, None])

		#TODO: unpack these in smarter way using *?
		#Make receptacle object
		r = Receptacle(location = receptacle_dict["location"],
		opened = receptacle_dict["opened"])

		#Generate the object
		o = Object(location = object_dict["location"],
			clean = object_dict["clean"],
			hot = object_dict["hot"],
			toggled = object_dict["toggled"],
			sliced = object_dict["sliced"])

		if holdsAny in predicates:
			agent_dict["holding"] = o

		#Make agent
		a = Agent(location = agent_dict["location"],
			holding = agent_dict["holding"])





	else:
		#1) Generate the receptacle
		r = Receptacle(location = random.choice(list(Location)),
			opened = bool(random.choice([0,1])))

		#2) Generate the object
		o = Object(location = random.choice(list(Location)),
			clean = random.choice([True,False,None]),
			hot = random.choice([True,False,None]),
			toggled = random.choice([True,False,None]),
			sliced = random.choice([True,False,None]))

		#3) Generate robot
		a = Agent(location = random.choice(list(Location)),
			holding = random.choice([None, o]))

	return([r,o,a])


def learn_preconditions(generate_state,predicates=None,arguments=None,epsilon=1,num_samples = 10):
	'''
	General function for learning preconditions.

	@generate_state: returns a low-level state to try rolling policy from. May scope what states can be sampled based on predicates and arguments
	@predicates: list of predicates to restrict generate_state. if None, just samples random state
	@arguments: list of argument links to restrict predicates for generate_state. If none, just make random links for predicates.
	@num_samples: number of states to try

	'''
	#TODO: Make this be able to have an action passed in as an argument


	#1) Generate dataset of lifted states
	lifted_dataset = []
	for _ in range(num_samples):
		#Auto-generate random state
		if predicates == None:
			low_level_state = generate_state()
		elif arguments == None:
			low_level_state = generate_state(predicates=predicates,epsilon=epsilon)
		else:
			low_level_state = generate_state(predicates=predicates,arguments=arguments,epsilon=epsilon)

		#Convert to high-level state based on predicates
		high_level_state = generate_grounded_predicates(low_level_state)


		#Check if action feasible
		#TODO: This assumes low-level state has specific ordering (r,o,a), make low-level state be a dict potentially and index accordingly?
		#TODO: This already assumes we have the class-level arguments to the action, might want to relax that, or somehow do choosing when multiple objects are involved??
		can_close = CloseObject(low_level_state[2], low_level_state[2].location, low_level_state[0])

		#Get lifted version of high-level state
		lifted_high_level_state = lift_grounded_predicates(high_level_state)

		#Add lifted and action success to dataset
		lifted_dataset.append([lifted_high_level_state, can_close])

	#Filter only succesful states
	succesful_lifted_dataset = [d[0] for d in lifted_dataset if d[1]]

	if len(succesful_lifted_dataset) == 0:
		#TODO: Should i just be returning this as 0? or skip over?
		#print("random_baseline: No states had succesful execution of action, can not learn any predicates")
		pass

	#[print(sld) for sld in succesful_lifted_dataset]

	preconditions = []

	#print("\n")

	#TODO: This approach assumes preconditions are only interesections of predictions and does not take into account any notion of noisy samples

	#TODO: this seems ineffecient way of checking if lifted predicate was in every positive high-level state, make this more effecient?

	for hls_0 in succesful_lifted_dataset: #for each high-level state
		for lifted_pred_arg in hls_0: #for every lifted predicate-argument pair
			in_all = True
			for hls_1 in succesful_lifted_dataset:
				if lifted_pred_arg not in hls_1:
					in_all = False
			if in_all and lifted_pred_arg not in preconditions:
				preconditions.append(lifted_pred_arg)

	#print(preconditions)
	return(preconditions)


if __name__ == "__main__":
	#TODO: extend this to learning effects?

	#Hyperparameters
	#Different number of samples to try
	num_samples_list = list(np.arange(0,150,10))
	#Number of seeds
	num_seeds = 10
	#Episilon used for sampling (we sample according to informed data epislon probability)
	epsilon = 0.7
	#TODO: put action and action description in a list to choose from
	#action to do and description 
	#TODO: This is not actually properly integrated in
	action = "CloseObject"
	action_description = "agent closes receptacle action"

	premade_predicates = [opened,atLocation,receptacleAtLocation, objectAtLocation]
	premade_arguments = [['receptacle_0'],['agent_0','loc1'],['receptacle_0','loc1'],['object_0','location2']]


	random_scores_seeds = []
	informed_scores_seeds = []
	informed_args_scores_seeds = []
	llm_scores_seeds = []

	#TODO: Currently, for all seeds and all runs, ping LLM once. could be moved inside but more expensive for expermentation.
	llm_predicates, llm_arguments = predicates_and_arguments_from_llm(action=action,action_description=action_description)

	for seed in tqdm(range(num_seeds)):
		random_scores = []
		for num_samples in num_samples_list:
			preconditions = learn_preconditions(generate_random_state,num_samples=num_samples)

			#TODO: This method of scoring may not be best?
			score = intersection_over_union("CloseObject", preconditions)
			random_scores.append(score)

		informed_scores = []
		for num_samples in num_samples_list:
			preconditions = learn_preconditions(generate_informed_state_predicates_only,predicates=premade_predicates,epsilon=epsilon,num_samples=num_samples)

			#TODO: This method of scoring may not be best?
			score = intersection_over_union("CloseObject", preconditions)
			informed_scores.append(score)

		informed_args_scores = []
		for num_samples in num_samples_list:
			preconditions = learn_preconditions(generate_informed_state_predicates_and_arguments,predicates=premade_predicates,arguments=premade_arguments,epsilon=epsilon,num_samples=num_samples)

			#TODO: This method of scoring may not be best?
			score = intersection_over_union("CloseObject", preconditions)
			informed_args_scores.append(score)

		llm_scores = []
		for num_samples in num_samples_list:
			preconditions = learn_preconditions(generate_informed_state_predicates_and_arguments,predicates=llm_predicates,arguments=llm_arguments,epsilon=epsilon,num_samples=num_samples)

			#TODO: This method of scoring may not be best?
			score = intersection_over_union("CloseObject", preconditions)
			llm_scores.append(score)

		random_scores_seeds.append(random_scores)
		informed_scores_seeds.append(informed_scores)
		informed_args_scores_seeds.append(informed_args_scores)
		llm_scores_seeds.append(llm_scores)

	np_random_scores = np.array(random_scores_seeds)
	np_informed_scores = np.array(informed_scores_seeds)
	np_informed_args_scores = np.array(informed_args_scores_seeds)
	np_llm_scores = np.array(llm_scores_seeds)

	random_avgs = np.average(np_random_scores, axis=0)
	random_stds = np.std(np_random_scores, axis=0)

	informed_avgs = np.average(np_informed_scores, axis=0)
	informed_stds = np.std(np_informed_scores, axis=0)

	informed_args_avgs = np.average(np_informed_args_scores, axis=0)
	informed_args_stds = np.std(np_informed_args_scores, axis=0)

	llm_avgs = np.average(np_llm_scores, axis=0)
	llm_stds = np.std(np_llm_scores, axis=0)

	sns.set_theme()

	plt.plot(num_samples_list,random_avgs,label="random")
	plt.fill_between(num_samples_list, random_avgs - random_stds, random_avgs + random_stds, color='blue', alpha=0.2)

	plt.plot(num_samples_list,informed_avgs,label="informed with lifted predicates")
	plt.fill_between(num_samples_list, informed_avgs - informed_stds, informed_avgs + informed_stds, color='orange', alpha=0.2)

	plt.plot(num_samples_list,informed_args_avgs,label="informed with lifted predicates and arguments")
	plt.fill_between(num_samples_list, informed_args_avgs - informed_args_stds, informed_args_avgs + informed_args_stds, color='green', alpha=0.2)

	plt.plot(num_samples_list,llm_avgs,label="LLM prior")
	plt.fill_between(num_samples_list, llm_avgs - llm_stds, llm_avgs + llm_stds, color='red', alpha=0.2)

	plt.legend(loc="lower right")
	plt.xlabel("Number of policy rollouts")
	plt.ylabel("Intersection over Union")
	plt.title("Number of samples vs initation set classification success\n{action}".format(action=action))
	plt.show()

