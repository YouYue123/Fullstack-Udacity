from flask import Flask,render_template,session,redirect,url_for,escape,request

app = Flask(__name__,static_url_path="",static_folder="static")
app.secret_key = 'somesomelongstring'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,User,Catalog,Item
import random,string

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

"""
newEntry = ClassName(Property = "value",...)
session.add(newEntry)
session.commit()

entity = session.query(Classname).all() or .first()
entity.property
"""

@app.route('/')
def index():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    
	session['state'] = state
	return render_template('main.html',state = state)

@app.route('/logout')
def logout():
	session.pop('user_id',None)
	return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)