from utils.predicates import *
from utils.classes import *

def CloseObject(a: Agent, al: Location, r: Receptacle):
	return (atLocation(a, al)
		and receptacleAtLocation(r,al)
		and openable(r)
		and opened(r))

def ToggleOffObject(a: Agent, al: Location, o: Object):
	return (atLocation(a, al)
		and objectAtLocation(r,al)
		and toggleable(o)
		and isToggled(o))


