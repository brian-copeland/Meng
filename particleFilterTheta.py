import random
import scipy.stats
import phone
import math
import cmath

def smarterInitialization(n):
	returnList = []
	sigma = 1.0
	for i in range(0, n):
		theta = random.random()*2*math.pi
		# dist = random.gauss(distance, sigma)
		returnList.append(theta)
	return returnList

def addNoise(diff, sigma):
	return phone.Vector(random.gauss(diff.xDiff, sigma), random.gauss(diff.yDiff, sigma))


def getPolarCoord(oldTheta, oldDist, diff):
	oldPoint = phone.Vector(math.cos(oldTheta)*oldDist, math.sin(oldTheta)*oldDist)
	newPoint = phone.Vector(oldPoint.x - diff.x, oldPoint.y - diff.y)
	return (math.atan(newPoint.x/newPoint.y), newPoint.abs())

def getNewTheta(oldTheta, cutoff=0.1):
	return (oldTheta + 2*cutoff*random.random() - 0.1)%2*math.pi



def getWeight(oldDistance, newDistance, sigma):
	return 1.0/math.abs(oldDistance - newDistance)**2

# def getNewPoint(oldTheta, oldLength, newDiff, newLength):

# 	return addNoise(oldDiff.add(diff.multiply(-1.0)), sigma)

# def getWeight(particleVector, distance, sigma, guessLocation = None):
# 	fastWeight = 1.0/(distance - particleVector.abs())**2
# 	# weight = scipy.stats.norm(distance, sigma*0.5).pdf(particleVector.abs())
# 	if guessLocation != None:
# 		diff = particleVector.add(guessLocation.multiply(-1.0)).abs()
# 		# weight = weight/2.0 + scipy.stats.norm(0, sigma*0.5).pdf(diff)/2.0
# 		fastWeight = fastWeight/2.0 + 1.0/(2.0*diff**2)
# 	return fastWeight

def updateParticles(amountMoved, particles, newDistance, oldDistance, sigma):
	weights = []
	oldWeightsMax = 0
	transformed = [getPolarCoord(theta, oldDistance, amountMoved) for theta in particles]
	for i in range(0, len(particles)):
		weights.append(getWeight(transformed[i][1], newDistance))
	oldWeightsMax = max(weights)

	numParticles = 0
	newParticles = []
	iterator = 0
	while numParticles < len(particles):
		if random.random() < weights[iterator%len(particles)]/oldWeightsMax:
			newParticles.append(getNewTheta(transformed[iterator%len(particles)][0]))
			numParticles += 1
		iterator += 1
	return newParticles
	
def complexAverage(thetas):
	#first convert to complex angle
	avg = complex(0,0)
	for theta in thetas:
		complexTheta = cmath.rect(1, theta)
		avg += complexTheta
	return cmath.polar(avg)[1]



# def updateParticles(diff, particles, newDistance, sigma, guessLocation = None):
# 	weights = []
# 	oldWeightsMax = 0
# 	for i in range(0, len(particles)):
# 		weights.append(particles[i][1]*getWeight(particles[i][0].add(diff.multiply(-1.0)), newDistance, sigma, guessLocation)**2)
# 		oldWeightsMax = max(oldWeightsMax, particles[i][1])
# 	numParticles = 0
# 	newParticles = []
# 	iterator = 0
# 	while numParticles < len(particles):
# 		if random.random() < weights[iterator%len(particles)]/oldWeightsMax:
# 			newParticles.append((getNewPoint(particles[iterator%len(particles)][0], diff, sigma), 
# 				# weights[iterator%len(particles)]/oldWeightsMax))
# 				1))
# 			numParticles += 1
# 		iterator += 1
# 	# print particles
# 	return newParticles

# def getMaxParticle(particles, distance):
# 	maxWeight = 0
# 	maxParticle = None
# 	sigma = 1.0
# 	# print "Particles: " + str(particles)
# 	for i in range(0, len(particles)):
# 		weight = getWeight(particles[i][0], distance, sigma)
# 		# print weight
# 		if weight > maxWeight:
# 			maxWeight = weight
# 			maxParticle = particles[i][0]
# 	return maxParticle

# def getAverageParticle(particles):
# 	vec = phone.Vector(0,0)
# 	for particle in particles:
# 		vec = vec.add(particle[0].multiply(1.0/len(particles)))
# 	return vec

# def getRefinedAverage(particles):
# 	avg = phone.Vector(0,0)
# 	for particle in particles:
# 		avg = avg.add(particle[0].multiply(1.0/len(particles)))
# 	var = 0.0
# 	diffs = []
# 	for i in range (0, len(particles)):
# 		var += particles[i][0].add(avg.multiply(-1.0)).abs()**2
# 	var = var/len(particles)
# 	ret = phone.Vector(0,0)
# 	num = 0
# 	for particle in particles:
# 		if (particle[0].add(avg.multiply(-1.0)).abs() < var*0.8):
# 			ret = ret.add(particle[0])
# 			num += 1
# 	# print num
# 	print "var = " + str(var/avg.abs())
# 	return ret.multiply(((1.0 + math.sqrt(var)/(avg.abs()**1.5))/max(num,1)))

# def getRefinedAverageVec(particles):
# 	avg = phone.Vector(0,0)
# 	for particle in particles:
# 		avg = avg.add(particle.multiply(1.0/len(particles)))
# 	var = 0.0
# 	diffs = []
# 	for i in range (0, len(particles)):
# 		var += particles[i].add(avg.multiply(-1.0)).abs()**2
# 	var = var/len(particles)
# 	ret = phone.Vector(0,0)
# 	num = 0
# 	for particle in particles:
# 		if (particle.add(avg.multiply(-1.0)).abs() < var*0.8):
# 			ret = ret.add(particle)
# 			num += 1
# 	# print num
# 	print "var = " + str(var/avg.abs())
# 	return ret.multiply(((1.0 + math.sqrt(var)/(avg.abs()**1.5))/max(num,1)))



