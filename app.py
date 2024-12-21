import os
from flask import Flask, render_template, request, jsonify,redirect

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Set an appropriate folder for storing uploaded files

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

    # Save the uploaded files
    resume_file = request.files['resume']
    job_description_file = request.files['job_description']

    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
    job_description_path = os.path.join(app.config['UPLOAD_FOLDER'], job_description_file.filename)

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
        # Pass the similarity score to the HTML template
        return render_template('index.html', similarity_score=similarity_score)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
