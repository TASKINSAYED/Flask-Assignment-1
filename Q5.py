from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Required to sign session data securely

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Store the user's name and email in the session
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('welcome'))
    
    return render_template('index_Q5.html')

@app.route('/welcome')
def welcome():
    # Retrieve the name and email from the session, if they exist
    name = session.get('name', 'Guest')
    email = session.get('email', 'Not provided')
    
    return render_template('welcome_Q5.html', name=name, email=email)

@app.route('/clear')
def clear_session():
    # Clear the session data
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0")