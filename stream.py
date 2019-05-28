import cv2
import time
import numpy as np
import time
from VideoSaver import VideoDeque

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480);
#cap.set(cv2.CAP_PROP_FPS,24) This does not work

# helper variables for detecting motion
dKernal = np.ones((5, 5), np.uint8)
minContourArea = 15000

# Misc variables
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (255,255,255)
lineType = 2
DEBUG = False
numSeconds = 5
detectedMotion = False
compareTime = None
initialTime = None

# Master image that the new image will compare to
master = None

# Vars to write and save videos
vidDeque = VideoDeque(30, 3)


while True:
	grabbed,oframe = cap.read()
	if not grabbed:
		break

	# Check if motion was detected on the previous frame
	if detectedMotion:
		compareTime = time.time()

		# loop while it has been less than the number of seconds
		if compareTime - initialTime < numSeconds:
			vidDeque.addNewFrame(oframe)
		else:
			print("Saving to file")
			# Once loop breaks save the old and new frames
			for pframe in vidDeque.prevFrames:
				vidWriter.write(pframe)
			for nframe in vidDeque.newFrames:
				vidWriter.write(nframe)
			vidWriter.release()

			# Clear both buffers
			vidDeque.clear()

			# Turn off detected motion
			detectedMotion = False

			# Set the master again as to not trip the motion detection
			master = cv2.GaussianBlur(cv2.cvtColor(oframe, cv2.COLOR_BGR2GRAY), (21,21),0)
			
			# If the software is to stop after the video then break
			#break

	# If no motion was detected look for some
	else:
		# Convert to greyscale
		frame = cv2.cvtColor(oframe, cv2.COLOR_BGR2GRAY)

		# blur the frame to reduce noise
		frame = cv2.GaussianBlur(frame, (21,21),0)

		# Check if master has been assigned
		if master is None:
			master = frame
			continue

		# Get the delta from the master and frame
		delta = cv2.absdiff(master, frame)

		# Get a Threshold frame
		_,threshold = cv2.threshold(delta, 12, 255, cv2.THRESH_BINARY)

		# Dilate the threshold image to fill in holes
		dilateFrame = cv2.dilate(threshold, dKernal, iterations=4)

		# find contours inside the dilated frame
		_,contours,_ = cv2.findContours(dilateFrame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		for c in contours:
			# If there is a large enough movement
			if cv2.contourArea(c) > minContourArea:
				detectedMotion = True
				vidWriter = cv2.VideoWriter(str(time.time())+".avi", cv2.VideoWriter_fourcc(*'XVID'), 30.0, (640,480))
				initialTime = time.time()
				print("Motion detected, getting extra footage")
				break
		
		vidDeque.addPrevFrame(oframe)
		if DEBUG:
			cv2.imshow("Delta", delta)
			cv2.imshow("Thresh", threshold)
			cv2.imshow("Dilate", dilateFrame)

		master = frame
	# Show the stream
	cv2.imshow("Stream", oframe)
	if cv2.waitKey(1) == 27:
		break

cap.release()
cv2.destroyAllWindows()
