# Import necessary libraries
from flask import Flask, render_template, request, send_file, redirect, url_for, flash  # Flask web framework and utilities
import os  # For file and directory operations
import pandas as pd  # For data processing
from werkzeug.utils import secure_filename  # For safely handling uploaded filenames
import uuid  # For generating unique IDs

# Initialize the Flask application
app = Flask(__name__)
# Set a secret key for session management and flash messages
app.secret_key = 'supersecretkey'

# Define base directory and folders for uploads and processed files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'static', 'processed')
# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}

# Create upload and processed folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Helper function to check if a file is allowed based on its extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the dashboard (home page)
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Route to process uploaded files
@app.route('/process', methods=['POST'])
def process():
    # Get uploaded files and form data
    files = request.files.getlist('files')
    filetype = request.form.get('filetype')
    null_action = request.form.get('null_action')  # How to handle null values
    pk_action = request.form.get('pk_action')      # How to handle primary key
    remove_duplicates = request.form.get('remove_duplicates')  # Whether to remove duplicates

    processed_files = []  # List to store info about processed files

    for file in files:
        if file and allowed_file(file.filename):
            # Secure the filename and generate a unique ID
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            file_id = str(uuid.uuid4())
            save_path = os.path.join(UPLOAD_FOLDER, file_id + '_' + filename)
            file.save(save_path)

            # Read the uploaded file into a pandas DataFrame
            if ext == 'csv':
                df = pd.read_csv(save_path)
            else:
                df = pd.read_excel(save_path)

            # Handle null values based on user selection
            if null_action == 'mean':
                df = df.fillna(df.mean(numeric_only=True))
            elif null_action == 'median':
                df = df.fillna(df.median(numeric_only=True))
            elif null_action == 'drop':
                df = df.dropna()

            # Remove duplicate rows if requested
            if remove_duplicates == 'on':
                df = df.drop_duplicates()

            # Assign a primary key column if requested
            if pk_action == 'assign':
                df.insert(0, 'PrimaryKey', range(1, 1 + len(df)))

            # Save the cleaned/processed file
            processed_filename = f"{file_id}_cleaned.{ext}"
            processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
            if ext == 'csv':
                df.to_csv(processed_path, index=False)
            else:
                df.to_excel(processed_path, index=False)

            # Add info for download link to the result page
            processed_files.append({
                'original': filename,
                'download': url_for('download_file', filename=processed_filename)
            })

    # If no valid files were uploaded, show an error and redirect
    if not processed_files:
        flash('No valid files uploaded!', 'error')
        return redirect(url_for('dashboard'))

    # Render the result page with download links for processed files
    return render_template('result.html', files=processed_files)

# Route to download a processed file
@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(PROCESSED_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)