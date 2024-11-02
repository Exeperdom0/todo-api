from flask import Flask,request,jsonify
import sqlite3
import jwt
import bcrypt
from datetime import datetime,timedelta

app = Flask(__name__)
key = "shave"

def deco(f):
    def wrapper(*args,**kwargs):
        try:
            token=request.headers["Authorization"].split(" ")[1]
            jwt.decode(token,key,algorithms=["HS256"])
        except Exception as e:
            print(str(e))
            return jsonify({"error":"Issue with token"})
        return f()
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
        cursor.execute("COMMIT")
        return jsonify("you have successfully registered!!")
    
    
@app.route("/login", methods=["POST"])
def login():
    email,password = request.json["email"],request.json["password"]
    
    conn = openDb()
    cursor = conn.cursor()
    
    userexists = cursor.execute("SELECT name,email,password FROM users WHERE email = (?)", (email,)).fetchone()
    
    if userexists and bcrypt.checkpw(password.encode('utf-8'),userexists[2]):
        #token
        expiration_time = datetime.utcnow() + timedelta(minutes=20)
        token = jwt.encode({"name":userexists[0],"exp":expiration_time},key)
        return jsonify({"token":f"Bearer {token}"})
    else:
        return jsonify({"error":"Authentication failed"})
    


if __name__ == "__main__":
    app.run(debug=True)