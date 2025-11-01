# COSC6050-Final-Project
This repository contains code for the final project for the class COSC 6050: Elements of Software Development. 

**Godsfavour-dev**
I created a Backend and Frontend directory for the project.
-The Backend folder contains:
    - app.py – the main Flask application file. 
    - iteration1.py – handles the ElevenLabs API logic for generating pronunciation audio.
-The Frontend folder contains:
    - templates/index.html – the main webpage.
	- static/ – all supporting files like CSS, JavaScript, and audio files.

You'll need to run the application from app.py and open Chrome browser and go to http://127.0.0.1:5000
The app allows you to enter a name to pronounce or upload a CSV file with multiple names.

NB: The upload and pronunciation feature works perfectly on Chrome but on Safari, it uploads successfully but does not play audio output.
    i am thinking it's due to Safari's built-in restriction on autoplaying audio.