import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify, request
from get_images.get_artworks import get_from_search
from utils_functions import dict_clean

load_dotenv()

app = Flask(__name__)

DATABASE_URL = None

if os.getenv('DEVELOPMENT'):
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://toeqqqdcmqxobw:4864ae538a3067220073bcf18185009f121f4f3026bac0e8ded5d0f865d903c3@ec2-54-220-243-77.eu-west-1.compute.amazonaws.com:5432/ddtjgf4o8osh6v'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class artists(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    artistdisplayname = db.Column(db.String(250), nullable=False)
    artistdisplaybio = db.Column(db.String)
    artistgender = db.Column(db.String)

    def __init__(self, artistdisplayname, artistdisplaybio, artistgender):
        self.artistdisplayname = artistdisplayname
        self.artistdisplaybio = artistdisplaybio
        self.artistgender = artistgender


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


class tagRelations(db.Model):
    __tablename__ = "tagrelations"
    tagid = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, nullable=False)
    artid = db.Column(db.Integer, db.ForeignKey('artworks.id'), primary_key=True, nullable=False)

    def __init__(self, tagid, artid):
        self.tagid = tagid
        self.artid = artid


class userArt(db.Model):
    __tablename__ = "userart"
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    artid = db.Column(db.Integer, db.ForeignKey('artworks.id'), primary_key=True, nullable=False)
    isfavourite = db.Column(db.Boolean, default=False)

    def __init__(self, userid, artid, isfavourite=False):
        self.userid = userid
        self.artid = artid
        self.isfavourite = isfavourite if isfavourite is not False else False


class artworks(db.Model):
    __tablename__ = 'artworks'
    id = db.Column(db.Integer, primary_key=True)
    ishighlight = db.Column(db.Boolean, nullable=False)
    primaryimage = db.Column(db.String, nullable=False)
    primaryimagesmall = db.Column(db.String, nullable=False)
    department = db.Column(db.String(150))
    objectname = db.Column(db.String(100))
    title = db.Column(db.String)
    culture = db.Column(db.String(150))
    period = db.Column(db.String(150))
    dynasty = db.Column(db.String(150))
    artistprefix = db.Column(db.String(150))
    artistid = db.Column(db.Integer, db.ForeignKey('artists.id'))
    objectdate = db.Column(db.String(150))
    medium = db.Column(db.String(150))
    country = db.Column(db.String(150))
    classification = db.Column(db.String(150))
    linkresource = db.Column(db.String)
    featured = db.Column(db.Boolean, default=False)

    def __init__(self, id, ishighlight, primaryimage, primaryimagesmall, department, objectname, title, culture, period,
                 dynasty, artistprefix, artistid, objectdate, medium, country, classification, linkresource,
                 featured=False):
        self.id = id
        self.ishighlight = ishighlight
        self.primaryimage = primaryimage
        self.primaryimagesmall = primaryimagesmall
        self.department = department
        self.objectname = objectname
        self.title = title
        self.culture = culture
        self.period = period
        self.dynasty = dynasty
        self.artistprefix = artistprefix
        self.artistid = artistid
        self.objectdate = objectdate
        self.medium = medium
        self.country = country
        self.classification = classification
        self.linkresource = linkresource
        self.featured = featured if featured is not False else False


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
        user_data = dict_clean(dict(user_data))
        in_database = users.query.filter_by(username=user_data['username']).first()
        if in_database:
            return jsonify({'status': 'failed', 'message': 'This username already exists, try another'}, user_data)
        new_user = users(username=user_data['username'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'user added',
                        'new_user': {'id': new_user.id, 'username': new_user.username}})
    return jsonify({'status': 'failed'}, 404)


@app.route('/tags', methods=['GET'])
def get_tags():
    if request.method == 'GET':
        all_tags = []
        response = tags.query.all()
        for tag in response:
            current_tag = {'id': tag.id, 'tag': tag.tag}
            all_tags.append(current_tag)
        return jsonify({'status': 'success', 'tags': all_tags})
    return jsonify({'status': 'failed'}, 404)


