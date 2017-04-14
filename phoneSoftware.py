import math
import phone
import particleFilter
import phone as phone
import particleFilterTheta

class PhoneSoftware:

	def __init__(self, world, phoneHardware):
		self.world = world
		self.phoneHardware = phoneHardware
		self.hardware = phoneHardware
		self.previousGuesses = []
		self.bestGuess = None
		# self.particles = particleFilter.randomInitialization(1000, -20, -20, 20, 20)
		# self.particles = particleFilter.smarterInitialization()
		self.particles = []


		self.otherRouters = {}
		self.otherGuess = []
		for i in range(0, len(self.world.routerList)):
			router = self.world.routerList[i]
			if not router.equals(phoneHardware):
				self.otherRouters[i] = self.getDistanceOtherPhone(router)
				self.particles.append([])
				self.otherGuess.append(None)
		self.otherPhones = {}

		for i in range(0, len(self.world.phoneList)):
			otherPhone = self.world.phoneList[i]
			if not otherPhone.equals(phoneHardware):
				self.otherPhones[i] = phone.Vector(0,0)

		# self.otherRouters = otherRouters

		

	def getDistanceOtherPhone(self, otherPhone):
		return self.world.getDistance(self.hardware, otherPhone, 0.3)

	def updateParticleTheta(self):
		selfMoved = self.hardware.getAmountMoved()
		sigma = 1.0
		returnList = []
		for i in range(0, len(self.world.routerList)):
			otherDevice = self.world.routerList[i]
			distance = self.getDistanceOtherPhone(otherDevice)
			if self.particles[i] == []:
				self.particles[i] = particleFilterTheta.smarterInitialization(1000)
			if self.world.stepNumber > 1:
				self.particles[i] = particleFilterTheta.updateParticles(selfMoved, self.particles[i], distance, self.routers[i], sigma)
			returnList.append((particleFilterTheta.complexAverage(self.particles[i]), self.particles[i]))
		return returnList


	def updateParticle(self):
		selfMoved = self.hardware.getAmountMoved()
		sigma = 1.0
		returnList = []
		for i in range(0, len(self.world.routerList)):
			# print self.otherRouters
			otherDevice = self.world.routerList[i]
			distance = self.getDistanceOtherPhone(otherDevice)
			if (self.particles[i] == []):
				self.particles[i] = particleFilter.smarterInitialization(1000, distance)
			if self.world.stepNumber > 1:
				self.particles[i] = particleFilter.updateParticles( selfMoved, self.particles[i], distance, sigma, self.otherGuess[i])
			else:
				self.particles[i] = particleFilter.updateParticles( selfMoved, self.particles[i], distance, sigma)
			returnList.append((particleFilter.getRefinedAverage(self.particles[i]), self.particles[i]))
		return returnList


	def update(self):
		selfMoved = self.hardware.getAmountMoved()
		first = None
		second = None
		for otherPhone in self.otherRouters:
			distance = self.getDistanceOtherPhone(otherPhone)
			oldDistance = self.otherRouters[otherPhone]
			self.otherRouters[otherPhone] = distance
			otherMoved = otherPhone.getAmountMoved()
			#This is how far this phone moved relative to the other one
			relativePositionDiff = selfMoved.add(otherMoved.multiply(-1.0))
			print relativePositionDiff
			distanceDiff = oldDistance

			sign = lambda a: 1 if a>=0 else -1
			theta = math.atan(relativePositionDiff.yDiff/(sign(relativePositionDiff.xDiff)*max(abs(
				relativePositionDiff.xDiff), 0.0000001)))
			if (relativePositionDiff.xDiff < 0):
				theta = theta + math.pi
			print theta*180/(math.pi)


			print oldDistance
			print relativePositionDiff.abs()
			print distance
			# r = (-1,(oldDistance**2 + relativePositionDiff.abs()**2 - distance**2)/
			# 	(2*oldDistance*relativePositionDiff.abs()))
			# print r

			t = math.acos(min(1,max(-1,(oldDistance**2 + relativePositionDiff.abs()**2 - distance**2)/
				(2*oldDistance*relativePositionDiff.abs()))))

			s = math.acos(min(1,max(-1,((oldDistance**2 - relativePositionDiff.abs()**2 + distance**2)/
				(max(2*oldDistance*distance, .0000001))%(1.0)))))

			if t < 0.001:
				s = 0
				print "adjustment1"
			if t > math.pi- 0.001:
				s = 0
				print "adjustment2"

			# print t*180/math.pi
			# print s*180/math.pi

			phi = t + theta + s
			# print (phi*180/(math.pi))%360
			other_phi = 2*theta - phi
			# print (other_phi*180/math.pi)%360
			first = phone.Vector(distance*math.cos(phi), distance*math.sin(phi))
			print first
			second = phone.Vector(distance*math.cos(other_phi), distance*math.sin(other_phi))
			print second
			if self.previousGuesses != []:
				bestGuess = None
				other = None
				minDist = 10**5
				print self.previousGuesses

				for oldGuess in self.previousGuesses:
					for currentGuess in [first, second]:
						dist = relativePositionDiff.add(currentGuess).add(oldGuess.multiply(-1)).getTotalDistance()
						if dist < minDist:
							minDist = dist
							bestGuess = currentGuess
				otherGuess = first
				if bestGuess == first:
					otherGuess = second
				if self.bestGuess == None:
					self.bestGuess = bestGuess
				else:					
					fac = abs(math.cos(t))
					self.bestGuess = self.bestGuess.multiply(fac).add(bestGuess.multiply(1-fac))

				self.previousGuesses = [bestGuess, otherGuess]

				return (self.bestGuess, otherGuess)
			else:

				self.previousGuesses = [first, second]
				return (first, second)





