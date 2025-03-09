"""
Statistical analysis of protein data.
"""
import os
import sys
import pandas as pd
import numpy as np
from collections import Counter

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.database.connection import get_session
from src.database.models import Protein, Chain, Residue, Author

class ProteinAnalyzer:
    """
    Analyze protein data from the database.
    """
    
    def __init__(self):
        """
        Initialize the protein analyzer.
        """
        self.session = get_session()
    
    def get_protein_dataframe(self):
        """
        Get a pandas DataFrame of all proteins in the database.
        
        Returns:
            DataFrame: Pandas DataFrame of proteins
        """
        # Query all proteins
        proteins = self.session.query(Protein).all()
        
        # Convert to DataFrame
        data = []
        for protein in proteins:
            data.append({
                'pdb_id': protein.pdb_id,
                'title': protein.title,
                'classification': protein.classification,
                'experimental_method': protein.experimental_method,
                'resolution': protein.resolution,
                'deposition_date': protein.deposition_date,
                'release_date': protein.release_date,
                'revision_date': protein.revision_date,
                'num_chains': len(protein.chains),
                'num_authors': len(protein.authors)
            })
        
        return pd.DataFrame(data)
    
    def get_chain_dataframe(self):
        """
        Get a pandas DataFrame of all chains in the database.
        
        Returns:
            DataFrame: Pandas DataFrame of chains
        """
        # Query all chains
        chains = self.session.query(Chain).all()
        
        # Convert to DataFrame
        data = []
        for chain in chains:
            data.append({
                'chain_id': chain.chain_id,
                'entity_id': chain.entity_id,
                'length': chain.length,
                'type': chain.type,
                'protein_id': chain.protein_id,
                'pdb_id': chain.protein.pdb_id if chain.protein else None
            })
        
        return pd.DataFrame(data)
    
    def get_residue_dataframe(self):
        """
        Get a pandas DataFrame of all residues in the database.
        
        Returns:
            DataFrame: Pandas DataFrame of residues
        """
        # This could be a large dataset, so we'll use a more efficient approach
        # Query residues in batches
        batch_size = 10000
        offset = 0
        all_data = []
        
        while True:
            residues = self.session.query(
                Residue.id, 
                Residue.residue_number, 
                Residue.residue_name, 
                Residue.secondary_structure,
                Residue.chain_id,
                Chain.protein_id,
                Chain.chain_id.label('chain_identifier')
            ).join(Chain).limit(batch_size).offset(offset).all()
            
            if not residues:
                break
                
            # Convert to list of dicts
            batch_data = [
                {
                    'id': r.id,
                    'residue_number': r.residue_number,
                    'residue_name': r.residue_name,
                    'secondary_structure': r.secondary_structure,
                    'chain_id': r.chain_id,
                    'protein_id': r.protein_id,
                    'chain_identifier': r.chain_identifier
                }
                for r in residues
            ]
            
            all_data.extend(batch_data)
            offset += batch_size
            
            # Break if we got less than a full batch
            if len(residues) < batch_size:
                break
        
        return pd.DataFrame(all_data)
    
    def analyze_resolution_distribution(self):
        """
        Analyze the distribution of protein resolution.
        
        Returns:
            dict: Statistical analysis results
        """
        df = self.get_protein_dataframe()
        
        # Filter out proteins with no resolution data
        resolution_df = df[df['resolution'].notna()]
        
        if len(resolution_df) == 0:
            return {
                'count': 0,
                'message': 'No resolution data available'
            }
        
        # Calculate statistics
        stats = {
            'count': len(resolution_df),
            'min': resolution_df['resolution'].min(),
            'max': resolution_df['resolution'].max(),
            'mean': resolution_df['resolution'].mean(),
            'median': resolution_df['resolution'].median(),
            'std': resolution_df['resolution'].std(),
            'percentiles': {
                '25%': np.percentile(resolution_df['resolution'], 25),
                '50%': np.percentile(resolution_df['resolution'], 50),
                '75%': np.percentile(resolution_df['resolution'], 75),
                '90%': np.percentile(resolution_df['resolution'], 90)
            }
        }
        
        return stats
    
    def analyze_chain_length_distribution(self):
        """
        Analyze the distribution of chain lengths.
        
        Returns:
            dict: Statistical analysis results
        """
        df = self.get_chain_dataframe()
        
        # Filter out chains with no length data
        length_df = df[df['length'].notna() & (df['length'] > 0)]
        
        if len(length_df) == 0:
            return {
                'count': 0,
                'message': 'No chain length data available'
            }
        
        # Calculate statistics
        stats = {
            'count': len(length_df),
            'min': length_df['length'].min(),
            'max': length_df['length'].max(),
            'mean': length_df['length'].mean(),
            'median': length_df['length'].median(),
            'std': length_df['length'].std(),
            'percentiles': {
                '25%': np.percentile(length_df['length'], 25),
                '50%': np.percentile(length_df['length'], 50),
                '75%': np.percentile(length_df['length'], 75),
                '90%': np.percentile(length_df['length'], 90)
            }
        }
        
        return stats
    
    def analyze_amino_acid_composition(self, limit=None):
        """
        Analyze the amino acid composition of proteins.
        
        Args:
            limit (int): Limit the number of residues to analyze
            
        Returns:
            dict: Amino acid composition statistics
        """
        # Query residues directly for efficiency
        query = self.session.query(Residue.residue_name)
        
        if limit:
            query = query.limit(limit)
            
        residues = query.all()
        
        if not residues:
            return {
                'count': 0,
                'message': 'No residue data available'
            }
        
        # Count amino acids
        aa_counter = Counter([r.residue_name for r in residues if r.residue_name])
        total_count = sum(aa_counter.values())
        
        # Calculate percentages
        aa_percentages = {aa: (count / total_count) * 100 for aa, count in aa_counter.items()}
        
        # Sort by frequency
        sorted_aa = sorted(aa_percentages.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'count': total_count,
            'frequencies': dict(sorted_aa),
            'top_5': dict(sorted_aa[:5])
        }
    
    def analyze_experimental_methods(self):
        """
        Analyze the distribution of experimental methods.
        
        Returns:
            dict: Experimental method statistics
        """
        df = self.get_protein_dataframe()
        
        # Count experimental methods
        method_counts = df['experimental_method'].value_counts().to_dict()
        total_count = sum(method_counts.values())
        
        # Calculate percentages
        method_percentages = {method: (count / total_count) * 100 for method, count in method_counts.items()}
        
        # Sort by frequency
        sorted_methods = sorted(method_percentages.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'count': total_count,
            'frequencies': dict(sorted_methods)
        }
    
    def analyze_deposition_years(self):
        """
        Analyze the distribution of deposition years.
        
        Returns:
            dict: Deposition year statistics
        """
        df = self.get_protein_dataframe()
        
        # Extract years from deposition dates
        df['deposition_year'] = df['deposition_date'].dt.year
        
        # Count years
        year_counts = df['deposition_year'].value_counts().sort_index().to_dict()
        
        return {
            'count': len(df),
            'year_counts': year_counts
        }
    
    def get_correlation_matrix(self):
        """
        Calculate correlation matrix between numerical protein properties.
        
        Returns:
            DataFrame: Correlation matrix
        """
        df = self.get_protein_dataframe()
        
        # Select numerical columns
        numerical_df = df.select_dtypes(include=[np.number])
        
        # Calculate correlation matrix
        corr_matrix = numerical_df.corr()
        
        return corr_matrix 