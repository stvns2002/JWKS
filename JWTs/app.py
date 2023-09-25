from flask import Flask, jsonify, request, make_response, render_template, session
import jwt
from datetime import datetime, timedelta
from functools import wraps
import webbrowser

app = Flask(__name__)
app.config['SECRET_KEY'] = '8118ec6e1221496996a59774261f4469'

#declares function that checks for token in auth endpoint 
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!':'JWT is verified, Welcome!'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'Alert!': 'Invalid Token'})
    return decorated


#Home and login sheet using login.html in templates, providing access to token
@app.route('/')
def home(name=None):
    if not session.get('logged in'):
        return render_template('login.html', name=name)
    else:
        return  'Logged in currently!'
    

#For anyone or the public, doesnt require token
@app.route('/public')
def public():
    return'For Public'


#For users with authentic token, authenticates if token is not expired
@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified, Welcome!'


#For login and Authentication(Using restFul api), proceeds when given username and password
@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in']= True
        token = jwt.encode({
            'user':request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=150))
        },
            app.config['SECRET_KEY'])
        return jsonify({'token': token})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate' : 'Basic realm:"Authentication Failed!'})


#setting up application and using automatic web opening
if __name__ == '__main__':
    url = 'http://127.0.0.1:8080'
    webbrowser.open_new(url)
    app.run(debug=True, port=8080)