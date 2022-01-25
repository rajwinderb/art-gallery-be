import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify, request
from get_images.get_artworks import get_from_search

load_dotenv()

app = Flask(__name__)

if os.getenv('DEVELOPMENT'):
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.debug = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)

    def __init__(self, username):
        self.username = username


class tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(150), nullable=False)

    def __init__(self, tag):
        self.tag = tag


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/<string:search_term>', methods=['GET'])
def search(search_term):
    search_results = get_from_search(search_term)
    if len(search_results) == 0:
        return jsonify({'status': 'success', 'message': 'no results found'})
    else:
        return jsonify({'status': 'success', 'artworks': search_results})


@app.route('/users', methods=['GET'])
def get_users():
    if request.method == 'GET':
        all_users = []
        response = users.query.all()
        for user in response:
            current_user = {'id': user.id, 'username': user.username}
            all_users.append(current_user)
        return jsonify({'status': 'success', 'users': all_users})
    return jsonify({'status': 'failed'}, 404)


@app.route('/users', methods=['POST'])
def add_users():
    if request.method == 'POST':
        user_data = request.get_json()
        in_database = users.query.filter_by(username=user_data['username']).first()
        if in_database:
            return jsonify({'status': 'failed', 'message': 'This username already exists, try another'}, user_data)
        new_user = users(username=user_data['username'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'user added'}, user_data)
    return jsonify({'status': 'failed'}, 404)


@app.route('/tags', methods=['GET'])
def get_tags():
    if request.method == 'GET':
        all_tags = []
        response = tags.query.all()
        for tag in response:
            current_tag = {'id': tag.id, 'tag': tag.username}
            all_tags.append(current_tag)
        return jsonify({'status': 'success', 'tags': all_tags})
    return jsonify({'status': 'failed'}, 404)


# @app.route('/artworks', method=['POST'])


if __name__ == '__main__':
    app.run(port=5000)
