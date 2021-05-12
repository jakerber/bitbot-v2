"""BitBot web app.

Not used by core BitBot runner.
"""
import flask

# initialize flask app
app = flask.Flask(__name__)


@app.route('/')
def root():
    """Root API endpoint."""
    return 'Bleep bloop'


if __name__ == '__main__':
    app.run(debug=True)
