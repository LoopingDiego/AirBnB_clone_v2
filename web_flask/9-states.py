#!/usr/bin/python3
""" Flask web application.
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
app = Flask(__name__, template_folder='templates')


@app.teardown_appcontext
def app_context(abc):
    """ Kill SQLAlchemy session.
    """

    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_list(id='0'):
    """ Display a HTML page inside the tag BODY.
    """

    return render_template('9-states.html',
                           states=storage.all(State).values(), id=id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
