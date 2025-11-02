import csv
import sys, os
from pathlib import Path
from flask import Flask, render_template, request, jsonify, url_for
from service import pronounce_name
from databridge import get_db

app = Flask(__name__,
            template_folder = "../Frontend/templates",
            static_folder = "../Frontend/static"
            )

# Route for main page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# Handles pronunciation without reloading
@app.route("/pronounce", methods=["POST"])
def pronounce():
    """
    Flask router for single name pronunciation.
    """

    # Retrieve user input/name from form data
    name = request.form.get("name")

    # Return a 404 error if user input is not provided. 
    if not name:
        return jsonify({"error": "No name provided"}), 400

    try:
        # Generate and save pronunciation audio
        audio_path = pronounce_name(name)
        audio_url = url_for('static', filename=f"audio/{os.path.basename(audio_path)}")

        # Log to database if available
        db = get_db()
        if db:
            try:
                # Insert driver record
                driver_id = db.insert_driver_record("single_text")

                # Insert user input into single table
                single_id = db.insert_single_record(driver_id, name)
                print(f"Logged single pronunciation to database: {name}")

                return jsonify({
                    "user request": name,
                    "status": "success",
                })
            except Exception as db_error:
                print(f"Database logging failed: {db_error}")

                return jsonify({
                    "user request": name,
                    "status": "error",
                    "error": str(db_error),
                }), 500


# Handles CSV uploads
@app.route("/upload", methods=["POST"])
def upload():
    """
    Flask router for CSV file upload. 
    """
    # Retrieve user uploaded file from form data
    file = request.files.get("file")

    # Return a 404 error if the user provided file is not of type CSV
    if not file or not file.filename.endswith(".csv"):
        return jsonify({"error": "Invalid file format"}), 400

    # Create the upload folder if one does not exist
    upload_folder = os.path.join("../Frontend/static", "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)

    # Read names from CSV
    audio_urls = []
    names_list = [] # Track names for returning to the frontend + database persistence. 
    
    # Loop through the CSV and pronounce each name
    try:
        with open(filepath, newline='',encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not row or not row[0].strip():
                    continue
                name = row[0].strip()
                names_list.append(name)  # Add to list for database
                print(f"Processing name: {name}")
                try:
                    audio_path = pronounce_name(name)
                    audio_url = url_for('static', filename=f'audio/{os.path.basename(audio_path)}')
                    audio_urls.append({"name": name, "audio_url": audio_url})
                except Exception as e:
                    print(f"Error pronouncing '{name}': {e}")
    except Exception as e:
        print("CSV Read Error:", e)
        return jsonify({"error": str(e)}), 500

    if not audio_urls:
        print("No valid names found in CSV or audio generation failed.")

    # Log to database if available
    db = get_db()
    if db and names_list:
        try:
            driver_id = db.insert_driver_record("csv_upload")
            db.insert_csv_upload_record(driver_id, file.filename, names_list)
            print(f"Logged CSV upload to database: {file.filename} ({len(names_list)} names)")
            return jsonify({
                "user request": names_list,
                "status": "success",
            })
        except Exception as db_error:
            print(f"Database logging failed: {db_error}")
            # Continue even if database logging fails

    print("Returning JSON:", audio_urls)
    return jsonify({"audios": audio_urls})


# Health check route
@app.route("/api/health", methods=["GET"])
def health_check():
    """
        Flask router to ensure the application + database are running as intended.
    """
    # Retrieve the DB
    db = get_db()
    
    health_status = {
        "status": "healthy",
        "database": "not_configured"
    }
    
    if db:
        if db.test_connection():
            health_status["database"] = "connected"
        else:
            health_status["database"] = "error"
            health_status["status"] = "degraded"
    
    return jsonify(health_status)



if __name__ == "__main__":
    app.run(debug=True)