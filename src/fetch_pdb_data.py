"""
Fetch protein data from the PDB API and store it in the database.
"""
import os
import sys
import argparse
import time

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.pdb_client import PDBClient
from src.api.data_processor import DataProcessor
from src.database.connection import get_session

def fetch_and_store_proteins(query=None, limit=10, delay=1):
    """
    Fetch protein data from the PDB API and store it in the database.
    
    Args:
        query (str): Search query (e.g., "hemoglobin")
        limit (int): Maximum number of proteins to fetch
        delay (float): Delay between API requests in seconds
    """
    # Initialize API client and data processor
    pdb_client = PDBClient()
    data_processor = DataProcessor()
    
    # Search for proteins
    print(f"Searching for proteins with query: {query or 'recent'}")
    pdb_ids = pdb_client.search_proteins(query=query, limit=limit)
    
    if not pdb_ids:
        print("No proteins found")
        return
    
    print(f"Found {len(pdb_ids)} proteins")
    
    # Fetch and process each protein
    for i, pdb_id in enumerate(pdb_ids):
        print(f"Processing protein {i+1}/{len(pdb_ids)}: {pdb_id}")
        
        # Fetch protein data
        protein_data = pdb_client.get_protein_data(pdb_id)
        
        if protein_data:
            # Process and store protein data
            data_processor.process_protein_data(protein_data)
        
        # Add delay to avoid overwhelming the API
        if i < len(pdb_ids) - 1 and delay > 0:
            time.sleep(delay)
    
    print("Finished processing proteins")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch protein data from the PDB API")
    parser.add_argument("--query", type=str, help="Search query (e.g., 'hemoglobin')")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of proteins to fetch")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between API requests in seconds")
    args = parser.parse_args()
    
    fetch_and_store_proteins(query=args.query, limit=args.limit, delay=args.delay) 