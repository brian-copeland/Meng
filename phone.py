import math
import random

class Vector:

	def __init__(self, xDiff, yDiff):
		self.xDiff = xDiff
		self.yDiff = yDiff

	def getTotalDistance(self):
		return  math.sqrt(self.xDiff**2 + self.yDiff**2)

	def add(self, other):
		return Vector(self.xDiff + other.xDiff, self.yDiff + other.yDiff)

	def multiply(self, scalar):
		return Vector(self.xDiff*scalar, self.yDiff*scalar)

	def abs(self):
		return math.sqrt(self.xDiff**2 + self.yDiff**2)

	def __str__(self):
		return "<"+ str(self.xDiff) + ", " + str(self.yDiff) + ">"

	def equal(self, other):
		return self.xDiff == other.xDiff and self.yDiff == other.yDiff

class Location:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def getLocationDifference(self, otherLoc):
		xDiff = otherLoc.x - self.x
		yDiff = otherLoc.y - self.y
		return Vector(xDiff, yDiff)

	def move(self, x, y):
		return Location(self.x + x, self.y + y)

	def __str__(self):
		return "<"+ str(self.x) + ", " + str(self.y) + ">"

	def add(self, vector):
		return Location(self.x + vector.xDiff, self.y + vector.yDiff)

class Phone:

	def __init__(self, location):
		self.location = location
		self.lastLocation = location

	def getLocation(self):
		return self.location

	def moveFixed(self, movedVector):
		self.lastLocation = self.location
		self.location = self.location.move(movedVector.xDiff, movedVector.yDiff)

	def moveRandom(self, limit = 1.0):
		ran1 = random.uniform(-1*limit,limit)
		ran2 = random.uniform(-1*limit,limit)
		self.lastLocation = self.location
		self.location = self.location.move(ran1, ran2)

	def getAmountMoved(self, error = 0.0):
		ran1 = random.uniform(-1*error,error)
		ran2 = random.uniform(-1*error,error)
		return Vector(-1*self.location.getLocationDifference(self.lastLocation).xDiff + \
				ran1, -1*self.location.getLocationDifference(self.lastLocation).yDiff + ran2)

	def equals(self, other):
		return self.location.x == other.location.x and self.location.y == other.location.y and \
				self.lastLocation.x == other.lastLocation.x and self.lastLocation.y == other.lastLocation.y

class WiFi(Phone):

	def moveRandom(self, limit = 1.0):
		return

	def getAmountMoved(self, error=0.0):
		return Vector(0.0,0.0)



		
   