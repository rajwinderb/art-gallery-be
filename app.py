from flask import Flask, render_template, jsonify, request
from get_images.get_artworks import get_from_search

app = Flask(__name__)


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


if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
