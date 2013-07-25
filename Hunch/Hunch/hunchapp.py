# imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import hunch_functions as hf

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('config/HUNCH_SETTINGS', silent=True)

#Views:
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/results', methods=['POST'])
def search_querry():
    '''
    finds the best lunch based on your search term
    '''
    if request.method == 'POST':
        queried_resturants = hf.find_lunch(request.form['search'])
        weather = hf.get_weather()
        weather_bool = hf.good_enough_to_walk(weather)
    return render_template(
                            'show_entries.html', 
                            queried_resturants=queried_resturants, 
                            weather=weather, 
                            walking_day=weather_bool
                            )

@app.route('/results')
def random_search_querry():
    '''
    randomly searches for a lunch for you 
    '''
    queried_resturants = hf.find_lunch(hf.get_a_hunch())
    weather = hf.get_weather()
    weather_bool = hf.good_enough_to_walk(weather)
    return render_template(
                            'show_entries.html', 
                            queried_resturants=queried_resturants, 
                            weather=weather, 
                            walking_day=weather_bool
                            )


if __name__ == '__main__':
        import os  
        import passwords
        #port = int(os.environ.get('PORT', 33507)) 
        #app.run(host='0.0.0.0', port=port)
        #passwords.get_secure_info()
        app.run(debug=True)