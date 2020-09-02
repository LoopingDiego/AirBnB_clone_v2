#!/usr/bin/python3
""" Flask web application
"""

from flask import Flask, render_template
app = Flask(__name__, template_folder='templates')


@app.route('/', strict_slashes=False)
def greetings():
    """ Hello function
    """

    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ hbnb direction
    """

    return 'HBNB'


@app.route('/c/<txt>', strict_slashes=False)
def c_route(txt):
    """ String with C as first char
    """

    return "C {}".format(txt.replace('_', ' '))


@app.route('/python', strict_slashes=False)
@app.route('/python/<txt>', strict_slashes=False)
def python_route(txt='is cool'):
    """ String with Python as first word
    """

    return "Python {}".format(txt.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """ number testing
    """

    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def num_template(n):
    """ Return a html page with n H1 tag
    """

    return render_template('5-number.html',
                           h1="{}".format(n))


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even_route(n):
    """ number_odd_or_even_route
    """

    if n % 2:
        oddity = "odd"
    else:
        oddity = "even"
    return render_template("6-number_odd_or_even.html",
                           h1=n,
                           oddity=oddity)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
