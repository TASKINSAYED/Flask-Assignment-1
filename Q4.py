from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Required for CSRF protection

# Create a simple form
class NameForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():  # If form is submitted and validated
        name = form.name.data  # Get the input data
        return redirect(url_for('greet', name=name))  # Redirect to the greet page with the name as a parameter
    return render_template('index_Q4.html', form=form)

@app.route('/greet/<name>')
def greet(name):
    return render_template('greet_Q4.html', name=name)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