@app.route('/artworks', methods=['POST'])
def add_artwork():
    if request.method == 'POST':
        artwork_data = request.get_json()
        artwork_data = dict_clean(dict(artwork_data))
        tags_data = artwork_data['tags']
        artwork_in_database = artworks.query.filter_by(id=artwork_data['id']).first()
        if artwork_in_database:
            return jsonify({'status': 'failed', 'message': 'This artwork already exists, try another'}, artwork_data)
        artist_in_database = artists.query.filter_by(artistdisplayname=artwork_data["artistDisplayName"]).first()
        artist_id = artist_in_database.id if artist_in_database is not None else 0
        if artist_in_database is None:
            new_artist = artists(artistdisplayname=artwork_data['artistDisplayName'],
                                 artistdisplaybio=artwork_data['artistDisplayBio'],
                                 artistgender=artwork_data['artistGender'])
            db.session.add(new_artist)
            db.session.flush()
            artist_id = new_artist.id
        new_artwork = artworks(id=artwork_data['id'],
                               primaryimage=artwork_data['primaryImage'],
                               primaryimagesmall=artwork_data['primaryImageSmall'],
                               department=artwork_data['department'],
                               objectname=artwork_data['objectName'],
                               title=artwork_data['title'],
                               culture=artwork_data['culture'],
                               period=artwork_data['period'],
                               dynasty=artwork_data['dynasty'],
                               artistprefix=artwork_data['artistPrefix'],
                               artistid=artist_id,
                               objectdate=artwork_data['objectDate'],
                               medium=artwork_data['medium'],
                               country=artwork_data['country'],
                               classification=artwork_data['classification'],
                               linkresource=artwork_data['linkResource'],
                               featured=artwork_data['featured'],
                               ishighlight=artwork_data['isHighlight'])
        db.session.add(new_artwork)
        db.session.flush()
        artwork_id = new_artwork.id
        for tag_check in tags_data:
            tag_in_database = tags.query.filter_by(tag=tag_check).first()
            tag_id = tag_in_database.id if tag_in_database is not None else 0
            if tag_in_database is None:
                new_tag = tags(tag=tag_check)
                db.session.add(new_tag)
                db.session.flush()
                tag_id = new_tag.id

            new_tag_relation = tagRelations(tagid=tag_id, artid=artwork_id)
            db.session.add(new_tag_relation)
            db.session.flush()
            db.session.commit()

        return jsonify({'status': 'success', 'message': 'new artwork added', 'new_artwork_id': artwork_id})
    return jsonify({'status': 'failed'}, 404)


@app.route('/artworks', methods=['GET'])
def get_artworks():
    if request.method == 'GET':
        all_artworks = []
        response = db.session.query(artworks, artists).join(artists).all()
        for artwork in response:
            tags_response = db.session.query(tags, tagRelations).join(tagRelations).filter_by(artid=artwork[0].id).all()
            artwork_tags = []
            for tag in tags_response:
                artwork_tags.append({'id': tag[0].id, 'tag': tag[0].tag})
            current_artwork = {'id': artwork[0].id,
                               'primaryimage': artwork[0].primaryimage,
                               'primaryimagesmall': artwork[0].primaryimagesmall,
                               'department': artwork[0].department,
                               'objectname': artwork[0].objectname,
                               'title': artwork[0].title,
                               'culture': artwork[0].culture,
                               'period': artwork[0].period,
                               'dynasty': artwork[0].dynasty,
                               'artistprefix': artwork[0].artistprefix,
                               'artistid': artwork[0].artistid,
                               'objectdate': artwork[0].objectdate,
                               'medium': artwork[0].medium,
                               'country': artwork[0].country,
                               'classification': artwork[0].classification,
                               'linkresource': artwork[0].linkresource,
                               'featured': artwork[0].featured,
                               'ishighlight': artwork[0].ishighlight,
                               'artistdisplayname': artwork[1].artistdisplayname,
                               'artistdisplaybio': artwork[1].artistdisplaybio,
                               'artistgender': artwork[1].artistgender,
                               'tags': artwork_tags}
            all_artworks.append(current_artwork)
        return jsonify({'status': 'success', 'artworks': all_artworks})
    return jsonify({'status': 'failed'}, 404)


