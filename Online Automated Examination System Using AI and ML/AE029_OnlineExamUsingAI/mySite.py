# import the necessary packages
from flask import Flask, render_template, redirect, url_for, request , session , Response , flash
from werkzeug.utils import secure_filename
from supportFile import *
import os

questions1 = ["Who is the prime minister of India?",
"Which is the capital of India?",
"How many states india has?",
"When India got Independence?",
"Which is the national language of India?",
"Where is the taj mahal located?",
"What is the official name of India?",
"Which is the currency of India?",
"Which is the flag of India?",
"Which city is known as pink city?"
]

questions2 = ["Who is the prime minister of India?",
"Which is the capital of India?",
"How many states india has?",
"When India got Independence?",
"Which is the national language of India?",
"Where is the taj mahal located?",
"What is the official name of India?",
"Which is the currency of India?",
"Which is the flag of India?",
"Which city is known as pink city?"
]

questions3 = ["Who is the prime minister of India?",
"Which is the capital of India?",
"How many states india has?",
"When India got Independence?",
"Which is the national language of India?",
"Where is the taj mahal located?",
"What is the official name of India?",
"Which is the currency of India?",
"Which is the flag of India?",
"Which city is known as pink city?"
]

questions4 = ["Who is the prime minister of India?",
"Which is the capital of India?",
"How many states india has?",
"When India got Independence?",
"Which is the national language of India?",
"Where is the taj mahal located?",
"What is the official name of India?",
"Which is the currency of India?",
"Which is the flag of India?",
"Which city is known as pink city?"
]

questions5 = ["Who is the prime minister of India?",
"Which is the capital of India?",
"How many states india has?",
"When India got Independence?",
"Which is the national language of India?",
"Where is the taj mahal located?",
"What is the official name of India?",
"Which is the currency of India?",
"Which is the flag of India?",
"Which city is known as pink city?"
]

questions = []

idx = 0
login_status=0
name=''
password=''
que_set=''

app = Flask(__name__)

app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			num = request.form['num']
			
			users = {'Name':request.form['name'],'Email':request.form['email'],'Contact':request.form['num']}
			df = pd.DataFrame(users,index=[0])
			df.to_csv('users.csv',mode='a',header=False)

			sec = {'num':num}
			df = pd.DataFrame(sec,index=[0])
			df.to_csv('secrets.csv')

			name = request.form['name']
			num = request.form['num']
			email = request.form['email']
			password = request.form['password']
			age = request.form['age']
			gender = request.form['gender']

			con = sqlite3.connect('mydatabase.db')
			cursorObj = con.cursor()
			cursorObj.execute(f"SELECT Name from Users WHERE Name='{name}' AND password = '{password}';")
		
			if(cursorObj.fetchone()):
				error = "<span style='color:red;'> User has been already register..!!!</span>"
			else:
				now = datetime.now()
				dt_string = now.strftime("%d/%m/%Y %H:%M:%S")			
				con = sqlite3.connect('mydatabase.db')
				cursorObj = con.cursor()
				cursorObj.execute("CREATE TABLE IF NOT EXISTS Users (Date text,Name text,Contact text,Email text,password text,age text,gender text)")
				cursorObj.execute("INSERT INTO Users VALUES(?,?,?,?,?,?,?)",(dt_string,name,num,email,password,age,gender))
				con.commit()

				return redirect(url_for('prelogin'))

	return render_template('register.html',error=error)


@app.route('/prelogin', methods=['GET', 'POST'])
def prelogin():
	error = None
	global name
	global password
	global que_set
	global login_status
	if request.method == 'POST':
		name = request.form['name']
		password = request.form['password']
		que_set = int(request.form['que_set'])
		return redirect(url_for('login'))
	return render_template('prelogin.html',error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	global name
	global password
	global login_status
	global que_set
	if request.method == 'POST':
		faces = detectFace()
		print(faces)
		if(faces>0):
			name = request.form['name']
			password = request.form['password']
			que_set = int(request.form['que_set'])
			con = sqlite3.connect('mydatabase.db')
			cursorObj = con.cursor()
			cursorObj.execute(f"SELECT Name from Users WHERE Name='{name}' AND password = '{password}';")

			if(cursorObj.fetchone()):
				con = sqlite3.connect('mydatabase.db')
				cursorObj = con.cursor()
				cursorObj.execute('DROP table IF EXISTS EResult;')
				con.commit()
				login_status = 1
				return redirect(url_for('input'))
			else:
				error = "<span style='color:red;'>Invalid Credentials Please try again..!!!</span>"
		else:
			return redirect(url_for('prelogin'))
	return render_template('login.html',error=error,name=name,password=password)

@app.route('/input', methods=['GET', 'POST'])
def input():
	global idx
	global que_set
	print(que_set)
	if(que_set == 1):
		questions = questions1
		documents = documents1
	elif(que_set==2):
		questions = questions2
		documents = documents2
	elif(que_set==3):
		questions = questions3
		documents = documents3
	elif(que_set==4):
		questions = questions4
		documents = documents4
	elif(que_set==5):
		questions = questions5
		documents = documents5
	question = questions[idx]
	if request.method == 'POST':
		if request.form['submitbutton']=='Answer':
			SpeakText(question)
			text = speech_text()
			print(text)
			ans1 = count_vectorizer.transform([documents[idx]])
			ans2 = count_vectorizer.transform([text])
			score = cosine_similarity(ans1,ans2)
			if(score>=0.8):
				score1 = "Correct"
			else:
				score1 = "Wrong" 
			
			print(score[0][0])
			print("Question:",question)
			print("Answer:",text)
			print("Actual:",documents[idx])
			con = sqlite3.connect('mydatabase.db')
			cursorObj = con.cursor()
			cursorObj.execute("CREATE TABLE IF NOT EXISTS EResult (Question text,Your_Ans text,Correct_Ans text, Score text)")
			cursorObj.execute("INSERT INTO EResult VALUES(?,?,?,?)",(question,text,documents[idx],score1))
			con.commit()
			return render_template('input.html',text=text,result=score[0][0]*100,question=question)


		if request.form['submitbutton']=='Next':			
			idx = idx+1
			if(idx == len(questions)):
				return redirect(url_for('result'))
			else:
				return render_template('input.html',question=questions[idx])
			
	return render_template('input.html',question=question)

@app.route('/result', methods=['GET', 'POST'])
def result():
	global name
	global idx
	idx = 0
	conn = sqlite3.connect('mydatabase.db', isolation_level=None,
						detect_types=sqlite3.PARSE_COLNAMES)
	db_df = pd.read_sql_query(f"SELECT * from EResult", conn)
	
	return render_template('result.html',tables=[db_df.to_html(classes='w3-table-all w3-hoverable w3-padding')], titles=db_df.columns.values)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('login')

@app.route('/video_stream')
def video_stream():

	return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.after_request
def add_header(response):
	
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response





if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, threaded=True)
