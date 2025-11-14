import csv
import sys, os
from pathlib import Path

import requests
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
            db.insert_single_record(driver_id, name)
            print(f"Logged single pronunciation to database: {name}")
        except Exception as db_error:
            print(f"Database logging failed: {db_error}")

    return jsonify({
        "user request": name,
        "audio_url": audio_url,
        "status": "success"
    })


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

#Name Origin and Ethnicity

BTN_API_KEY = os.getenv("BTN_API_KEY")

@app.route("/name_facts", methods=["POST"])
def name_facts():
    name = request.form.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400

    first_name = name.split()[0].strip()

    result = {
        "name": name,
        "origin": "Unknown",
        "ethnicity": []
    }

    #  Nationalize.io ( Handles Ethnicity Probability)
    top_country = None
    top_prob = 0.0

    try:
        nat_res = requests.get(f"https://api.nationalize.io/?name={first_name}", timeout=5)
        if nat_res.status_code == 200:
            nat_data = nat_res.json()
            for c in nat_data.get("country", []):
                prob = round(c.get("probability", 0.0) * 100, 1)
                country_id = c.get("country_id")

                result["ethnicity"].append({
                    "country": country_id,
                    "probability": prob
                })

                if prob > top_prob:
                    top_prob = prob
                    top_country = country_id

    except Exception:
        pass

    # Behind The Name API (handles the Origin) --------
    try:
        if BTN_API_KEY:
            url = "https://www.behindthename.com/api/lookup.json"
            params = {"name": first_name, "key": BTN_API_KEY}
            r = requests.get(url, params=params, timeout=5)

            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list) and len(data) > 0:
                    entry = data[0]
                    usages = entry.get("usages", [])
                    origins = [u.get("usage_full") for u in usages if u.get("usage_full")]

                    if origins:
                        result["origin"] = ", ".join(origins)

    except Exception:
        pass

    # Origin Backup (Using Nationalize)
    if result["origin"] == "Unknown":
        if top_country and top_prob >= 25:  # Only assign if strong probability
            result["origin"] = f"Likely {top_country}"
        else:
            result["origin"] = "Not available"

    return jsonify(result)


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
    app.run(debug=True, port=5051)