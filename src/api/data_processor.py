"""
Data processor for transforming PDB API data and storing it in the database.
"""
import os
import sys
from datetime import datetime

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.database.models import Protein, Chain, Residue, Author
from src.database.connection import get_session

class DataProcessor:
    """
    Process data from the PDB API and store it in the database.
    """
    
    def __init__(self):
        """
        Initialize the data processor.
        """
        self.session = get_session()
    
    def process_protein_data(self, pdb_data):
        """
        Process protein data from the PDB API and store it in the database.
        
        Args:
            pdb_data (dict): Protein data from the PDB API
            
        Returns:
            Protein: The created or updated Protein object
        """
        if not pdb_data or 'entry' not in pdb_data:
            print("Invalid protein data")
            return None
        
        entry_data = pdb_data['entry']
        
        # Extract basic protein information
        pdb_id = entry_data.get('rcsb_id', '')
        
        # Check if protein already exists in the database
        existing_protein = self.session.query(Protein).filter_by(pdb_id=pdb_id).first()
        if existing_protein:
            print(f"Protein {pdb_id} already exists in the database")
            return existing_protein
        
        # Create new protein record
        protein = Protein(
            pdb_id=pdb_id,
            title=self._get_nested_value(entry_data, ['struct', 'title'], ''),
            classification=self._get_nested_value(entry_data, ['struct', 'pdbx_descriptor'], ''),
            experimental_method=self._get_nested_value(entry_data, ['exptl', 'method'], ''),
            resolution=self._get_nested_value(entry_data, ['refine', 'ls_d_res_high'], None),
            deposition_date=self._parse_date(self._get_nested_value(entry_data, ['rcsb_accession_info', 'deposit_date'], '')),
            release_date=self._parse_date(self._get_nested_value(entry_data, ['rcsb_accession_info', 'initial_release_date'], '')),
            revision_date=self._parse_date(self._get_nested_value(entry_data, ['rcsb_accession_info', 'revision_date'], ''))
        )
        
        # Process authors
        self._process_authors(protein, entry_data)
        
        # Process chains and entities
        self._process_chains(protein, pdb_data)
        
        # Save to database
        self.session.add(protein)
        self.session.commit()
        
        print(f"Processed protein {pdb_id}")
        return protein
    
    def _process_authors(self, protein, entry_data):
        """
        Process author information and add to the protein.
        
        Args:
            protein (Protein): The protein object
            entry_data (dict): Entry data from the PDB API
        """
        authors_list = self._get_nested_value(entry_data, ['audit_author'], [])
        if not isinstance(authors_list, list):
            authors_list = [authors_list]
        
        for author_data in authors_list:
            if isinstance(author_data, dict):
                name = author_data.get('name', '')
                if name:
                    author = Author(
                        name=name,
                        institution=''  # Institution data might not be directly available
                    )
                    protein.authors.append(author)
    
    def _process_chains(self, protein, pdb_data):
        """
        Process chain and entity information and add to the protein.
        
        Args:
            protein (Protein): The protein object
            pdb_data (dict): Protein data from the PDB API
        """
        entities_data = pdb_data.get('entities', {})
        
        for entity_id, entity_data in entities_data.items():
            # Extract sequence
            sequence = self._get_nested_value(entity_data, ['entity_poly', 'pdbx_seq_one_letter_code'], '')
            
            # Extract chain IDs for this entity
            chain_ids = self._get_nested_value(entity_data, ['rcsb_polymer_entity_container_identifiers', 'auth_asym_ids'], [])
            if not isinstance(chain_ids, list):
                chain_ids = [chain_ids]
            
            # Entity type
            entity_type = self._get_nested_value(entity_data, ['entity_poly', 'type'], '')
            
            # Create chain records
            for chain_id in chain_ids:
                chain = Chain(
                    chain_id=chain_id,
                    entity_id=entity_id,
                    sequence=sequence,
                    length=len(sequence) if sequence else 0,
                    type=entity_type
                )
                protein.chains.append(chain)
                
                # Process residues (simplified - in a real application, you might want to get more detailed residue data)
                if sequence:
                    for i, residue in enumerate(sequence):
                        if residue != ' ':  # Skip spaces in the sequence
                            residue_obj = Residue(
                                residue_number=i + 1,
                                residue_name=residue,
                                secondary_structure=''  # Would require additional API calls to get this data
                            )
                            chain.residues.append(residue_obj)
    
    def _get_nested_value(self, data, keys, default=None):
        """
        Safely get a nested value from a dictionary.
        
        Args:
            data (dict): The dictionary to extract from
            keys (list): List of keys to traverse
            default: Default value to return if the path doesn't exist
            
        Returns:
            The value at the specified path, or the default value
        """
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    
    def _parse_date(self, date_str):
        """
        Parse a date string from the PDB API.
        
        Args:
            date_str (str): Date string in format YYYY-MM-DD
            
        Returns:
            datetime: Parsed datetime object, or None if parsing fails
        """
        if not date_str:
            return None
        
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return None 