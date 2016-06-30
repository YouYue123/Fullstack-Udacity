from flask import Flask, render_template, request, redirect, jsonify, url_for, flash,make_response
from flask import session as login_session
#setup environment
app = Flask(__name__,static_url_path="",static_folder="static")
app.secret_key = 'somesomelongstring'
#For DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Country,FootballClub
#Python Library
import random,string,json,requests,httplib2
##For oAuth2
from oauth2client.client import flow_from_clientsecrets,FlowExchangeError

CLIENT_ID = json.loads(open('client_secrets.json','r').read())['web']['client_id'] 

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

def make_json_response(content,status_code):
    response = make_response(json.dumps(content,status_code))
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/')
def index():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    
	login_session['state'] = state
	return render_template('main.html',state = state)

#google-plus login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    
    # Validate state token
    if request.args.get('state') != login_session['state']:

        return make_json_response('Invalid state parameter',401)
    
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)

    except FlowExchangeError:

        return make_json_response('Failed to upgrade the authorization code.',401)

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:

        return make_json_response('error',500)

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:

        return make_json_response("Token's user ID doesn't match given user ID.",401)

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:

        return make_json_response("Token's client ID does not match app's.",401)

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:

        return make_json_response("Current user is already connected",200)

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)
    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"] 
    return make_json_response("Yes",200)

#google-plus logout
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    if access_token is None:

        return make_json_response("Current user is not connected",401)
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url,'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['pciture']
        return make_json_response('Successfully connected',200)
    else:
        return make_json_response('Failed to revoke token for given user',400)



#JSON APIs to view 
@app.route('/country/<int:country_id>/football_club/JSON')
def countryfootballClubs(country_id):

    return jsonfy(football_clubs = FootballClub.serialize)

@app.route('/country/JSON')
def countryJSON():
    return jsonfy()


#View country
@app.route('/')
@app.route('/country')
def country():
	country_list = session.query(Country).all()
	return render_template('country.html'，country_list = country_list)
#Create new country
@app.route('/country/new/')
def newCountry():
    if request.method = 'GET':
	   return render_template('new_country.html')
    if request.method = 'POST':

#Edit the country
@app.route('/country/<int:country_id>/edit',methods=['POST'])

#Delete the country
@app.route('/country/<int:country_id>/delete',methods=['POST'])

#View clubs under the country
@app.route('/country/<int:country_id>/football_club/',methods=['GET'])

#Add new club in the country
@app.route('/country/<int:country_id>/football_club/new')
def newFootballClub():

    if reqeust.method = 'GET':

    if request.method = 'POST':

#Edit the club in the country
@app.route('/country/<int:country_id>/football_club/<int:club_id>/edit',methods['POST'])

#Delete the club in the country
@app.route('/country/<int:country_id>/football_club/<int:club_id>/delete',methods['POST'])
def test():
	return render_template('test.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)