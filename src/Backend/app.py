import csv
import sys, os
from fileinput import filename
from flask import Flask, render_template, request, jsonify, url_for
from iteration1 import pronounce_name

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
    try:
        with open(filepath, newline='',encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not row or not row[0].strip():
                    continue
                name = row[0].strip()
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

    print("Returning JSON:", audio_urls)
    return jsonify({"audios": audio_urls})



if __name__ == "__main__":
    app.run(debug=True)