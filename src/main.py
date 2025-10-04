from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os
import sys
import csv

def pronounce_text(elevenlabs_client, text):
    """Convert text to speech and play it"""
    audio = elevenlabs_client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    play(audio)

def option_1_single_text(elevenlabs_client):
    """Option 1: Get single text input and pronounce it"""
    user_text = input("Please enter the text you want to convert to speech: ").strip()
    
    if not user_text:
        print("Error: No text provided.")
        return
    
    print(f"Pronouncing: '{user_text}'")
    pronounce_text(elevenlabs_client, user_text)

def option_2_csv_names(elevenlabs_client):
    """Option 2: Read names from CSV file and pronounce each one"""
    csv_file_path = input("Please enter the path to your CSV file containing names: ").strip()
    
    if not csv_file_path:
        print("Error: No CSV file path provided.")
        return
    
    # Validate that the CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file '{csv_file_path}' does not exist.")
        return
    
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            # Try to detect the delimiter
            sample = csvfile.read(1024)
            csvfile.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            
            reader = csv.reader(csvfile, delimiter=delimiter)
            
            # Skip header if it exists (optional)
            first_row = next(reader, None)
            if first_row is None:
                print("Error: CSV file is empty.")
                return
            
            # Ask user if first row is header
            print(f"First row: {first_row}")
            is_header = input("Is the first row a header? (y/n): ").strip().lower()
            
            names = []
            if is_header == 'y':
                # Skip header, continue with remaining rows
                for row in reader:
                    if row:  # Skip empty rows
                        names.extend([cell.strip() for cell in row if cell.strip()])
            else:
                # Include first row
                names.extend([cell.strip() for cell in first_row if cell.strip()])
                for row in reader:
                    if row:  # Skip empty rows
                        names.extend([cell.strip() for cell in row if cell.strip()])
            
            if not names:
                print("Error: No names found in the CSV file.")
                return
            
            print(f"Found {len(names)} names to pronounce:")
            for i, name in enumerate(names, 1):
                print(f"{i}. {name}")
            
            print("\nStarting pronunciation...")
            for i, name in enumerate(names, 1):
                print(f"Pronouncing ({i}/{len(names)}): {name}")
                pronounce_text(elevenlabs_client, name)
                
                # Add a small pause between names
                if i < len(names):
                    input("Press Enter to continue to the next name...")
            
            print("Finished pronouncing all names!")
            
    except Exception as e:
        print(f"Error reading CSV file: {e}")

if __name__ == "__main__":
    
    load_dotenv()
    
    # Initialize ElevenLabs client
    elevenlabs = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
    )
    
    print("=== Name Pronunciation CLI ===")
    print("Choose an option:")
    print("1. Enter text to pronounce")
    print("2. Upload CSV file with names to pronounce")
    
    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        
        if choice == "1":
            option_1_single_text(elevenlabs)
            # break
        elif choice == "2":
            option_2_csv_names(elevenlabs)
            # break
        else:
            print("Invalid choice. Please enter 1 or 2.")