from typing import Optional, Dict, Any, List
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import sqlalchemy
import json
import os

# Load environment variables to get access to .env variables. 
load_dotenv()

class DatabaseManager:
    """
    This class facilitates CRUD operations to the database. 
    """
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        Database Manager constructor: Initializes the database connection.
        
        Args:
            connection_string (str, optional): PostgreSQL connection string.
            Default variables are defined. 
        """
        if connection_string:
            self.connection_string = connection_string
        else:
            # Build connection string from environment variables
            db_host = os.getenv('DB_HOST', 'localhost')
            db_port = os.getenv('DB_PORT', '5432')
            db_name = os.getenv('DB_NAME', 'name_pronunciation')
            db_user = os.getenv('DB_USER', 'postgres')
            db_password = os.getenv('DB_PASSWORD', 'password')
            
            self.connection_string = (
                f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            )
        
        self.engine = None
        self._connect()
    
    def _connect(self):
        """
        Establish database connection.
        """
        try:
            # Create the engine to connect to the database
            self.engine = create_engine(self.connection_string)

            # Test the connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database connection established successfully.")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test if database connection is working.
        Returns: 
            boolean: True if the connection was successful, else False. 
        """
        try:
            with self.engine.connect() as conn:
                # Run a test query to ensure that we are connected to the DB
                result = conn.execute(text("SELECT 1"))
                return True
        except Exception as e:
            print(f"Database connection test failed: {e}")
            return False
    
    # Driver table operations
    def insert_driver_record(self, feature: str, custom_datetime: Optional[datetime] = None) -> str:
        """
        Function to insert a record into the driver table. 
        
        Args:
            feature (str): The feature opted in by the user, i.e., single text vs. CSV upload
            custom_datetime (datetime, optional): Current timestamp.            
        Returns:
            str: The UUID of the inserted record
        """
        try:
            # Insert with RETURNING clause to get the generated ID
            with self.engine.connect() as conn:
                if custom_datetime:
                    result = conn.execute(text(
                        "INSERT INTO driver (feature, datetime) VALUES (:feature, :datetime) RETURNING id"
                    ), {'feature': feature, 'datetime': custom_datetime})
                else:
                    result = conn.execute(text(
                        "INSERT INTO driver (feature) VALUES (:feature) RETURNING id"
                    ), {'feature': feature})
                
                conn.commit()
                record_id = result.fetchone()[0]
                
            return str(record_id)
            
        except Exception as e:
            print(f"Error inserting driver record: {e}")
            raise
    
    def get_driver_records(self, limit: Optional[int] = None) -> pd.DataFrame:
        """
        Helper function to retrieve driver records from the database. 
        
        Args:
            limit (int, optional): Maximum number of records to retrieve
            
        Returns:
            pd.DataFrame: Records from the driver table. 
        """
        try:
            query = "SELECT * FROM driver ORDER BY datetime DESC"
            if limit:
                query += f" LIMIT {limit}"
                
            df = pd.read_sql(query, self.engine)
            return df
            
        except Exception as e:
            print(f"Error retrieving driver records: {e}")
            raise
    
    # Single table operations
    def insert_single_record(self, driver_id: str, input_text: str, custom_datetime: Optional[datetime] = None) -> str:
        """
        Function to insert a record into the single table. 
        
        Args:
            driver_id (str): The UUID from the Driver table (foreign key)
            input_text (str): The user input text
            custom_datetime (datetime, optional): Current timestamp.
            
        Returns:
            str: The UUID of the inserted record (same as driver_id)
        """
        try:
            # Insert with the provided driver_id
            with self.engine.connect() as conn:
                if custom_datetime:
                    conn.execute(text(
                        "INSERT INTO single (id, input, datetime) VALUES (:id, :input, :datetime)"
                    ), {'id': driver_id, 'input': input_text, 'datetime': custom_datetime})
                else:
                    conn.execute(text(
                        "INSERT INTO single (id, input) VALUES (:id, :input)"
                    ), {'id': driver_id, 'input': input_text})
                
                conn.commit()
                
            return driver_id
            
        except Exception as e:
            print(f"Error inserting single record: {e}")
            raise
    
    def get_single_records(self, limit: Optional[int] = None) -> pd.DataFrame:
        """
        Helper function to retrieve single records
        
        Args:
            limit (int, optional): Maximum number of records to retrieve
            
        Returns:
            pd.DataFrame: Records from the single table.
        """
        try:
            query = "SELECT * FROM single ORDER BY datetime DESC"
            if limit:
                query += f" LIMIT {limit}"
                
            df = pd.read_sql(query, self.engine)
            return df
            
        except Exception as e:
            print(f"Error retrieving single records: {e}")
            raise
    
    # CSV_Upload table operations
    def insert_csv_upload_record(self, driver_id: str, filename: str, 
        contents: List[str], custom_datetime: Optional[datetime] = None) -> str:
        """
        Function to insert a record into the csv_upload table
        
        Args:
            driver_id (str): The UUID from the Driver table (foreign key)
            filename (str): The name of the CSV file
            contents (List[str]): List of names/content from the CSV
            custom_datetime (datetime, optional): Custom timestamp, defaults to current time
            
        Returns:
            str: The UUID of the inserted record (same as driver_id)
        """
        try:
            # Convert contents to JSON
            contents_json = json.dumps({
                'names': contents,
                'count': len(contents)
            })
            
            # Insert with the provided driver_id
            with self.engine.connect() as conn:
                if custom_datetime:
                    conn.execute(text(
                        "INSERT INTO csv_upload (id, filename, contents, datetime) VALUES (:id, :filename, CAST(:contents AS jsonb), :datetime)"
                    ), {'id': driver_id, 'filename': filename, 'contents': contents_json, 'datetime': custom_datetime})
                else:
                    conn.execute(text(
                        "INSERT INTO csv_upload (id, filename, contents) VALUES (:id, :filename, CAST(:contents AS jsonb))"
                    ), {'id': driver_id, 'filename': filename, 'contents': contents_json})
                
                conn.commit()
                
            print(f"CSV upload record inserted with ID: {driver_id}")
            return driver_id
            
        except Exception as e:
            print(f"Error inserting CSV upload record: {e}")
            raise
    
    def get_csv_upload_records(self, limit: Optional[int] = None) -> pd.DataFrame:
        """
        Helper function to retrieve CSV upload records
        
        Args:
            limit (int, optional): Maximum number of records to retrieve
            
        Returns:
            pd.DataFrame: Records from the CSV Upload table. 
        """
        try:
            query = "SELECT * FROM csv_upload ORDER BY datetime DESC"
            if limit:
                query += f" LIMIT {limit}"
                
            df = pd.read_sql(query, self.engine)
            return df
            
        except Exception as e:
            print(f"Error retrieving CSV upload records: {e}")
            raise
    
    def close_connection(self):
        """
        Close the database connection.
        """
        if self.engine:
            self.engine.dispose()
            print("Database connection closed.")