from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from pymongo import MongoClient

app = Flask(__name__)

#conexion a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['login-google']
collection = db['users']

app.secret_key = 'myscretkey'
#configuraciones de oauth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="",
    client_secret="",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)

##observamos el correo cuando nos redirecciona 
@app.route("/")
def index():
    return f'usuario existente'


@app.route('/login')
def registro():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    profile = resp.json()
    # do something with the token and profile
    print(profile, token)
    user = collection.find_one({"_id": profile['id']}) #Buscamos si existe ese id en la base de datos
    if user:
        return redirect('/')
    else:
        new_user = {
            "_id": profile['id'],
            "correo": profile['email'],
            "avatar": profile['picture']
        }
        collection.save(new_user) #Guardamos el usuario en la Base de Datos
        return redirect('http://localhost:3000/inicio')


if __name__ == "__main__":
    app.run(debug=True)
