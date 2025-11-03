from pathlib import Path
import sys

# Add parent directory to path to import database_manager
sys.path.insert(0, str(Path(__file__).parent.parent))
from database_manager import DatabaseManager



# Initialize database manager (will be None if database is not set up)
db_manager = None

def get_db():
    """Get or initialize database manager."""
    global db_manager
    if db_manager is None:
        try:
            db_manager = DatabaseManager()
            print("✅ Database connection established")
        except Exception as e:
            print(f"⚠️  Database not available: {e}")
            print("   The app will continue without database logging.")
            db_manager = False  # Set to False to indicate we tried and failed
    return db_manager if db_manager is not False else None
