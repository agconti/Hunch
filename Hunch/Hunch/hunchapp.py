# imports
from flask import Flask, request, url_for, render_template
from contextlib import closing
import hunch_functions as hf



# instantiate hunch
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('config/HUNCH_SETTINGS', silent=True)

#Views:
@app.route('/')
def home():
    '''
    standard home template view
    '''
    return render_template('home.html')

@app.route('/results', methods=['POST'])
def search_querry():
    '''
    finds the best lunch based on your search term, renders a search results template
    '''
    if request.method == 'POST':
        # handle an empty search request
        if request.form['search'] == '':
            return render_template('home.html')

        # uses search term to generate a list of restaurants, 
        # and extracts the top rated result
        queried_restaurants = hf.find_lunch(request.form['search'])[0]
        # gets current weather conditions
        weather = hf.get_weather()
        # evaluates current weather conditions to see if its a nice day to go outside
        weather_bool = hf.good_enough_to_walk(weather)
        #renders results template
        return render_template(
                                'show_entries.html', 
                                queried_restaurants=queried_restaurants, 
                                weather=weather, 
                                walking_day=weather_bool,
                                search_val=request.form['search'],
                                i = 0
                                )

@app.route('/results')
def random_search_querry():
    '''
    randomly searches for a lunch for you 
    '''
    # gets a random search term
    random_search_term = hf.get_a_hunch()
    # uses search term to generate a list of restaurants, 
    # and extracts the top rated result
    queried_restaurants = hf.find_lunch(random_search_term)[0]
    # gets current weather conditions
    weather = hf.get_weather()
    # evaluates current weather conditions to see if its a nice day to go outside
    weather_bool = hf.good_enough_to_walk(weather)
    #renders results template
    return render_template(
                            'show_entries.html', 
                            queried_restaurants=queried_restaurants, 
                            weather=weather, 
                            walking_day=weather_bool
                            )

@app.route('/results/more_<past_val>_hunches<ind>', methods=['POST'])
def more_results(past_val, ind):
    
    if request.form["action"] == "Get the next Hunch!":
        
        # increment the index reference
        ind = int(ind)
        ind += 1 

        # gets the the previous list of queried restaurants
        # by using the last search term (past_val)
        queried_restaurants = hf.find_lunch(past_val)
        
        # gets the ith restaurant in that result 
        # i is tracked by the ind (index) variable 
        queried_restaurants = queried_restaurants[ind]

        weather = hf.get_weather()
        weather_bool = hf.good_enough_to_walk(weather)
        # renders template, and passes index and past search term for later use
        return render_template(
                               'show_entries.html', 
                                queried_restaurants=queried_restaurants, 
                                weather=weather, 
                                walking_day=weather_bool,
                                search_val=past_val,
                                i=ind 
                               )
# handles 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('home.html')

if __name__ == '__main__':
        import os  
        port = int(os.environ.get('PORT', 33507)) 
        app.run(host='0.0.0.0', port=port)
        #import passwords
        #passwords.get_secure_info()
        #app.run(debug=True)