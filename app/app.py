"""entry point"""
from flask import Flask

from .features import image, index

app = Flask(__name__)


@app.route('/', defaults={'name': 'index'})
@app.route('/<path:name>.php')
def home(name):
    return index.php(name)


@app.route('/comics/<path:name>.png')
def get_comic(name):
    return image.comic(name)


@app.route('/<path:full_path>')
def catch_all(full_path: str):
    name = full_path.split('.')[0]

    return image.png(name)
