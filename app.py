from flask import Flask,render_template,request,url_for,redirect
import pymysql
import warnings
import numpy as np
import pickle
warnings.filterwarnings("ignore")

# SQL
def verify(username,password):
    # Connection
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='Mysqlpassword', db='mlt')
    cur = conn.cursor()
    
    cur.execute(f'SELECT password from user_db where username = "{username}";')
    data = cur.fetchall()

    if(len(data) == 1 and data[0][0] == password):
        return True
    else:
        return False

def create(username,email,password):
    # Connection
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='Mysqlpassword', db='mlt')
    cur = conn.cursor()

    cur.execute(f'SELECT * from user_db where username = "{username}";')
    data = cur.fetchall()
    print(data)
    if(len(data) == 0):
        cur.execute(f'Insert into user_db values("{username}","{email}","{password}")')
        conn.commit()
        return True
    else:
        return False

# Flask
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html',message="")

@app.route('/signin',methods=["POST"])
def signin():
    name = request.form["username"]
    password = request.form["password"]
    if(verify(name,password)):
        return redirect(url_for('predict'))
    else:
        return render_template('login.html',message="Invalid login credentials !!!")

@app.route('/signup',methods=["POST"])
def signup():
    name = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    if(create(name,email,password)):
        return render_template('login.html',message="Your account has been created successfully you can now sign in !!!")
    else:
        return render_template('login.html',message="Username already exists !!!")

@app.route('/predict',methods=["POST","GET"])
def predict():
    model=pickle.load(open('model.pkl', 'rb'))
    if request.method == "POST":
        input1 = float(request.form["sepallength"])
        input2 = float(request.form["sepalwidth"])
        input3 = float(request.form["petallength"])
        input4 = float(request.form["petalwidth"])
        arr = np.array([input1,input2,input3,input4])
        out=model.predict(arr)
        return render_template('predict.html',output=out)
    else:
        return render_template('predict.html',output="")

if __name__ == '__main__':
    app.run(debug = True)

