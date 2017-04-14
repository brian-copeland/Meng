import pygtk
pygtk.require('2.0')
import gtk
import random
import environment
from phone import Vector
import particleFilter

class GUI:


 	def __init__(self):

 		self.hRange = [-20, 20]
		self.vRange = [-20, 20]
		self.height = self.vRange[1] - self.vRange[0]
		self.width = self.hRange[1] - self.hRange[0]
		self.xPixels = 600
		self.yPixels = 600
		self.dotSize = 18
		self.pointSize = 4

		e = gtk.Entry()
		self.map = e.get_colormap()
		white = self.map.alloc_color("white")

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.box1 = gtk.VBox(False, 0)
		self.box0 = gtk.HBox(False, 0)
		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)

		self.quit_button = gtk.Button("Exit")
		self.quit_button.connect_object("clicked", gtk.Widget.destroy, self.window)
		self.step_button = gtk.Button("Step")
		self.step_button.connect("clicked", self.step)
		self.box0.pack_start(self.step_button, True, True, 0)
		self.box0.pack_start(self.quit_button, True, True, 0)
		self.box1.pack_start(self.box0, True, True, 0)

		self.drawing_area = gtk.DrawingArea()
		self.drawing_area.set_size_request(self.xPixels, self.yPixels)
		self.box1.pack_start(self.drawing_area, True, True, 0)

		self.window.add(self.box1)
		self.window.show_all()

		self.drawable = self.drawing_area.window
		self.drawing_area.modify_bg(gtk.STATE_NORMAL, white)

		self.current_circles = []
		self.current_unfilled_circles = []
		self.current_point = []

		self.world = environment.World(True)

		

	def getPixelsFromPosition(self, x, y):
		xFrac = (x - self.hRange[0])/(1.0*self.width)
		xPixel = int(xFrac*self.xPixels)
		yFrac = -1*(y - self.vRange[1])/(1.0*self.height)
		yPixel = int(yFrac*self.yPixels)
		return (xPixel, yPixel)


	def main(self):
		gtk.main()

	def destroy(self, widget, data=None):
		gtk.main_quit()

	def delete_event(self, widget, event, data=None):
		return False


	def comparePoints(self, points1, points2, numSamples):
		loc = Vector(0, 0)
		# print locat
		newPoints = []
		for i in range(0, numSamples):
			point1 = points1[random.randint(0, len(points1)-1)][0]
			point2 = points2[random.randint(0, len(points2)-1)][0]
			tmp = point1.add(point2.multiply(-1.0))
			newPoints.append(loc.add(tmp))
		# loc = particleFilter.getRefinedAverageVec(newPoints)
		# loc = loc.multiply(1.0/numSamples)
		return newPoints


	##Everything after here is stuff I think I need to do the computation
	def step(self, data=None):
		print "New Step\n"
		self.erase_circle()
		self.erase_points()
		stepData = self.world.step(True)
		self.erase_circle()
		self.erase_unfilled_circle()
		for j in range(0, len(self.world.phoneList)):
			newGuess = Vector(0,0)
			points = []
			# print newGuess
			for i in range(0, len(self.world.routerList)):
				newGuess = newGuess.add(stepData[j][i][0].add(stepData[(j-1)%2][i][0].multiply(-1)))
				points = points + self.comparePoints(stepData[j][i][1], stepData[(j-1)%2][i][1], 1000)
				
			# newGuess = newGuess.multiply(1.0/len(self.world.routerList))
			newGuess = particleFilter.getRefinedAverageVec(points)
			# if j == 1:
				# self.stepMultiParticle(points, self.world.phoneList[j])

			phone1Location = self.world.phoneList[j].getLocation()
			for i in range(0, len(self.world.routerList)):
				# modifiedNewGuess = newGuess.multiply(len(self.world.routerList)).add(stepData[(j-1)%2][i][0].multiply(
					# -1.0)).multiply(1.0/(len(self.world.routerList)-1))
				self.world.phoneSoftwareList[j].otherGuess[i] = newGuess.add(stepData[(j-1)%2][i][0])
				# self.draw_unfilled_circle("yellow", phone1Location.x + self.world.phoneSoftwareList[j].otherGuess[i].xDiff, 
					# phone1Location.y + 	self.world.phoneSoftwareList[j].otherGuess[i].yDiff)

			self.draw_unfilled_circle("purple", phone1Location.x + newGuess.xDiff, phone1Location.y + newGuess.yDiff)

		for i in [0, 1]:

			myPhone = self.world.phoneList[i]
			phoneLocation = myPhone.getLocation()
			data = stepData[i]
			for router in data:

				(output, points) = router

				x = phoneLocation.x + output.xDiff
				y = phoneLocation.y + output.yDiff
				print x
				print y
				# x1 = phone1.x + output[1].xDiff
				# y1 = phone1.y + output[1].yDiff
				self.stepMultiParticle([point[0] for point in points], myPhone)
				if (i == 0):
					self.draw_unfilled_circle("blue", x, y)
				else:
					self.draw_unfilled_circle("red", x, y)
		# self.draw_unfilled_circle("yellow", x1, y1)
		self.draw_circle("blue", self.world.phone1.getLocation().x, self.world.phone1.getLocation().y)
		self.draw_circle("red", self.world.phone2.getLocation().x, self.world.phone2.getLocation().y)
		for router in self.world.routerList:

			self.draw_circle("green", router.getLocation().x, router.getLocation().y)
			# self.draw_circle("green", self.world.router2.getLocation().x, self.world.router2.getLocation().y)
		

	def stepMultiParticle(self, points, phoneIn, data=None):

		output = points
		# self.erase_circle()
		# self.erase_points()

		self.draw_circle("blue", self.world.phone1.getLocation().x, self.world.phone1.getLocation().y)
		self.draw_circle("red", self.world.phone2.getLocation().x, self.world.phone2.getLocation().y)

		phone1 = phoneIn.getLocation()
		for point in output:
			x = phone1.x + point.xDiff
			y = phone1.y + point.yDiff
		# x1 = phone1.x + output[1].xDiff
		# y1 = phone1.y + output[1].yDiff
			self.draw_point("black", x, y)
		# self.draw_unfilled_circle("yellow", x1, y1)
			
	def draw_point(self, color, x, y):
		self.current_point.append((x,y))
		new_gc = gtk.gdk.Drawable.new_gc(self.drawable)
		colour = self.map.alloc_color(color)

		new_gc.set_foreground(colour)

		(newx, newy) = self.getPixelsFromPosition(x, y)
		upperx = newx - self.dotSize/2
		uppery = newy - self.dotSize/2
		self.drawable.draw_arc(new_gc, True, upperx, uppery, self.pointSize, self.pointSize, 0, 360*64)

	def erase_points(self):
		for vec in self.current_point:
			colour = self.map.alloc_color("white")
			new_gc = gtk.gdk.Drawable.new_gc(self.drawable)
			new_gc.set_foreground(colour)

			(newx, newy) = self.getPixelsFromPosition(vec[0], vec[1])
			upperx = newx - self.dotSize/2
			uppery = newy - self.dotSize/2
			self.drawable.draw_arc(new_gc, True, upperx, uppery, self.pointSize, self.pointSize, 0, 360*64)
		self.current_point = []

	def draw_circle(self, color, x, y):
		self.current_circles.append((x,y))
		new_gc = gtk.gdk.Drawable.new_gc(self.drawable)
		colour = self.map.alloc_color(color)

		new_gc.set_foreground(colour)

		(newx, newy) = self.getPixelsFromPosition(x, y)
		upperx = newx - self.dotSize/2
		uppery = newy - self.dotSize/2
		self.drawable.draw_arc(new_gc, True, upperx, uppery, self.dotSize, self.dotSize, 0, 360*64)



	def draw_unfilled_circle(self, color, x, y):
		self.current_unfilled_circles.append((x,y))
		new_gc = gtk.gdk.Drawable.new_gc(self.drawable)
		colour = self.map.alloc_color(color)

		new_gc.set_foreground(colour)
		new_gc.line_width = 2

		(newx, newy) = self.getPixelsFromPosition(x, y)
		upperx = newx - (self.dotSize+10)/2
		uppery = newy - (self.dotSize+10)/2
		self.drawable.draw_arc(new_gc, False, upperx, uppery, self.dotSize+10, self.dotSize+10, 0, 360*64)

	def erase_circle(self):
		for (x,y) in self.current_circles:
			new_gc = gtk.gdk.Drawable.new_gc(self.drawable)

			colour = self.map.alloc_color("white")
			new_gc.set_foreground(colour)

			(newx, newy) = self.getPixelsFromPosition(x, y)
			upperx = newx - self.dotSize/2
			uppery = newy - self.dotSize/2
			self.drawable.draw_arc(new_gc, True, upperx, uppery, self.dotSize, self.dotSize, 0, 360*64)
		self.current_circles = []

	def erase_unfilled_circle(self):
		for (x,y) in self.current_unfilled_circles:
			new_gc = gtk.gdk.Drawable.new_gc(self.drawable)

			colour = self.map.alloc_color("white")
			new_gc.set_foreground(colour)

			(newx, newy) = self.getPixelsFromPosition(x, y)
			upperx = newx - (self.dotSize+15)/2
			uppery = newy - (self.dotSize+15)/2
			self.drawable.draw_arc(new_gc, True, upperx, uppery, self.dotSize+15, self.dotSize+15, 0, 360*64)
		self.current_unfilled_circles = []



print __name__
if __name__ == "__main__":
	base = GUI()
	base.main()