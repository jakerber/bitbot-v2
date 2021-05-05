"""BitBot web app."""
import flask

# initialize flask app
app = flask.Flask(__name__)

@app.route("/")
def root():
    """Root API endpoint."""
    return "Hello, world!"


if __name__ == "__main__":
    app.run(debug=True)
