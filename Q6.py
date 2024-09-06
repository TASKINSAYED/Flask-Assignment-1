from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Directory to save uploaded files
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed file types

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    """Check if the file has one of the allowed extensions."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the user has selected a file
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']

        # If the user does not select a file, the browser also submits an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        
        # Save the file if it is allowed
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return redirect(url_for('uploaded_file', filename=filename))
    
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Display the uploaded file
    return render_template('display.html', filename=filename)

@app.route('/uploads/<filename>/display')
def display_image(filename):
    # Serve the file from the upload folder
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
