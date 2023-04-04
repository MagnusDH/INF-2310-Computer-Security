from flask import Flask, render_template, redirect, url_for, request, flash, session
import os.path

#Import sqlite3 to create databse for usernames and passwords
import sqlite3

# Use bcrypt for password handling
import bcrypt

PASSWORDFILE = 'passwords'
PASSWORDFILEDELIMITER = ":"

#Database containing: [id, username, password]
DATABASE = "users"

LOGGED_IN = False

#Create database if it does not exist
if not os.path.exists(DATABASE):
    print("\nNO DATABASE, CREATING NEW ONE")
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    
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
    print("LOGGED_IN = ", LOGGED_IN)

    # TODO: Check if user is logged in
    # if user is logged in
    #    return render_template('loggedin.html')

    if(LOGGED_IN == False):
        return render_template('home.html')
    else:
       return render_template('loggedin.html')


#Display register form
@app.route('/register', methods=['GET'])
def register_get():
    print("\n\nREGISTER GET FUNCTION")

    return render_template('register.html')


#Handle registration data
@app.route('/register', methods=['POST'])
def register_post():
    """Registers a user to databse if unique username and correct password length"""

    register_username = request.values["username"]
    register_password = request.values["password"]
    register_matchPassword = request.values["matchpassword"]

    #Check if username already exists
    if(user_exists(register_username) == True):
        return render_template("/register.html", error="Username already exists")
    
    #Check if password is of sufficient length
    if(len(register_password) < 3):
        return render_template("register.html", error="Password must be of at least 3 characters")

    #Check if entered passwords are identical
    if(register_password != register_matchPassword):
        return render_template("register.html", error="Entered passwords are not identical")
    
    #Add user to database
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (register_username, register_password))
    connection.commit()
    connection.close()

    return redirect(location="/", code=200, Response="OK")


#Display login form
@app.route('/login', methods=['GET'])
def login_get():
    """Renders the login page"""

    return render_template('login.html')


#Handle login credentials
@app.route('/login', methods=['POST'])
def login_post():
    """Checks if entered username exists in database and if password matches username"""

    #Get request values
    entered_username = request.values["username"]
    entered_password = request.values["password"]

    #Check if user exists in database
    if(user_exists(entered_username) == True):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (entered_username,))
        dbAttributes = cursor.fetchall()

        #Check if password matches username i database
        if(dbAttributes[0][1] == entered_username and dbAttributes[0][2] == entered_password):
            #SETT USERNAME IN HTML PAGE??????????????????
            LOGGED_IN = True
            return render_template('loggedin.html')

        #Password did not match
        else:
            return render_template("login.html", error="Invalid password")
    
    #Username did not exist in database
    else:
        return render_template("login.html", error="Invalid username")


#helper functions
def user_exists(username):
    """Returns True if given username exists in database"""
    
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT (*) FROM users WHERE username=?", (username,))

    if cursor.fetchone()[0] > 0:
        return True
    else:
        return False


#Application start point
if __name__ == '__main__':
    print("\n########## STARTING APPLICATION ##########")
    print("LOGGED IN = ", LOGGED_IN)

    # TODO: Add TSL
    app.run(debug=True)