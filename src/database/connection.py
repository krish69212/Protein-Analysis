"""
Database connection utilities for the Protein Analysis project.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_connection_string():
    """
    Get the database connection string from environment variables.
    
    Returns:
        str: Database connection string
    """
    db_type = os.getenv('DB_TYPE', 'sqlite')
    db_name = os.getenv('DB_NAME', 'protein_analysis.db')
    
    if db_type.lower() == 'sqlite':
        # SQLite connection
        data_dir = os.getenv('DATA_DIR', './data')
        db_path = os.path.join(data_dir, db_name)
        return f"sqlite:///{db_path}"
    
    # For other database types
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    
    if db_type.lower() == 'mysql':
        return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    elif db_type.lower() == 'postgresql':
        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def get_engine():
    """
    Create and return a SQLAlchemy engine.
    
    Returns:
        Engine: SQLAlchemy engine
    """
    connection_string = get_connection_string()
    return create_engine(connection_string, echo=False)


def get_session():
    """
    Create and return a SQLAlchemy session.
    
    Returns:
        Session: SQLAlchemy session
    """
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session() 