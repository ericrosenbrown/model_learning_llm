import openai
from utils.predicates import PREDICATES

def generate_response_from_llm(action: str, action_description: str):
	'''
	Generates a response from the LLM with the action as the desired action
	@action: natural language name of action
	@action_description: a description of the action
	'''

	prompt = ";; Specification in PDDL1 of the Extended Task domain\n\n(define (domain put_task)\n (:requirements\n  :adl\n )\n (:types\n  agent\n  location\n  receptacle\n  object\n  )\n\n\n (:predicates\n    (atLocation ?a - agent ?l - location)                     ; true if the agent is at the location\n    (receptacleAtLocation ?r - receptacle ?l - location)      ; true if the receptacle is at the location (constant)\n    (objectAtLocation ?o - object ?l - location)              ; true if the object is at the location\n    (openable ?r - receptacle)                                ; true if a receptacle is openable\n    (opened ?r - receptacle)                                  ; true if a receptacle is opened\n    (holds ?a - agent ?o - object)                            ; object ?o is held by agent ?a\n    (holdsAny ?a - agent)                                     ; agent ?a holds an object\n    (isClean ?o - object)                                     ; true if the object has been clean in sink\n    (cleanable ?o - object)                                   ; true if the object can be placed in a sink\n    (isHot ?o - object)                                       ; true if the object has been heated up\n    (heatable ?o - object)                                    ; true if the object can be heated up in a microwave\n    (toggleable ?o - object)                                  ; true if the object can be turned on/off\n    (isToggled ?o - object)                                   ; true if the object has been toggled\n    (sliceable ?o - object)                                   ; true if the object can be sliced\n    (isSliced ?o - object)                                    ; true if the object is sliced\n )\n\n;;{action_description}\n (:action {action}\n:precondition ".format(action=action,action_description=action_description)


	models = ["code-davinci-002",
	"text-davinci-003"]
	# create a completion
	completion = openai.Completion.create(engine=models[0],
	prompt=prompt,
	max_tokens=100,
	temperature=0
	)

	# print the completion
	response = completion.choices[0].text
	return(response)

def parse_response_from_llm(response):
	'''
	Take the response from the LLM and parse the preconditions into a predicates/arguments representation suitable for the learning algorithm.

	@response: the response from the LLM
	'''

	#TODO: this parsing is a little hard-coded and assumes the LLM will give same strucutre each time, should probably be more robust, either in how data is prompted or how we extract. For example, will break if not is involved, or not fully generated outputs
	predicates = []
	arguments = []
	for line in response.split("\n"):
		if line.strip(" ") == ")": #we've hit the end of preconditions, bread
			break
		else:
			split_line = line.split("(")
			#print(split_line)
			#parse line till we see predicate in it
			print(split_line)
			if 'not ' in split_line:
				#TODO: we can't handle not, skip over
				continue
			for piece in split_line:
				for predicate_name in PREDICATES:
					#TODO: there is a bug on the line below where if one predicate is the substring of another (e.g: holds for holdsAny), it will get activated here too, which is not good at all. instead, predicate_name.__name__ needs to uniquely match a part of piece. come back to this later?
					if predicate_name.__name__ in piece: #we found the piece with the predicate, start parsing
						split_piece = piece.split(" ")
						#TODO: we can not handle nots, skip over
						#print(split_piece)
						#Assumes that predicate is first in split, and the following are argument names
						predicates.append(predicate_name)
						args = []
						for arg in split_piece[1:]:
							arg = arg.replace(")","") #Removes ) at the end, normally happens with last argument
							args.append(arg)
						arguments.append(args)
	return(predicates,arguments)

def predicates_and_arguments_from_llm(action,action_description):
	#response = generate_response_from_llm(action=action, action_description=action_description)

	#####ToggleObjectOff responses
	response="(and (atLocation ?agent ?location)\n                   (objectAtLocation ?object ?location)\n                   (toggleable ?object)\n                   (isToggled ?object)\n                   )\n:effect (and (not (isToggled ?object))\n             )\n)\n\n;;agent toggles on object action\n (:action ToggleOnObject\n:precondition (and (atLocation ?agent ?location)\n                   (objectAtLocation ?object\n"

	#####CloseObject Responses
	#response = "(and (atLocation ?agent ?location)\n                  (receptacleAtLocation ?receptacle ?location)\n                  (openable ?receptacle)\n                  (opened ?receptacle)\n                  )\n:effect (and (not (opened ?receptacle))\n             )\n)\n\n;;agent opens receptacle action\n (:action OpenReceptacle\n:precondition (and (atLocation ?agent ?location)\n                  (re\n"

	#response="(and (atLocation ?agent ?location)\n                   (receptacleAtLocation ?receptacle ?location)\n                   (openable ?receptacle)\n                   (opened ?receptacle)\n                   (not (holdsAny ?agent))\n                   )\n:effect (and (not (opened ?receptacle))\n             )\n)\n\n;;agent opens receptacle action\n"

	#This response is wrong for CloseObject, includes holding receptacle, which isn't even a valid predicate!
	#response="(and (atLocation ?agent ?location)\n                   (receptacleAtLocation ?receptacle ?location)\n                   (openable ?receptacle)\n                   (opened ?receptacle)\n                   (holds ?agent ?receptacle)\n                   )\n:effect (and (not (opened ?receptacle))\n             )\n)\n"

	print("Action:\n{action}\n\nDescription:\n{description}\n\nLLM Response:\n{response}".format(action=action, description=action_description,response=response))

	predicates, arguments = parse_response_from_llm(response)
	print("predicates and arguments extracted from LLM:\n{pa}".format(pa=list(zip(predicates,arguments))))

	return(predicates,arguments)


if __name__ == "__main__":
	action = "CloseReceptacle"
	action_description = "agent closes receptacle action"
	predicates_and_arguments_from_llm(action,action_description)