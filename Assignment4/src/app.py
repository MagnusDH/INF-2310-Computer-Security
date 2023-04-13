#TODO
#ADD TLS/SSL to the application
#Launch the application on my server
#Protect the credentials from replay attacks and snooping
#Protect the password file from dictionary attacks
#Optional: show log-in attempts?


from flask import Flask, render_template, redirect, url_for, request, flash, session, make_response
import os.path

#Import sqlite3 to create databse for usernames and passwords
import sqlite3

# Use bcrypt for password handling
import bcrypt

PASSWORDFILE = 'passwords'
PASSWORDFILEDELIMITER = ":"

#Database containing: [id, username, password]
DATABASE = "users"

LOGGED_IN_USER = {"UserName": None, "LoggedIn": False}

FAILED_LOGIN_ATTEMPTS = 0

#Initialize database file if it does not exist
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

#DONE
#Render home-page
@app.route('/')
def home():
    print("\n\nHOME FUNCTION")

    #Check if user is logged in or not
    if(LOGGED_IN_USER["LoggedIn"] == False):
        return render_template('home.html')
    else:
        # return render_template("loggedin.html", username=LOGGED_IN_USER[0])
        return render_template("loggedin.html", username=LOGGED_IN_USER["UserName"])


#DONE
#Display register form
@app.route('/register', methods=['GET'])
def register_get():

    return render_template('register.html')


#DONE
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


#DONE
#Display login form
@app.route('/login', methods=['GET'])
def login_get():
    """Renders the login page"""

    return render_template('login.html')


#NOT DONE, check cookies
#Handle login credentials
@app.route('/login', methods=['POST'])
def login_post():
    """*Renders the loggedIn page with username if:\n
            \t-Entered username exists in database\n
            \t-Entered password matches username\n
        *If loggin is successful, the logged in state is set to 'logged in'"""

    login_attempts = request.cookies.get("login_attempts", 0, type=int)

    #Get request values
    entered_username = request.values["username"]
    entered_password = request.values["password"]

    #Check if user exists in database
    if(user_exists(entered_username) == True):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (entered_username,))
        dbAttributes = cursor.fetchall()

        #Render 'loggedin' if password matches username i database
        if(dbAttributes[0][1] == entered_username and dbAttributes[0][2] == entered_password):
            LOGGED_IN_USER["LoggedIn"] = True
            LOGGED_IN_USER["UserName"] = entered_username

            return redirect(location="/", code=200, Response="OK")

        #Password did not match
        else:         
            if(login_attempts >= 5):
                return render_template("login.html", error="Wrong password entered to many times.\n You can try again in 5 minutes")
            else:
                return render_template("login.html", error=("Invalid password. Number of attempts", login_attempts))
    
    #Username did not exist in database
    else:
        return render_template("login.html", error="Invalid username")


#helper functions

#DONE
#Checks if given username exists in database 
def user_exists(username):
    """Returns True if given username exists in database"""
    
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT (*) FROM users WHERE username=?", (username,))

    if cursor.fetchone()[0] > 0:
        return True
    else:
        return False


@app.route("/setCookie", methods = ["POST"])
def setcookie():
    print("\nSETTING COOKIE!!!!!!!")
    response = make_response("Setting a mafakking coockie")
    response.set_cookie("TITLE", "Maggietits")
    return response

@app.route("/getCookie")
def getCookie(cookie_name: str):
    print("\nGETTING COOKIE: ", cookie_name)

    cookie = request.cookies.get(cookie_name, None)
    return cookie

#Application start point
if __name__ == '__main__':

    # TODO: Add TSL
    app.run(debug=True)