from app import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from sqlalchemy.orm import validates


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum('A', 'D', 'E'),
                       server_default='A',
                       nullable=False)
    register_date = db.Column(db.DateTime,
                              server_default=db.func.current_timestamp(),
                              nullable=False)


class User(Base):
    __tablename__ = 'user'
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    document = db.Column(db.String(11), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    celphone = db.Column(db.String(20), nullable=False)
    telephone = db.Column(db.String(20))

    def __init__(self, document, name, lastname, email, password,
                 celphone=None, telephone=None):
        self.document = document
        self.name = name
        self.lastname = lastname
        self.email = email
        self.celphone = celphone
        self.telephone = telephone
        self.password = password

    def save(self):
        try:
            password = self.create_password(self.password)
            data = User(self.document, self.name, self.lastname, self.email,
                        password, self.celphone, self.telephone)
            db.session.add(data)
            db.session.commit()
            return True
        except Exception:
            return False

    def create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @validates('email')
    def validate_email(self, key, email):
        data = User.query.filter_by(email=email).first()
        if data:
            raise ValueError(
                "El correo ya se encuentra registrado")
        else:
            return email

    def get_by_email(email):
        return User.query.filter(User.email == email, User.status == 'A',
                                 User.type_user != 'S').first()

    def get_by_id(pk):
        return User.query.filter_by(id=pk).first()

    def update(pk, ranges_id, is_financing):
        data = User.query.filter_by(id=pk).first()
        if data is None:
            return False
        data.ranges_id = ranges_id
        data.is_financing = is_financing
        db.session.commit()
        return True


class Client(db.Model):
    # creator of the client, not required
    user_id = db.Column(db.ForeignKey('user.id'))
    # required if you need to support client credential
    user = db.relationship('User')

    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), unique=True, index=True,
                              nullable=False)
    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    def __init__(self, user_id, client_id, client_secret, _redirect_uris,
                 _default_scopes):
        self.user_id = user_id
        self.client_id = client_id
        self.client_secret = client_secret
        self._redirect_uris = _redirect_uris
        self._default_scopes = _default_scopes

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []


class Grant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')

    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    code = db.Column(db.String(255), index=True, nullable=False)

    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)

    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id')
    )
    user = db.relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