@app.route('/userart/<int:userid>', methods=['GET'])
def get_user_art(userid):
    if request.method == 'GET':
        all_artworks = []
        response = db.session.query(artworks, artists, userArt).select_from(artworks).join(artists).join(userArt) \
            .filter_by(userid=userid).all()
        for artwork in response:
            tags_response = db.session.query(tags, tagRelations).join(tagRelations).filter_by(artid=artwork[0].id).all()
            artwork_tags = []
            for tag in tags_response:
                artwork_tags.append({'id': tag[0].id, 'tag': tag[0].tag})
            current_artwork = {'id': artwork[0].id,
                               'primaryimage': artwork[0].primaryimage,
                               'primaryimagesmall': artwork[0].primaryimagesmall,
                               'department': artwork[0].department,
                               'objectname': artwork[0].objectname,
                               'title': artwork[0].title,
                               'culture': artwork[0].culture,
                               'period': artwork[0].period,
                               'dynasty': artwork[0].dynasty,
                               'artistprefix': artwork[0].artistprefix,
                               'artistid': artwork[0].artistid,
                               'objectdate': artwork[0].objectdate,
                               'medium': artwork[0].medium,
                               'country': artwork[0].country,
                               'classification': artwork[0].classification,
                               'linkresource': artwork[0].linkresource,
                               'featured': artwork[0].featured,
                               'ishighlight': artwork[0].ishighlight,
                               'artistdisplayname': artwork[1].artistdisplayname,
                               'artistdisplaybio': artwork[1].artistdisplaybio,
                               'artistgender': artwork[1].artistgender,
                               'tags': artwork_tags,
                               'isfavourite': artwork[2].isfavourite}
            all_artworks.append(current_artwork)
        return jsonify({'status': 'success', 'artworks': all_artworks})
    return jsonify({'status': 'failed'}, 404)


@app.route('/userart/<int:userid>', methods=['POST'])
def add_user_art(userid):
    if request.method == 'POST':
        user_art_data = request.get_json()
        user_art_data = dict_clean(dict(user_art_data))
        in_database = userArt.query.filter_by(userid=userid, artid=user_art_data['artid']).first()
        if in_database:
            return jsonify({'status': 'failed', 'message': 'This is already in your art gallery, try another'},
                           user_art_data)
        new_user_art = userArt(userid=userid, artid=user_art_data['artid'], isfavourite=user_art_data['isFavourite'])
        db.session.add(new_user_art)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'user art added',
                        'new_user_art': {'userid': new_user_art.userid, 'artid': new_user_art.artid,
                                         'isfavourite': new_user_art.isfavourite
                                         }
                        })
    return jsonify({'status': 'failed'}, 404)


@app.route('/userart/<int:userid>', methods=['DELETE'])
def delete_user_art(userid):
    if request.method == 'DELETE':
        user_art_data = request.get_json()
        user_art_data = dict_clean(dict(user_art_data))
        user_art_delete = userArt.query.filter_by(userid=userid, artid=user_art_data['artid']).first()
        if user_art_delete is None:
            jsonify({'status': 'failed', 'message': 'This is not in your art gallery, try another'},
                    user_art_data)
        userArt.query.filter_by(userid=userid, artid=user_art_data['artid']).delete()
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'user art deleted'})
    return jsonify({'status': 'failed'}, 404)


@app.route('/artworks/<int:artid>', methods=['PUT'])
def update_artwork(artid):
    update_data = request.get_json()
    update_data = dict_clean(dict(update_data))
    artwork = artworks.query.filter_by(id=artid).first()
    artwork.featured = update_data['featured']
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'featured changed', 'featured': artwork.featured})


@app.route('/userart/<int:userid>', methods=['PUT'])
def update_user_art(userid):
    update_data = request.get_json()
    update_data = dict_clean(dict(update_data))
    user_art = userArt.query.filter_by(userid=userid, artid=update_data['artid']).first()
    user_art.isfavourite = update_data['isfavourite']
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'isfavourite changed', 'is_favourite': user_art.isfavourite})


if __name__ == '__main__':
    app.run(port=5000)
