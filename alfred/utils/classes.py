from enum import Enum


class Location(Enum):
	KITCHEN = 1
	BEDROOM = 2
	OFFICE = 3
	LIVING_ROOM = 4

#TODO: Type hints are a lie for bool, they can be none. Maybe do some better way to deal with open/openable etc.
class Object:
	def __init__(self, location: Location, clean: bool, hot: bool, toggled: bool, sliced: bool):
		self.location = location
		self.clean = clean
		self.hot = hot
		self.toggled = toggled
		self.sliced = sliced
		#TODO: Write equals function over attributes, and for other classes (maybe?)
	def __str__(self):
		ret_string = "Object | "
		ret_string += "Location: {l} | ".format(l=str(self.location))
		ret_string += "Clean: {c} | ".format(c=str(self.clean))
		ret_string += "Hot: {h} | ".format(h=str(self.hot))
		ret_string += "Toggled {t} | ".format(t=str(self.toggled))
		ret_string += "Sliced {s} | ".format(s=str(self.sliced))
		return(ret_string)


class Agent:
	def __init__(self, location: Location, holding: Object):
		self.location = location
		self.holding = holding
	def __str__(self):
		ret_string = "Agent | "
		ret_string += "Location {l} | ".format(l=str(self.location))
		ret_string += "Holding {h} | ".format(h=str(self.holding))
		return(ret_string)

class Receptacle:
	def __init__(self, location: Location, opened: bool):
		self.location = location
		self.opened = opened
	def __str__(self):
		ret_string = "Receptacle | "
		ret_string += "Location {l} | ".format(l=str(self.location))
		ret_string += "Opened {o} | ".format(o=str(self.opened))
		return(ret_string)


if __name__ == "__main__":
	#Test Location
	assert Location.KITCHEN in Location

	#Test object
	bread1 = Object(location = Location.KITCHEN,
					clean = None,
					hot = False,
					toggled = None,
					sliced = True,
					opened = None)

	#Test Agent
	agent1 = Agent(location = Location.KITCHEN,
				   holding = bread1)

	#TODO: write test cases
