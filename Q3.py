from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Dynamic Content App! Use /greet?name=YourName&age=YourAge to get a personalized greeting."

@app.route('/greet')
def greet():
    # Get URL parameters (name and age)
    name = request.args.get('name', 'Guest')  # Default to 'Guest' if no name is provided
    age = request.args.get('age', 'unknown')  # Default to 'unknown' if no age is provided
    
    # Dynamic content based on URL parameters
    return f"Hello, {name}! You are {age} years old."

if __name__ == '__main__':
    app.run(host="0.0.0.0")
