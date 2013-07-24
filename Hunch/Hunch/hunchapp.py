# imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import hunch_functions as hf

# config
DEBUG = True

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('config/HUNCH_SETTINGS', silent=True)

#Views:
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add', methods=['POST'])
def search_querry():
    #first test return single business rendered
    if request.method == 'POST':
        queried_resturants = hf.find_lunch(request.form['search'])
    return render_template('show_entries.html', queried_resturants=queried_resturants)

#views for and handling : login / logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None) # dont have to check for usr to 
    flash('You were logged out')   #    be loggedin...sweet!
    return redirect(url_for('home'))

if __name__ == '__main__':
    import os  
    port = int(os.environ.get('PORT', 33507)) 
    app.run(host='0.0.0.0', port=port)
    