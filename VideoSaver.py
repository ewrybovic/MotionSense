from collections import deque

# Holds two buffers to save videos from
class VideoDeque:
	def __init__(self, frameRate, seconds):
		# Create a deque to get the last couple seconds of footage
		self.prevFrames = deque([], frameRate * seconds)

		# A deque for new footage, just so we don't miss anything when writing video to file
		self.newFrames = deque([])

	# Adds a new frame to the right of the deque
	def addPrevFrame(self, frame):
		if self.prevFrames is not None:
			self.prevFrames.append(frame)

	# Adds a new frame to the newFrames deque
	def addNewFrame(self, frame):
		if self.newFrames is not None:
			self.newFrames.append(frame)

	# Clears both deques for new footage
	def clear(self):
		self.newFrames.clear()
		self.prevFrames.clear()

