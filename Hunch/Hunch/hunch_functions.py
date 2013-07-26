#Hunch Functions 
#AGC 2013

###########################################################
# Work Hourse Functions


def connection(url):
    '''
    connects to api source to extract data
    '''
    import urllib
    import urllib2
    import json
    
    try:
        conn = urllib2.urlopen(url, None)
        try:
            data = json.loads(conn.read())
        finally:
            conn.close()
    except urllib2.HTTPError, error:
        data = json.loads(error.read())
    
    return data

###########################################################
# Yelp API Functions

def yelp_search(search_term):   
    """
    signs a yelp search request using the oauth2 library.
    """
    
    import oauth2
    import base64
    import os

    #pull passwords from heroku enviroment passwords
    consumer_key = os.environ['Consumer_Key']
    consumer_secret = os.environ['Consumer_Secret']
    token = os.environ['Token']
    token_secret = os.environ['Token_Secret']

    #set query vars
    reonomy_loc = '40.749281,-73.994369' # lat long coordinates
    distance = '400'                     # 5 blocks in meters
    
    #set query
    url = ('http://api.yelp.com/v2/search?' \
            'limit=5&' \
            'sort=2&' \
            'term=%s&'\
            'll=%s&'  \
            'radius_filter=%s' \
             %
            (search_term, reonomy_loc, distance))
    
    # use oauth2 to sign request and make query
    consumer = oauth2.Consumer(consumer_key, consumer_secret)
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                          'oauth_timestamp': oauth2.generate_timestamp(),
                          'oauth_token': token,
                          'oauth_consumer_key': consumer_key})
    
    token = oauth2.Token(token, token_secret)
    
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    
    signed_url = oauth_request.to_url()
    
    return signed_url
    
def yelp_business(bid):   
    """
    signs a yelp search request using the oauth2 library.
    """
    
    import oauth2
    import base64
    import os
    
    #pull passwords from heroku enviroment passwords
    consumer_key = os.environ['Consumer_Key']
    consumer_secret = os.environ['Consumer_Secret']
    token = os.environ['Token']
    token_secret = os.environ['Token_Secret']
    
    #set querry
    url = ('http://api.yelp.com/v2/business/%s' % bid)
    
    # use oauth2 to sign request and make query
    consumer = oauth2.Consumer(consumer_key, consumer_secret)
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                          'oauth_timestamp': oauth2.generate_timestamp(),
                          'oauth_token': token,
                          'oauth_consumer_key': consumer_key})
    
    token = oauth2.Token(token, token_secret)
    
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    
    signed_url = oauth_request.to_url()
    
    return signed_url

def dist_convert(dist_meters):
    '''
    takes a distance in meters and returns a distance in NYC Blocks
    '''
    feet_conversion = 3.28
    block_conversion = 264
    return str(((dist_meters * feet_conversion) / block_conversion))[:4] #removes extraneous decimal places

def business_profile(bid):
    '''
    gets information specific to the business
    '''
    return connection(yelp_business(bid))
    

def find_lunch(search_term):
    '''
    queries yelp to get a list of delicious restaurants
    '''
    
    #get search data from data from yelp
    data = connection(yelp_search(search_term))
    
    #extract data
    combiner = []
    queried_restaurants = []
    for i, b in enumerate(data['businesses']):
        
        #clear out combiner
        if i > 0 :
            del combiner
            combiner = []

        #convert distance to blocks
        b['distance'] = dist_convert(b['distance'])

        combiner.append(b) # append search results
        combiner.append(business_profile(b['id'])) # append business profile results
    
        queried_restaurants.append(combiner) # package for later access

    return queried_restaurants

###################################################################
# Weather Underground Functions

def get_weather():
    '''
    gets current weather forecast from weather underground. 
    '''
    import base64   
    import os
    

    # get api password
    weather_key = os.environ['weather_key']
    
    # make query to weather underground and pull the current weather conditions
    url = 'http://api.wunderground.com/api/%s/conditions/q/NY/New_York.json' % (weather_key)
    data = connection(url)['current_observation']
    return data

def good_enough_to_walk(data):
    '''
    Is it a good day for a walk? Let's find out.
    '''
    outside_day = False

    # evaluate the current weather conditions to see if walking is acceptable
    if (45 < data['feelslike_f'] > 85) and data['precip_1hr_in'] == '0.00':
        outside_day = True
    return outside_day

def get_a_hunch():
    '''
    finds a random lunch for you when you cant decide
    '''
    from random import choice
    words = [
             'soup', 'coffee', 'burger',
             'Asian', 'deli', 'bagel',
             'shrimp', 'oyster', 'seafood',
             'salad', 'frozen', 'spanish',
             'cold brew','cronut', 'spicy'
             ]
    return choice(words)