from flask import Flask,request,jsonify
import sqlite3

app = Flask(__name__)

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
        conn = openDb()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO users (name,email,password) VALUES (?,?,?)""", (name,email,password,))
        cursor.execute("COMMIT")
        return jsonify("you have successfully registered!!")
    
    
@app.route("/login", methods=["POST"])
def login():
    pass


if __name__ == "__main__":
    app.run(debug=True)