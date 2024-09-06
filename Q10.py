from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the home page!"

@app.route('/error')
def error():
    # This route is used to trigger a 500 error
    raise Exception("This is a test exception")

if __name__ == '__main__':
    app.run(host="0.0.0.0")

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    # Log the error details for debugging
    app.logger.error('An error occurred: %s', (error))
    return render_template('500.html'), 500

import logging
from logging.handlers import RotatingFileHandler

# Set up logging
if not app.debug:
    # Only set up logging if not in debug mode
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)
