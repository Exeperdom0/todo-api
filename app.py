from flask import Flask,request,jsonify
import sqlite3
import jwt
import bcrypt
from datetime import datetime,timedelta

app = Flask(__name__)
secret = "key"

def deco(f):
    def wrapper(*args,**kwargs):
        try:
            token=request.headers["Authorization"].split(" ")[1]
            jwt.decode(token,secret,algorithms=["HS256"])
        except Exception as e:
            print(str(e))
            return jsonify({"error":"Issue with token"})
        return f(*args,**kwargs)
    return wrapper

def openDb():
    with sqlite3.connect("todo eipiai/tododb") as conn:
        return conn

@app.route("/register", methods=["POST"])
def register():
    name,email,password = request.json["name"], request.json["email"], request.json["password"]
    
    conn = openDb()
    cursor = conn.cursor()
    
    userexists = cursor.execute("SELECT * FROM users WHERE name = (?) or email = (?)", (name,email,)).fetchone()
    conn.close()
    
    if userexists:
        return jsonify("User or email already in use")
    else:
        password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        conn = openDb()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO users (name,email,password) VALUES (?,?,?)""", (name,email,password,))
        conn.commit()
        return jsonify("you have successfully registered!!")
    
    
@app.route("/login", methods=["POST"])
def login():
    email,password = request.json["email"],request.json["password"]
    
    conn = openDb()
    cursor = conn.cursor()
    
    userexists = cursor.execute("SELECT name,email,password FROM users WHERE email = (?)", (email,)).fetchone()
    
    if userexists and bcrypt.checkpw(password.encode('utf-8'),userexists[2]):
        
        #token
        expiration_time = datetime.utcnow() + timedelta(minutes=10)
        token = jwt.encode({"name":userexists[0],"exp":expiration_time},"key")
        return jsonify({"token":f"Bearer {token}"})
    
    else:
        return jsonify({"error":"Authentication failed"})
    
@app.route("/todos", methods=["POST"], endpoint="posttask")
@deco
def make_todo():
    
    token = request.headers["Authorization"].split(" ")[1]
    name = jwt.decode(token,"key",algorithms=["HS256"])["name"]
    
    title,description = request.json["title"],request.json["description"]
    
    conn = openDb()
    cursor = conn.cursor()
    
    titleexists = cursor.execute("SELECT title FROM tasks WHERE user = (?) and title = (?)", (name,title,)).fetchone()
    
    if titleexists:
        return jsonify({"error":"A task with that title already exists"})
    else:
        cursor.execute("INSERT INTO tasks (user,title,description) VALUES (?,?,?)", (name,title,description))
        conn.commit()
        taskid = cursor.execute("SELECT id FROM tasks WHERE user = (?) and title = (?)", (name,title,)).fetchone()
        return jsonify({"id":taskid[0],"title":title,"description":description})
    
@app.route("/todos/<int:todo_id>", methods=["PUT","DELETE"], endpoint="updateordeletetask")
@deco
def updateTask(todo_id):
    token = request.headers["Authorization"].split(" ")[1]
    name = jwt.decode(token,secret,algorithms=["HS256"])["name"]
    
    conn = openDb()
    cursor = conn.cursor()
    
    if request.method == "PUT":
        title,description = request.json["title"],request.json["description"]
        
        taskexists = cursor.execute("SELECT title FROM tasks WHERE user = (?) AND id = (?)", (name,todo_id,)).fetchone()
        
        if taskexists:
            cursor.execute("UPDATE tasks SET title = (?), description = (?) WHERE user = (?) and id = (?)", (title,description,name,todo_id))
            conn.commit()
            return jsonify({"id":todo_id,"title":title,"description":description})
        else:
            return jsonify("Forbidden")
    elif request.method == "DELETE":
        taskexists = cursor.execute("SELECT user FROM tasks WHERE user = (?) AND id = (?)", (name,todo_id,)).fetchone()
        
        if taskexists:
            cursor.execute("DELETE FROM tasks WHERE user = (?) and id = (?) ", (name,todo_id,))
            conn.commit()
            return jsonify({"status_code":204})
        else:
            return jsonify({"error":"A task with that id does not exists"})
    
@app.route("/todos/<int:page>/<int:limit>", methods=["GET"])
@deco
def watchtasks(page,limit):
    token = request.headers["Authorization"].split(" ")[1]
    name = jwt.decode(token,secret,algorithms=["HS256"])["name"]
    
    conn = openDb()
    cursor = conn.cursor()
    
    tasks = cursor.execute(f"SELECT id,title,description FROM tasks WHERE user = ? LIMIT ? OFFSET ?", (name,limit,(page-1)*limit)).fetchall()
    for i,v in enumerate(tasks):
        tasks[i] = {"id":v[0],"title":v[1],"description":v[2]}
    return jsonify({"data":[i for i in tasks],"page":page,"limit":limit,"total":len(tasks)})
        
if __name__ == "__main__":
    app.run(debug=True)