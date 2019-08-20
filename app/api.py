from flask import Blueprint, jsonify
from app.models import User, Client, Grant, Token
from app import db, oauth
from datetime import datetime, timedelta
from flask import request


mod_oauth = Blueprint('oauth', __name__, url_prefix='/oauth')


@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=1000)
    client = Client.query.filter_by(client_id=client_id).first()
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=client.user_id,
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant


@oauth.tokengetter
def bearer_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(
        client_id=request.client.client_id,
        user_id=request.user.id
    )
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)
    # expires_in = token.pop('expires_in')
    expires_in = 36000
    expires = datetime.utcnow() + timedelta(seconds=expires_in)
    refresh_token = None
    if 'refresh_token' in token:
        refresh_token = token['refresh_token']
    tok = Token(
        access_token=token['access_token'],
        refresh_token=refresh_token,
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db.session.add(tok)
    db.session.commit()
    return tok


@oauth.usergetter
def get_user(username, password, *args, **kwargs):
    user = User.query.filter_by(email=username).first()
    if user is not None and user.verify_password(password):
        return user
    return None


@mod_oauth.route('/index', methods=['GET', 'POST'])
def index():
    return "Hello world"


@mod_oauth.route('/me', methods=['POST'])
@oauth.require_oauth()
def me():
    user = request.oauth.user
    result = {'email': user.email,
              'name': user.name,
              'lastname': user.lastname,
              'document': user.document,
              'celphone': user.celphone,
              'telephone': user.telephone}
    return jsonify(result)


@mod_oauth.route('/token', methods=['GET', 'POST'])
@oauth.token_handler
def access_token():
    return None


@mod_oauth.route('/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    # print(kwargs.get('client_id'))
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client_id
        # kwargs['user'] = user
        return client.client_id
    return True
