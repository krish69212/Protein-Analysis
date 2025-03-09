"""
PDB API client for fetching protein data.
"""
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PDBClient:
    """
    Client for interacting with the PDB (Protein Data Bank) API.
    """
    
    def __init__(self):
        """
        Initialize the PDB API client.
        """
        self.base_url = os.getenv('PDB_API_BASE_URL', 'https://data.rcsb.org/rest/v1/core')
        self.search_url = os.getenv('PDB_SEARCH_URL', 'https://search.rcsb.org/rcsbsearch/v2/query')
    
    def search_proteins(self, query=None, limit=10):
        """
        Search for proteins in the PDB database.
        
        Args:
            query (str): Search query (e.g., "hemoglobin")
            limit (int): Maximum number of results to return
            
        Returns:
            list: List of PDB IDs matching the search criteria
        """
        if query:
            # Text search query
            payload = {
                "query": {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "value": query
                    }
                },
                "return_type": "entry",
                "request_options": {
                    "pager": {
                        "start": 0,
                        "rows": limit
                    }
                }
            }
        else:
            # Default query to get recent structures
            payload = {
                "query": {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_accession_info.deposit_date",
                        "operator": "greater_or_equal",
                        "value": (datetime.now().year - 1)
                    }
                },
                "return_type": "entry",
                "request_options": {
                    "pager": {
                        "start": 0,
                        "rows": limit
                    },
                    "sort": [
                        {
                            "sort_by": "rcsb_accession_info.deposit_date",
                            "direction": "desc"
                        }
                    ]
                }
            }
        
        try:
            response = requests.post(self.search_url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            pdb_ids = [hit['identifier'] for hit in result.get('result_set', [])]
            
            return pdb_ids
        except requests.exceptions.RequestException as e:
            print(f"Error searching PDB: {e}")
            return []
    
    def get_protein_data(self, pdb_id):
        """
        Get detailed data for a specific protein.
        
        Args:
            pdb_id (str): PDB ID of the protein
            
        Returns:
            dict: Protein data
        """
        try:
            # Get entry data
            entry_url = f"{self.base_url}/entry/{pdb_id}"
            entry_response = requests.get(entry_url)
            entry_response.raise_for_status()
            entry_data = entry_response.json()
            
            # Get polymer entity data
            entity_data = {}
            for entity_id in self._get_entity_ids(entry_data):
                entity_url = f"{self.base_url}/polymer_entity/{pdb_id}/{entity_id}"
                entity_response = requests.get(entity_url)
                if entity_response.status_code == 200:
                    entity_data[entity_id] = entity_response.json()
            
            # Combine data
            result = {
                'entry': entry_data,
                'entities': entity_data
            }
            
            return result
        except requests.exceptions.RequestException as e:
            print(f"Error fetching protein data for {pdb_id}: {e}")
            return None
    
    def _get_entity_ids(self, entry_data):
        """
        Extract entity IDs from entry data.
        
        Args:
            entry_data (dict): Entry data from PDB API
            
        Returns:
            list: List of entity IDs
        """
        try:
            entity_ids = []
            if 'rcsb_entry_container_identifiers' in entry_data:
                identifiers = entry_data['rcsb_entry_container_identifiers']
                if 'polymer_entity_ids' in identifiers:
                    entity_ids = identifiers['polymer_entity_ids']
            return entity_ids
        except Exception as e:
            print(f"Error extracting entity IDs: {e}")
            return [] 