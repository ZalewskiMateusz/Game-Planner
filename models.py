from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    max_players = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_by_user = db.relationship('User', backref='created_games', lazy=True)
    image_filename = db.Column(db.String(100), nullable=False, default='NoImage.jpg')
    game_type = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            "title": self.title,
            "image_filename": self.image_filename,
            "game_type": self.game_type,
            "description": self.description,
            "max_players": self.max_players,
            "created_by": self.created_by_user.username
        }

class UserGameParticipation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
