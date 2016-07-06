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
session = DBSession()

def make_json_response(content,status_code):
    response = make_response(json.dumps(content,status_code))
    response.headers['Content-Type'] = 'application/json'
    return response



@app.route('/')
def index():

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))

    login_session['state'] = state

    username = None

    if not 'username' in login_session:
        username = None
    else:
        username = login_session['username']

    countries = session.query(Country).all()
    country_list = []
    for country in countries:
        country_item = {}
        country_item['id'] = country.id
        country_item['name'] = country.name
        if 'gplus_id' in login_session and country.add_owner == login_session['gplus_id']:
            country_item['editable'] = True
        else:
            country_item['editable'] = False
        country_list.append(country_item)

    return render_template('main.html',state=state,username=username,countries = country_list)

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
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]
    result = {'picture': login_session['picture'], 'username' : login_session['username']}
    return make_json_response(result,200)

#google-plus logout
@app.route('/gdisconnect',methods=['POST'])
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
        del login_session['picture']
        return make_json_response('Successfully connected',200)
    else:
        return make_json_response('Failed to revoke token for given user',400)



#JSON APIs to view 
@app.route('/country/<int:country_id>/football_club/JSON')
def countryfootballClubs(country_id):
    clubs = session.query(FootballClub).filter_by(country_id = country_id).all()
    return jsonify(football_clubs = [club.serialize for club in clubs])

@app.route('/country/JSON')
def countryJSON():
    countries =session.query(Country).all()
    return jsonify(countriy_list = [country.serialize for country in countries])

#Create new country
@app.route('/country/new',methods=['POST'])
def newCountry():
        country = Country(name=request.form.get('name'),add_owner=login_session['gplus_id'])
        session.add(country)
        session.commit()
        return redirect('/')
#Edit the country
@app.route('/country/<int:country_id>/edit',methods=['POST'])
def editCountry(country_id):
    country = session.query(Country).filter_by(id = country_id).first()
    if 'gplus_id' in login_session and login_session['gplus_id'] == country.add_owner:
        country.name = request.form.get('name')

    session.commit()
    return redirect('/')
#Delete the country
@app.route('/country/<int:country_id>/delete',methods=['POST'])
def deletecountry(country_id):
    country = session.query(Country).filter_by(id = country_id).first()
    country_club_list = session.query(FootballClub).filter_by(country_id = country.id).all()
    if 'gplus_id' in login_session and login_session['gplus_id'] == country.add_owner:
        if country_club_list:
            session.delete(country_club_list)
        if country:
            session.delete(country)
    session.commit()
    return make_json_response('Success',200)

#Show Football Club under specific country
@app.route('/country/<int:country_id>/football_club')
def showFootballClub(country_id):

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))

    login_session['state'] = state

    username = None


    if not 'username' in login_session:
        username = None
    else:
        username = login_session['username']

    countries = session.query(Country).all()
    country_list = []
    for country in countries:
        country_item = {}
        country_item['id'] = country.id
        country_item['name'] = country.name
        if 'gplus_id' in login_session and country.add_owner == login_session['gplus_id']:
            country_item['editable'] = True
        else:
            country_item['editable'] = False
        country_list.append(country_item)

    clubs = session.query(FootballClub).filter_by(country_id = country_id).all()
    club_list = []
    for club in clubs:
        club_item = {}
        club_item['id'] = club.id
        club_item['name'] = club.name
        club_item['country_id'] = club.country_id
        club_item['add_owner'] = club.add_owner
        if 'gplus_id' in login_session and club.add_owner == login_session['gplus_id']:
            club_item['editable'] = True
        else:
            club_item['editable'] = False

        club_list.append(club_item)

    selected_country = session.query(Country).filter_by(id = country_id).first()
    country_name = selected_country.name
    country_id = selected_country.id

    return render_template('main.html',state=state,username=username,countries = country_list,country_club_list = club_list,country_name = country_name,country_id = country_id)    

#Add new club in the country
@app.route('/country/<int:country_id>/football_club/new',methods=['POST'])
def newFootballClub(country_id):
    club = FootballClub(name = request.form.get('name'),country_id = country_id,add_owner = login_session['gplus_id'])
    session.add(club)
    session.commit()
    return redirect('/country/'+ str(country_id) + '/football_club')

#Edit the club in the country
@app.route('/country/<int:country_id>/football_club/<int:club_id>/edit',methods = ['POST'])
def editFootballClub(country_id,club_id):
    club = session.query(FootballClub).filter_by(id = club_id).first()
    if 'gplus_id' in login_session and login_session['gplus_id'] == club.add_owner:
    
        club.name = request.form.get('name')

    session.commit()
    return redirect('/country/'+ str(country_id) + '/football_club')
#Delete the club in the country
@app.route('/country/<int:country_id>/football_club/<int:club_id>/delete',methods = ['POST'])
def deleteFootballClub(country_id,club_id):
    club = session.query(FootballClub).filter_by(id = club_id).first()
    if 'gplus_id' in login_session and login_session['gplus_id'] == club.add_owner:
        session.delete(club)
    session.commit()
    return make_json_response('Success',200)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)