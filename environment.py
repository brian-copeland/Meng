import phone 
import random
import phoneSoftware as software

class World:

	def __init__(self, multi):
		if multi:
			self.stepNumber = 0
			self.phone1 = phone.Phone(phone.Location(20.0,-20.0))
			self.phone2 = phone.Phone(phone.Location(10.0, 10.0))
			self.router1 = phone.Phone(phone.Location(10.0,0.0))
			self.router2 = phone.Phone(phone.Location(0.0, 10.0))
			self.router3 = phone.Phone(phone.Location(-10.0, -10.0))
			self.router4 = phone.Phone(phone.Location(-19.0, 19.0))
			self.router5 = phone.Phone(phone.Location(25.0, 0.0))
			self.router6 = phone.Phone(phone.Location(0.0, -10))

			self.router7 = phone.Phone(phone.Location(-19, 15.0))

			# self.routerList = [self.router1, self.router2, self.router3, self.router4]
			# self.routerList = [self.router1, self.router2, self.router3, self.router4, self.router5, self.router6, self.router7]
			self.routerList = [self.router1, self.router2, self.router3]

			self.phoneList = [self.phone1, self.phone2]

			self.phoneSoftware1 = software.PhoneSoftware(self, self.phone1)
			self.phoneSoftware2 = software.PhoneSoftware(self, self.phone2)
			self.phoneSoftwareList = [self.phoneSoftware1, self.phoneSoftware2]
			#self.phoneSoftware1 = software.PhoneSoftware(self, self.phone1)
			#self.phoneSoftware2 = software.PhoneSoftware(self, self.phone2)

		else:
			self.phone1 = phone.Phone(phone.Location(0.0,0.0))
			self.phone2 = phone.Phone(phone.Location(10.0, 10.0))
			self.phoneList = [self.phone1, self.phone2]
			self.phoneSoftware1 = software.PhoneSoftware(self, self.phone1)
			self.phoneSoftware2 = software.PhoneSoftware(self, self.phone2)

	def addPhone(self, phone):
		self.phoneList.append(phone)

	def getDistance(self, phone1, phone2, noise):
		actualDistance = phone1.getLocation().getLocationDifference(phone2.getLocation()).getTotalDistance()
		ran = (2*random.random() - 1.0)*noise
		# print "ran = " + str(ran)
		return (actualDistance + ran)

	def step(self, multi):
		self.stepNumber += 1
		if multi:
			self.phone1.moveFixed(phone.Vector(-0.5, 0.5))
			self.phone2.moveFixed(phone.Vector(-0.5, -0.2))
			return (self.phoneSoftware1.updateParticleTheta(), self.phoneSoftware2.updateParticleTheta())
		else:
			self.phone1.moveRandom()
			# self.phone2.moveRandom()
			return self.phoneSoftware1.updateParticle()[0]
			# print res1
			# print res2




# Main Method/functions
#world = World()
#world.step()

# print phone1.getLocation()


