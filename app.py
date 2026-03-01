from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# 1. DEFINE THE APP FIRST (Crucial!)
app = Flask(__name__)

# 2. SETUP DATABASE CONNECTION
try:
    print("STEP B: Trying MySQL connection...")
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Harsha@123",
        database="login_db",
        auth_plugin="mysql_native_password",
        use_pure=True,
        connection_timeout=5
    )
    print(" STEP C: MySQL connected successfully")
except Exception as e:
    print(" MYSQL CONNECTION FAILED")
    print(e)
    exit()

# 3. ROUTES (Login & Home)
@app.route("/")
def home():
    return render_template("login.html") 

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return f"<h1>Welcome {username} Login Successful </h1>"
    else:
        return "<h1>Invalid Credentials </h1><a href='/'>Try again</a>"

# 4. ROUTES (Registration)
@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_user():
    username = request.form.get("username")
    password = request.form.get("password")
    try:
        cursor = db.cursor()
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, password))
        db.commit()
        cursor.close()
        return "<h1>Registration Successful </h1><a href='/'>Go to Login</a>"
    except Exception as e:
        return f"<h1>Error </h1><p>{e}</p>"

# 5. START SERVER
if __name__ == "__main__":
    app.run(debug=True)