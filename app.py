import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from models import db, User, Game, UserGameParticipation
from config import Config

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config.from_object(Config)

# Init extensions
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    games = Game.query.all()
    for game in games:
        game.creator = User.query.get(game.created_by)
        game_participations = game.participants
        participants_users = [participation.user for participation in game_participations]
        game.participants_users = participants_users

    return render_template('home.html', games=games)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already taken.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('home'))
        flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('home'))

@app.route('/add_game', methods=['GET', 'POST'])
@login_required
def add_game():
    if request.method == 'POST':
        title = request.form['title']
        max_players = request.form['max_players']
        description = request.form['description']
        game_type = request.form['game_type']
        image_file = request.files['image']

        if image_file and image_file.filename != '' and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            image_file.save(image_path)
        else:
            filename = 'NoImage.jpg'

        new_game = Game(
            title=title,
            max_players=max_players,
            description=description,
            game_type=game_type,
            image_filename=filename,
            created_by=current_user.id
        )
        db.session.add(new_game)
        db.session.commit()
        flash('Game added successfully.')
        return redirect(url_for('home'))

    return render_template('add_game.html')

@app.route('/join_game/<int:game_id>', methods=['POST'])
@login_required
def join_game(game_id):
    already_joined = UserGameParticipation.query.filter_by(user_id=current_user.id, game_id=game_id).first()
    if not already_joined:
        participation = UserGameParticipation(user_id=current_user.id, game_id=game_id)
        db.session.add(participation)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/leave_game/<int:game_id>', methods=['POST'])
@login_required
def leave_game(game_id):
    participation = UserGameParticipation.query.filter_by(user_id=current_user.id, game_id=game_id).first()
    if participation:
        db.session.delete(participation)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/game/<int:game_id>')
@login_required
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template('game_details.html', game=game)

@app.route('/delete_game/<int:game_id>', methods=['POST'])
@login_required
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)

    if game.created_by != current_user.id:
        flash("You are not authorized to delete this game.", "danger")
        return redirect(url_for('home'))

    db.session.delete(game)
    db.session.commit()
    flash("Game deleted successfully.", "success")
    return redirect(url_for('home'))


@app.route('/edit/<int:game_id>', methods=['GET', 'POST'])
@login_required
def edit_game(game_id):
    game = Game.query.get_or_404(game_id)
    if game.created_by != current_user.id:
        abort(403)

    if request.method == 'POST':
        game.title = request.form['title']
        game.description = request.form['description']
        game.max_players = request.form['max_players']
        game.game_type = request.form['game_type']

        #Images
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename != '' and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                image_file.save(image_path)
                game.image_filename = filename

        db.session.commit()
        flash('Game updated successfully!')
        return redirect(url_for('home'))

    return render_template('edit_game.html', game=game)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
