from flask import Flask, render_template, request, redirect, url_for, flash
import os
from utils import detect_deepfake
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Run deepfake detection
        results = detect_deepfake(file_path, 'model/deepfake_detector.h5')
        
        return render_template('result.html', filename=filename, results=results)
    else:
        flash('Invalid file format. Please upload a .mp4 video.')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
