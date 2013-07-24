#Hunch Functions 
#AGC 2013

def yelp_search(search_term):   
    """
    signs a yelp search request using the oauth2 library.
    """
    
    import oauth2
    import base64
    import passwords
    
    #get passwords
    my_info = passwords.get_secure_info()
    #'decrypt passwords'
    consumer_key = base64.b64decode(my_info['Consumer_Key'])
    consumer_secret = base64.b64decode(my_info['Consumer_Secret'])
    token = base64.b64decode(my_info['Token'])
    token_secret = base64.b64decode(my_info['Token_Secret'])
    
    
    #set query vars
    reonomy_loc = '40.749281,-73.994369' # lat long coordinates
    distance = '400'                     # 5 blocks in meters
    
    #set query
    url = ('http://api.yelp.com/v2/search?' \
            'sort=2&' \
            'term=%s&' \
            'll=%s&' \
            'radius_filter=%s'\
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
    import passwords
    
    #get passwords
    my_info = passwords.get_secure_info()
    #'decrypt passwords'
    consumer_key = base64.b64decode(my_info['Consumer_Key'])
    consumer_secret = base64.b64decode(my_info['Consumer_Secret'])
    token = base64.b64decode(my_info['Token'])
    token_secret = base64.b64decode(my_info['Token_Secret'])
    
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
    takes a distance in meteres and returns a distance in NYC Blocks
    '''
    feet_conversion = 3.28
    block_conversion = 264
    return ((dist_meters * feet_conversion) / block_conversion)

def connection(url):
    '''
    connects to yelp to extract data
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

def business_profile(bid):
    '''
    gets information specific to the business
    '''
    profile = connection(yelp_business(bid))

def find_lunch(search_term):
    '''
    queries yelp to get a list of delicious restaurants
    '''
    queried_resturants = {}
    #get search data from data from yelp
    data = connection(yelp_search(search_term))
    
    #extract data
    combiner = []
    for b in data['businesses']:
        combiner[:] = []
        combiner.append(b)
        #get business ratings
        combiner.append(business_profile(b['id']))
        queried_resturants[b['name']] = combiner
        break # limit to 1 query for now

    return queried_resturants

        