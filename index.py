from flask import Flask, jsonify, request, url_for, session, redirect
from flask_cors import CORS, cross_origin
import urllib.request
import json
import URL
from datetime import timedelta
from functools import wraps
from authlib.integrations.flask_client import OAuth


CLIENT_ID = '589168516609-ait0c02qa91mh2o3lamlemqmoqkt8dpv.apps.googleusercontent.com'
CLIENT_SECRET = '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'
APP_SECRET = '20628199e8441e0d39372e7cf25542ae'


app = Flask(__name__)

# enable cors in developement
CORS(app, support_credentials=True)

# because some currencies contains utf-8 chars
app.config['JSON_AS_ASCII'] = False

# Session config
app.secret_key = APP_SECRET
app.config['SESSION_COOKIE_NAME'] = 'login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    # This is only needed if using openId to fetch user info
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('profile', None)
        # You would add a check here and usethe user id or something to fetch
        # the other data for that user/check if they exist
        if user:
            return f(*args, **kwargs)
        return 'You aint logged in, no page for u!'
    return decorated_function


@cross_origin(supports_credentials=True)
@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@cross_origin(supports_credentials=True)
@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    # Access token from google (needed to get user info)
    token = google.authorize_access_token()
    # userinfo contains stuff u specificed in the scrope
    resp = google.get('userinfo')
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    # keep remember me to true
    session.permanent = True
    return redirect('/')


@cross_origin(supports_credentials=True)
@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


@login_required
@app.route("/currencies")
def get_currencies():
    # Open the orders.json file
    with open("currencies.json", mode="r", encoding="utf-8") as file:
        # Load its content and make a new dictionary
        data = json.load(file)
    return jsonify(data)


@cross_origin(supports_credentials=True)
@app.route("/latest")
def get_latest():
    user = dict(session).get('profile', None)
    # You would add a check here and usethe user id or something to fetch
    # the other data for that user/check if they exist
    if user:
        with open("latest.json", mode="r", encoding="utf-8") as file:
            data = json.load(file)
        return jsonify(data)
    return jsonify({"error": "Missing Authentication", }), 403
    # url = URL.LATEST_URL
    # response = urllib.request.urlopen(url)
    # data_json = response.read()
    # data_dict = json.loads(data_json)
    # return jsonify(data_dict)


@app.route("/historic")
def get_historic():
    date = request.args.get("date")
    url = URL.HISTORICAL_URL.format(date)
    response = urllib.request.urlopen(url)
    data_json = response.read()
    data_dict = json.loads(data_json)
    return jsonify(data_dict)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(debug=True)
