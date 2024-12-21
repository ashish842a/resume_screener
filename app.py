import os
from flask import Flask, render_template, request, jsonify, redirect
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Set environment variables or use defaults for production
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')  # Set a default path or use environment variable
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Assuming the screen_resume function is already defined
from screener import screen_resume

@app.route('/')
def home():
    return render_template('index.html', similarity_score=None)

@app.route('/screen', methods=['GET'])
def screen_get():
    # Redirect any GET requests for '/screen' to the home page
    return redirect('/')

@app.route('/screen', methods=['POST'])
def screen():
    """Handle file uploads and calculate similarity."""
    
    if 'resume' not in request.files or 'job_description' not in request.files:
        return jsonify({"error": "Missing resume or job description file"}), 400

    resume_file = request.files['resume']
    job_description_file = request.files['job_description']

    # Ensure the file extensions are allowed
    if not (allowed_file(resume_file.filename) and allowed_file(job_description_file.filename)):
        return jsonify({"error": "Invalid file format. Only PDF and TXT files are allowed."}), 400

    # Secure filenames and save the files
    resume_filename = secure_filename(resume_file.filename)
    job_description_filename = secure_filename(job_description_file.filename)

    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
    job_description_path = os.path.join(app.config['UPLOAD_FOLDER'], job_description_filename)

    # Save files to the specified path
    resume_file.save(resume_path)
    job_description_file.save(job_description_path)

    # Read job description text
    try:
        with open(job_description_path, 'r') as f:
            job_description = f.read()
    except Exception as e:
        return jsonify({"error": f"Failed to read job description file: {str(e)}"}), 500

    # Calculate similarity
    try:
        similarity_score = screen_resume(resume_path, job_description)
        # Return the result with similarity score
        return render_template('index.html', similarity_score=similarity_score)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the application in production
if __name__ == '__main__':
    # Get the port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
