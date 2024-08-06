from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_artist = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artist = db.relationship('User', backref=db.backref('artworks', lazy=True))

    def __repr__(self):
        return f'<Artwork {self.title}>'

class ArtistProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    portfolio = db.Column(db.Text, nullable=True)
    user = db.relationship('User', backref=db.backref('artist_profile', uselist=False))

    def __repr__(self):
        return f'<ArtistProfile {self.user_id}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'), nullable=False)
    artwork = db.relationship('Artwork', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f'<Comment {self.id}>'

class Follow(db.Model):
    __tablename__ = 'follows'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', foreign_keys=[user_id])
    artist = db.relationship('User', foreign_keys=[artist_id])

    def __repr__(self):
        return f'<Follow user_id={self.user_id} artist_id={self.artist_id}>'
