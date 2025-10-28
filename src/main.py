"""
Enhanced version of main.py with database integration
This file demonstrates how to integrate the DatabaseManager with the existing application
"""

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os
import sys
import csv
from database_manager import DatabaseManager

def pronounce_text(elevenlabs_client, text) -> None:
    """
    Convert text to speech and play it
    """
    audio = elevenlabs_client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    play(audio)

def option_1_single_text(elevenlabs_client, db_manager):
    """
    Option 1: Given the user input, convert the text to speech and play it
    Enhanced with database logging
    """
    user_text = input("Please enter the text you want to convert to speech: ").strip()
    
    if not user_text:
        print("Error: No text provided.")
        return
    
    print(f"Pronouncing: '{user_text}'")
    pronounce_text(elevenlabs_client, user_text)
    
    # Log to database: Create driver record first, then single record with same ID
    try:
        driver_id = db_manager.insert_driver_record('single_text')
        single_id = db_manager.insert_single_record(driver_id, user_text)
        print(f"Logged to database with ID: {driver_id}")
    except Exception as e:
        print(f"Warning: Could not log to database: {e}")

def option_2_csv_names(elevenlabs_client, db_manager):
    """
    Option 2: Read names from CSV file and pronounce names one by one
    Enhanced with database logging
    """
    csv_file_path = input("Please enter the path to your CSV file containing names: ").strip()
    
    if not csv_file_path:
        print("Error: No CSV file path provided.")
        return
    
    # Check to see if the CSV file exists. If not, print an error message. 
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file '{csv_file_path}' does not exist.")
        return
    
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:

            sample = csvfile.read(1024)
            csvfile.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            
            reader = csv.reader(csvfile, delimiter=delimiter)
            
            # Check to see if the first row is header. 
            first_row = next(reader, None)
            if first_row is None:
                print("Error: CSV file is empty.")
                return
            
            # Ask user if first row is header
            print(f"First row: {first_row}")
            is_header = input("Is the first row a header? (y/n): ").strip().lower()
            
            names = []
            if is_header == 'y':
                for row in reader:
                    if row:  # Skip empty rows
                        names.extend([cell.strip() for cell in row if cell.strip()])
            else:
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
            
            # Log CSV upload to database: Create driver record first, then csv_upload with same ID
            try:
                csv_filename = os.path.basename(csv_file_path)
                driver_id = db_manager.insert_driver_record('csv_upload')
                csv_id = db_manager.insert_csv_upload_record(driver_id, csv_filename, names)
                print(f"Logged CSV upload to database with ID: {driver_id}")
            except Exception as e:
                print(f"Warning: Could not log CSV upload to database: {e}")
            
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

def option_3_view_database(db_manager):
    """
    Option 3: View database statistics and recent records
    """
    try:
        print("\n=== Database Statistics ===")
        tables_info = db_manager.get_all_tables_info()
        print(tables_info['summary'])
        
        print("\n=== Recent Driver Records (All Operations) ===")
        driver_records = tables_info['driver_sample']
        if not driver_records.empty:
            print(driver_records.to_string(index=False))
        else:
            print("No driver records found.")
        
        print("\n=== Single Text Operations (with JOIN) ===")
        try:
            single_ops = db_manager.get_single_operations_with_details(limit=3)
            if not single_ops.empty:
                print(single_ops.to_string(index=False))
            else:
                print("No single text operations found.")
        except Exception as e:
            print(f"Could not retrieve single operations: {e}")
        
        print("\n=== CSV Upload Operations (with JOIN) ===")
        try:
            csv_ops = db_manager.get_csv_operations_with_details(limit=3)
            if not csv_ops.empty:
                # Display without full JSON contents for readability
                display_cols = ['id', 'feature', 'operation_time', 'filename']
                available_cols = [col for col in display_cols if col in csv_ops.columns]
                print(csv_ops[available_cols].to_string(index=False))
            else:
                print("No CSV upload operations found.")
        except Exception as e:
            print(f"Could not retrieve CSV operations: {e}")
        
        print("\n--- Schema Info ---")
        print("Note: Driver.id is the primary key, shared by Single and CSV_Upload as foreign keys")
        print("Each operation creates a Driver record + either Single or CSV_Upload record with the same ID")
            
    except Exception as e:
        print(f"Error retrieving database information: {e}")

if __name__ == "__main__":
    
    load_dotenv()
    
    # Initialize ElevenLabs client
    elevenlabs = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
    )
    
    # Initialize Database Manager
    try:
        db_manager = DatabaseManager()
        if not db_manager.test_connection():
            print("Warning: Database connection failed. Application will continue without database logging.")
            db_manager = None
    except Exception as e:
        print(f"Warning: Could not initialize database: {e}")
        print("Application will continue without database logging.")
        db_manager = None
    
    print("=== Name Pronunciation CLI (Enhanced with Database) ===")
    print("Choose an option:")
    print("1. Enter text to pronounce")
    print("2. Upload CSV file with names to pronounce")
    if db_manager:
        print("3. View database statistics")
    print("4. Exit")
    
    while True:
        choice = input(f"\nEnter your choice (1-{4 if db_manager else 2}): ").strip()
        
        if choice == "1":
            option_1_single_text(elevenlabs, db_manager)
        elif choice == "2":
            option_2_csv_names(elevenlabs, db_manager)
        elif choice == "3" and db_manager:
            option_3_view_database(db_manager)
        elif choice == "4":
            print("Goodbye!")
            if db_manager:
                db_manager.close_connection()
            break
        else:
            valid_choices = "1, 2" + (", 3" if db_manager else "") + ", 4"
            print(f"Invalid choice. Please enter: {valid_choices}")
