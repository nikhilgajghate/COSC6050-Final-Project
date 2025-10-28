"""
Database Manager for Name Pronunciation CLI
This module provides functions to interact with PostgreSQL database using pandas
"""

import pandas as pd
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
import sqlalchemy
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseManager:
    """
    A class to manage database operations for the Name Pronunciation CLI application.
    Uses pandas for data operations and SQLAlchemy for database connections.
    """
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize the DatabaseManager with a database connection.
        
        Args:
            connection_string (str, optional): PostgreSQL connection string.
                If not provided, will try to build from environment variables.
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
        """Establish database connection."""
        try:
            self.engine = create_engine(self.connection_string)
            # Test the connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database connection established successfully.")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test if database connection is working."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                return True
        except Exception as e:
            print(f"Database connection test failed: {e}")
            return False
    
    # Driver table operations
    def insert_driver_record(self, feature: str, custom_datetime: Optional[datetime] = None) -> str:
        """
        Insert a record into the Driver table.
        
        Args:
            feature (str): The text feature that was processed (e.g., 'single_text', 'csv_upload')
            custom_datetime (datetime, optional): Custom timestamp, defaults to current time
            
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
        Retrieve driver records as a pandas DataFrame.
        
        Args:
            limit (int, optional): Maximum number of records to retrieve
            
        Returns:
            pd.DataFrame: Driver records
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
        Insert a record into the Single table.
        
        Args:
            driver_id (str): The UUID from the Driver table (foreign key)
            input_text (str): The user input text
            custom_datetime (datetime, optional): Custom timestamp, defaults to current time
            
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
        Retrieve single records as a pandas DataFrame.
        
        Args:
            limit (int, optional): Maximum number of records to retrieve
            
        Returns:
            pd.DataFrame: Single records
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
    def insert_csv_upload_record(self, driver_id: str, filename: str, contents: List[str], 
                               custom_datetime: Optional[datetime] = None) -> str:
        """
        Insert a record into the CSV_Upload table.
        
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
        Retrieve CSV upload records as a pandas DataFrame.
        
        Args:
            limit (int, optional): Maximum number of records to retrieve
            
        Returns:
            pd.DataFrame: CSV upload records
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
    
    # Query functions with joins
    def get_single_operations_with_details(self, limit: Optional[int] = None) -> pd.DataFrame:
        """
        Get all single text operations joined with their driver records.
        
        Args:
            limit (int, optional): Maximum number of records to retrieve
            
        Returns:
            pd.DataFrame: Joined driver and single records
        """
        try:
            query = """
                SELECT 
                    d.id,
                    d.feature,
                    d.datetime as operation_time,
                    s.input as user_input
                FROM driver d
                INNER JOIN single s ON d.id = s.id
                ORDER BY d.datetime DESC
            """
            if limit:
                query += f" LIMIT {limit}"
                
            df = pd.read_sql(query, self.engine)
            return df
            
        except Exception as e:
            print(f"Error retrieving single operations with details: {e}")
            raise
    
    def get_csv_operations_with_details(self, limit: Optional[int] = None) -> pd.DataFrame:
        """
        Get all CSV upload operations joined with their driver records.
        
        Args:
            limit (int, optional): Maximum number of records to retrieve
            
        Returns:
            pd.DataFrame: Joined driver and csv_upload records
        """
        try:
            query = """
                SELECT 
                    d.id,
                    d.feature,
                    d.datetime as operation_time,
                    c.filename,
                    c.contents
                FROM driver d
                INNER JOIN csv_upload c ON d.id = c.id
                ORDER BY d.datetime DESC
            """
            if limit:
                query += f" LIMIT {limit}"
                
            df = pd.read_sql(query, self.engine)
            return df
            
        except Exception as e:
            print(f"Error retrieving CSV operations with details: {e}")
            raise
    
    def get_operation_by_id(self, operation_id: str) -> pd.DataFrame:
        """
        Get a specific operation by ID with all details from related tables.
        
        Args:
            operation_id (str): The UUID of the operation
            
        Returns:
            pd.DataFrame: Complete operation details
        """
        try:
            query = """
                SELECT 
                    d.id,
                    d.feature,
                    d.datetime,
                    s.input,
                    c.filename,
                    c.contents
                FROM driver d
                LEFT JOIN single s ON d.id = s.id
                LEFT JOIN csv_upload c ON d.id = c.id
                WHERE d.id = :id
            """
            
            df = pd.read_sql(query, self.engine, params={'id': operation_id})
            return df
            
        except Exception as e:
            print(f"Error retrieving operation by ID: {e}")
            raise
    
    # Utility functions
    def get_all_tables_info(self) -> Dict[str, pd.DataFrame]:
        """
        Get information about all tables and their record counts.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary with table info
        """
        try:
            tables_info = {}
            
            # Get record counts
            with self.engine.connect() as conn:
                driver_count = conn.execute(text("SELECT COUNT(*) FROM driver")).fetchone()[0]
                single_count = conn.execute(text("SELECT COUNT(*) FROM single")).fetchone()[0]
                csv_count = conn.execute(text("SELECT COUNT(*) FROM csv_upload")).fetchone()[0]
            
            summary_data = {
                'Table': ['driver', 'single', 'csv_upload'],
                'Record_Count': [driver_count, single_count, csv_count]
            }
            
            tables_info['summary'] = pd.DataFrame(summary_data)
            tables_info['driver_sample'] = self.get_driver_records(limit=5)
            tables_info['single_sample'] = self.get_single_records(limit=5)
            tables_info['csv_upload_sample'] = self.get_csv_upload_records(limit=5)
            
            return tables_info
            
        except Exception as e:
            print(f"Error getting tables info: {e}")
            raise
    
    def close_connection(self):
        """Close the database connection."""
        if self.engine:
            self.engine.dispose()
            print("Database connection closed.")


# Example usage functions
def example_usage():
    """Example of how to use the DatabaseManager."""
    
    # Initialize database manager
    db = DatabaseManager()
    
    # Test connection
    if not db.test_connection():
        print("Cannot proceed without database connection")
        return
    
    # Insert sample data
    try:
        # Example 1: Insert a single text operation
        driver_id_1 = db.insert_driver_record("single_text")
        single_id = db.insert_single_record(driver_id_1, "User typed: Hello there!")
        
        # Example 2: Insert a CSV upload operation
        driver_id_2 = db.insert_driver_record("csv_upload")
        csv_id = db.insert_csv_upload_record(
            driver_id_2,
            "names.csv", 
            ["John", "Jane", "Bob", "Alice"]
        )
        
        # Retrieve and display data
        print("\n=== Recent Driver Records ===")
        print(db.get_driver_records(limit=3))
        
        print("\n=== Recent Single Records ===")
        print(db.get_single_records(limit=3))
        
        print("\n=== Recent CSV Upload Records ===")
        print(db.get_csv_upload_records(limit=3))
        
        print("\n=== Tables Summary ===")
        tables_info = db.get_all_tables_info()
        print(tables_info['summary'])
        
    except Exception as e:
        print(f"Error during example usage: {e}")
    
    finally:
        # Always close connection
        db.close_connection()


if __name__ == "__main__":
    example_usage()
