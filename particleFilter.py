import random
import scipy.stats
import phone
import math

def randomInitialization(n, lowerX, lowerY, upperX, upperY):
	xLength = upperX - lowerX
	yLength = upperY - lowerY
	returnList = []
	for i in range(0, n):
		returnList.append((phone.Vector(random.random()*xLength + lowerX, random.random()*yLength + lowerY), 1.0))
	return returnList

def smarterInitialization(n, distance):
	returnList = []
	sigma = 1.0
	for i in range(0, n):
		theta = random.random()*2*math.pi
		dist = random.gauss(distance, sigma)
		returnList.append((phone.Vector(dist*math.cos(theta), dist*math.sin(theta)),1.0))
	return returnList

def addNoise(diff, sigma):
	return phone.Vector(random.gauss(diff.xDiff, sigma), random.gauss(diff.yDiff, sigma))

def getNewPoint(oldDiff, diff, sigma):
	return addNoise(oldDiff.add(diff.multiply(-1.0)), sigma)

def getWeight(particleVector, distance, sigma, guessLocation = None):
	fastWeight = 1.0/(distance - particleVector.abs())**2
	# weight = scipy.stats.norm(distance, sigma*0.5).pdf(particleVector.abs())
	if guessLocation != None:
		diff = particleVector.add(guessLocation.multiply(-1.0)).abs()
		# weight = weight/2.0 + scipy.stats.norm(0, sigma*0.5).pdf(diff)/2.0
		fastWeight = fastWeight/2.0 + 1.0/(2.0*diff**2)
	return fastWeight


def updateParticles(diff, particles, newDistance, sigma, guessLocation = None):
	weights = []
	oldWeightsMax = 0
	for i in range(0, len(particles)):
		weights.append(particles[i][1]*getWeight(particles[i][0].add(diff.multiply(-1.0)), newDistance, sigma, guessLocation)**2)
		oldWeightsMax = max(oldWeightsMax, particles[i][1])
		if i == 0:
			print particles[i][1]
	numParticles = 0
	newParticles = []
	iterator = 0
	while numParticles < len(particles):
		if random.random() < weights[iterator%len(particles)]/oldWeightsMax:
			newParticles.append((getNewPoint(particles[iterator%len(particles)][0], diff, sigma), 
				# weights[iterator%len(particles)]/oldWeightsMax))
				1))
			numParticles += 1
		iterator += 1
	# print particles
	return newParticles

def getMaxParticle(particles, distance):
	maxWeight = 0
	maxParticle = None
	sigma = 1.0
	# print "Particles: " + str(particles)
	for i in range(0, len(particles)):
		weight = getWeight(particles[i][0], distance, sigma)
		# print weight
		if weight > maxWeight:
			maxWeight = weight
			maxParticle = particles[i][0]
	return maxParticle

def getAverageParticle(particles):
	vec = phone.Vector(0,0)
	for particle in particles:
		vec = vec.add(particle[0].multiply(1.0/len(particles)))
	return vec

def getRefinedAverage(particles):
	avg = phone.Vector(0,0)
	for particle in particles:
		avg = avg.add(particle[0].multiply(1.0/len(particles)))
	var = 0.0
	diffs = []
	for i in range (0, len(particles)):
		var += particles[i][0].add(avg.multiply(-1.0)).abs()**2
	var = var/len(particles)
	ret = phone.Vector(0,0)
	num = 0
	for particle in particles:
		if (particle[0].add(avg.multiply(-1.0)).abs() < var*0.8):
			ret = ret.add(particle[0])
			num += 1
	# print num
	print "var = " + str(var/avg.abs())
	return ret.multiply(((1.0 + math.sqrt(var)/(avg.abs()**1.5))/max(num,1)))

def getRefinedAverageVec(particles):
	avg = phone.Vector(0,0)
	for particle in particles:
		avg = avg.add(particle.multiply(1.0/len(particles)))
	var = 0.0
	diffs = []
	for i in range (0, len(particles)):
		var += particles[i].add(avg.multiply(-1.0)).abs()**2
	var = var/len(particles)
	ret = phone.Vector(0,0)
	num = 0
	for particle in particles:
		if (particle.add(avg.multiply(-1.0)).abs() < var*0.8):
			ret = ret.add(particle)
			num += 1
	# print num
	print "var = " + str(var/avg.abs())
	return ret.multiply(((1.0 + math.sqrt(var)/(avg.abs()**1.5))/max(num,1)))



