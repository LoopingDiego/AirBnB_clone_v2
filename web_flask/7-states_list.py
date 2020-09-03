#!/usr/bin/python3
""" Flask web application.
"""

from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__, template_folder='templates')


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ Display HTML page with list of states.
    """

    return render_template('7-states_list.html',
                           states=storage.all(State).values())


@app.teardown_appcontext
def remove_session(response_or_exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
