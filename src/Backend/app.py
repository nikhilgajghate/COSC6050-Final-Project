import csv
import sys, os
from pathlib import Path
from flask import Flask, render_template, request, jsonify, url_for
from iteration1 import pronounce_name
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
    name = request.form.get("name")
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
                driver_id = db.insert_driver_record("single_text")
                db.insert_single_record(driver_id, name)
                print(f"📝 Logged single pronunciation to database: {name}")
            except Exception as db_error:
                print(f"⚠️  Database logging failed: {db_error}")
                # Continue even if database logging fails

        return jsonify({"audio_url": audio_url})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to generate pronunciation"}), 500


# Handles CSV uploads
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file or not file.filename.endswith(".csv"):
        return jsonify({"error": "Invalid file format"}), 400

    upload_folder = os.path.join("../Frontend/static", "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)

    #Read names from CSV
    audio_urls = []
    names_list = []  # Track names for database logging
    
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
            print(f"📝 Logged CSV upload to database: {file.filename} ({len(names_list)} names)")
        except Exception as db_error:
            print(f"⚠️  Database logging failed: {db_error}")
            # Continue even if database logging fails

    print("Returning JSON:", audio_urls)
    return jsonify({"audios": audio_urls})


# Health check route
@app.route("/api/health", methods=["GET"])
def health_check():
    """Check health of the application and database."""
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