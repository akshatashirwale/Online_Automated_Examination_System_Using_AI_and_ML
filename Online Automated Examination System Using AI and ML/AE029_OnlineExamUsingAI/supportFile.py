# Scikit Learn
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import speech_recognition as sr
import pyttsx3
import sqlite3
from datetime import datetime
import cv2
import time
import os 

documents1 = ["narendra modi is the prime minister of india",
"delhi is the capital of india",
"india has total 28 states",
"india got independence on augst 15 1947",
"national language of india is hindi",
"taj mahal is located in agra",
"the official name of india is the republic of india",
"rupee is the currency of india",
"tricolor is the national flag of india",
"jaipur is known as pink city"]

documents2 = ["narendra modi is the prime minister of india",
"delhi is the capital of india",
"india has total 28 states",
"india got independence on augst 15 1947",
"national language of india is hindi",
"taj mahal is located in agra",
"the official name of india is the republic of india",
"rupee is the currency of india",
"tricolor is the national flag of india",
"jaipur is known as pink city"]

documents3 = ["narendra modi is the prime minister of india",
"delhi is the capital of india",
"india has total 28 states",
"india got independence on augst 15 1947",
"national language of india is hindi",
"taj mahal is located in agra",
"the official name of india is the republic of india",
"rupee is the currency of india",
"tricolor is the national flag of india",
"jaipur is known as pink city"]

documents4 = ["narendra modi is the prime minister of india",
"delhi is the capital of india",
"india has total 28 states",
"india got independence on augst 15 1947",
"national language of india is hindi",
"taj mahal is located in agra",
"the official name of india is the republic of india",
"rupee is the currency of india",
"tricolor is the national flag of india",
"jaipur is known as pink city"]

documents5 = ["narendra modi is the prime minister of india",
"delhi is the capital of india",
"india has total 28 states",
"india got independence on augst 15 1947",
"national language of india is hindi",
"taj mahal is located in agra",
"the official name of india is the republic of india",
"rupee is the currency of india",
"tricolor is the national flag of india",
"jaipur is known as pink city"]

print(documents1[0])

# Create the Document Term Matrix
count_vectorizer = CountVectorizer(stop_words='english')
count_vectorizer = CountVectorizer()
sparse_matrix = count_vectorizer.fit_transform(documents1)


# OPTIONAL: Convert Sparse Matrix to Pandas Dataframe if you want to see the word frequencies.
doc_term_matrix = sparse_matrix.todense()
df = pd.DataFrame(doc_term_matrix, 
                  columns=count_vectorizer.get_feature_names(), 
                  )


# Compute Cosine Similarity
from sklearn.metrics.pairwise import cosine_similarity
print(cosine_similarity(df, df))

s1 = count_vectorizer.transform([documents1[0]])
s2 = count_vectorizer.transform([documents1[0]])
print(cosine_similarity(s1,s1))


# Initialize the recognizer
r = sr.Recognizer()

# Function to convert text to
# speech
def SpeakText(command):
	
	# Initialize the engine
	engine = pyttsx3.init()
	engine.say(command)
	engine.runAndWait()
	

def speech_text():	
	
	# Exception handling to handle
	# exceptions at the runtime
	try:
		
		# use the microphone as source for input.
		with sr.Microphone() as source2:
			
			# wait for a second to let the recognizer
			# adjust the energy threshold based on
			# the surrounding noise level
			r.adjust_for_ambient_noise(source2, duration=0.2)
			
			#listens for the user's input
			audio2 = r.listen(source2)
			
			# Using ggogle to recognize audio
			MyText = r.recognize_google(audio2)
			MyText = MyText.lower()

			
			return(MyText)
			
	except sr.RequestError as e:
		return("Could not request results; {0}".format(e))
		
	except sr.UnknownValueError:
		return("unknown error occured")


def get_frame():
	camera_port=0
	camera=cv2.VideoCapture(camera_port) #this makes a web cam object
	time.sleep(2)

	while True:
		ret, img = camera.read()
		cv2.imwrite(os.path.join("static/images/","test_image.jpg"),img)
		faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(
			gray,

			scaleFactor=1.2,
			minNeighbors=5
			,     
			minSize=(20, 20)
		)
		for (x, y, w, h) in faces:
			cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

		if(len(faces)==0):
			cv2.putText(img, 'No Face Found...!!!', (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255))
		elif(len(faces)>1):
			cv2.putText(img, 'Multiple Faces Found...!!!', (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255))
		imgencode=cv2.imencode('.jpg',img)[1]
		stringData=imgencode.tostring()
		yield (b'--frame\r\n'
			b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

	del(camera)


def detectFace():
	frame = cv2.imread('static/images/test_image.jpg')
	faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(
		gray,

		scaleFactor=1.2,
		minNeighbors=5
		,     
		minSize=(20, 20)
	)

	return(len(faces))



