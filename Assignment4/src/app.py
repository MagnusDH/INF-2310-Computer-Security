from flask import Flask, render_template, redirect, url_for, request, flash, session
import os.path

# Use bcrypt for password handling
import bcrypt

PASSWORDFILE = 'passwords'
PASSWORDFILEDELIMITER = ":"

app = Flask(__name__)
# The secret key here is required to maintain sessions in flask
app.secret_key = b'8852475abf1dcc3c2769f54d0ad64a8b7d9c3a8aa8f35ac4eb7454473a5e454c'

# Initialize Database file if not exists.
if not os.path.exists(PASSWORDFILE):
    open(PASSWORDFILE, 'w').close()


@app.route('/')
def home():

    # TODO: Check if user is logged in
    # if user is logged in
    #    return render_template('loggedin.html')

    return render_template('home.html')


# Display register form
@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')

# Handle registration data
@app.route('/register', methods=['POST'])
def register_post():
    raise NotImplemented

# Display login form
@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')


# Handle login credentials
@app.route('/login', methods=['POST'])
def login_post():
    raise NotImplemented


if __name__ == '__main__':

    # TODO: Add TSL
    app.run(debug=True)
