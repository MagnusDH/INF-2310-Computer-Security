from flask import Flask, render_template, redirect, url_for, request, flash, session
import os.path

#Import sqlite3 to create databse for usernames and passwords
import sqlite3

# Use bcrypt for password handling
import bcrypt

PASSWORDFILE = 'passwords'
PASSWORDFILEDELIMITER = ":"

DATABASE = "USERS"

#Create database if it does not exist
if not os.path.exists(DATABASE):
    print("\n\nNO DATABASE, CREATING NEW ONE")
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE USERS (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    
    #Commit the changes and close
    connection.commit()
    connection.close()

app = Flask(__name__)
# The secret key here is required to maintain sessions in flask
app.secret_key = b'8852475abf1dcc3c2769f54d0ad64a8b7d9c3a8aa8f35ac4eb7454473a5e454c'

# Initialize Database file if not exists.
if not os.path.exists(PASSWORDFILE):
    open(PASSWORDFILE, 'w').close()


@app.route('/')
def home():
    print("\n\nHOME FUNCTION")

    # TODO: Check if user is logged in
    # if user is logged in
    #    return render_template('loggedin.html')

    return render_template('home.html')


#Display register form
@app.route('/register', methods=['GET'])
def register_get():
    print("\n\nREGISTER GET FUNCTION")

    return render_template('register.html')


#Handle registration data
@app.route('/register', methods=['POST'])
def register_post():
    print("\n\nREGISTER POST FUNCTION")

    register_username = request.values["username"]
    register_password = request.values["password"]
    register_matchPassword = request.values["matchpassword"]
    
    print("\nUsername: ", register_username)
    print("Password: ", register_password)
    print("Match password: ", register_matchPassword)


    #Check if username already exists
    if(user_exists(register_username) == True):
        render_template("/register.html", error="Username already exists")
    
    #Check if password is of sufficient length
    if(len(register_password) < 3):
        return render_template("register.html", error="Password must be of at least 3 characters")

    #Check if entered passwords are identical
    if(register_password != register_matchPassword):
        return render_template("register.html", error="Entered passwords are not identical")
    
    #Add user to database
    print("Add user to database...")
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO USERS (username, password) VALUES (?, ?)", (register_username, register_password))
    connection.commit()
    connection.close()
    # file = open("passwords", "w")
    # file.write(register_username+"\n")
    # file.write(register_password)
    # file.close()

    return redirect(location="/", code=200, Response="OK")
    #Open password file
    #Write credentials to password file
    # raise NotImplemented


#Display login form
@app.route('/login', methods=['GET'])
def login_get():
    print("\n\nLOG IN GET FUNCTION")

    return render_template('login.html')


#Handle login credentials
@app.route('/login', methods=['POST'])
def login_post():
    print("\n\nLOG IN POST FUNCTION")

    raise NotImplemented





#helper functions
def user_exists(username):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM USERS WHERE username=?", (username,))

    if cursor.fetchone()[0] > 0:
        return True
    else:
        return False


#Application start point
if __name__ == '__main__':
    print("\n\n\n\n########## STARTING APPLICATION ##########")

    # TODO: Add TSL
    app.run(debug=True)