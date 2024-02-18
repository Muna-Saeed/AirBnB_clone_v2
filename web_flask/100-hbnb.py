#!/usr/bin/python3
""" Starts a Flask web application """

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Display a HTML page like 8-index.html """
    states = storage.all(State).values()
    cities = storage.all(City).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    return render_template('100-hbnb.html', states=sorted(states, key=lambda x: x.name),
                           cities=sorted(cities, key=lambda x: x.name),
                           amenities=sorted(amenities, key=lambda x: x.name),
                           places=sorted(places, key=lambda x: x.name))


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
