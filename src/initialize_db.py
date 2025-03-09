"""
Initialize the database for the Protein Analysis project.
"""
import os
import argparse
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.connection import get_engine
from src.database.models import create_tables

def initialize_database(force=False):
    """
    Initialize the database by creating all tables.
    
    Args:
        force (bool): If True, will recreate the database if it already exists
    """
    # Create data directory if it doesn't exist
    data_dir = os.getenv('DATA_DIR', './data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Get database engine
    engine = get_engine()
    
    # Create tables
    create_tables(engine)
    
    print("Database initialized successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize the database for Protein Analysis")
    parser.add_argument("--force", action="store_true", help="Force recreation of the database")
    args = parser.parse_args()
    
    initialize_database(force=args.force) 