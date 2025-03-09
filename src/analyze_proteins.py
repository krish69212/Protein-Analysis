"""
Run statistical analysis on protein data.
"""
import os
import sys
import argparse
import json
import pandas as pd
import numpy as np

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis.statistics import ProteinAnalyzer

def run_analysis(analysis_type=None, output_format='json'):
    """
    Run statistical analysis on protein data.
    
    Args:
        analysis_type (str): Type of analysis to run
        output_format (str): Output format ('json' or 'csv')
    """
    # Initialize analyzer
    analyzer = ProteinAnalyzer()
    
    # Check if we have data
    proteins_df = analyzer.get_protein_dataframe()
    if len(proteins_df) == 0:
        print("No protein data found in the database. Please fetch data first.")
        return
    
    print(f"Found {len(proteins_df)} proteins in the database")
    
    # Create results directory if it doesn't exist
    results_dir = os.getenv('RESULTS_DIR', './results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Run the specified analysis or all analyses
    if analysis_type == 'basic_stats' or analysis_type is None:
        print("Running basic statistics analysis...")
        
        # Get basic statistics
        resolution_stats = analyzer.analyze_resolution_distribution()
        chain_length_stats = analyzer.analyze_chain_length_distribution()
        
        # Save results
        results = {
            'resolution_stats': resolution_stats,
            'chain_length_stats': chain_length_stats
        }
        
        save_results(results, 'basic_stats', output_format, results_dir)
    
    if analysis_type == 'amino_acid_composition' or analysis_type is None:
        print("Running amino acid composition analysis...")
        
        # Get amino acid composition
        aa_composition = analyzer.analyze_amino_acid_composition()
        
        # Save results
        save_results(aa_composition, 'amino_acid_composition', output_format, results_dir)
    
    if analysis_type == 'experimental_methods' or analysis_type is None:
        print("Running experimental methods analysis...")
        
        # Get experimental methods distribution
        exp_methods = analyzer.analyze_experimental_methods()
        
        # Save results
        save_results(exp_methods, 'experimental_methods', output_format, results_dir)
    
    if analysis_type == 'deposition_years' or analysis_type is None:
        print("Running deposition years analysis...")
        
        # Get deposition years distribution
        deposition_years = analyzer.analyze_deposition_years()
        
        # Save results
        save_results(deposition_years, 'deposition_years', output_format, results_dir)
    
    if analysis_type == 'correlation_matrix' or analysis_type is None:
        print("Running correlation analysis...")
        
        # Get correlation matrix
        corr_matrix = analyzer.get_correlation_matrix()
        
        # Save results
        if output_format == 'json':
            # Convert DataFrame to dict for JSON serialization
            corr_dict = corr_matrix.to_dict(orient='split')
            save_results(corr_dict, 'correlation_matrix', output_format, results_dir)
        else:
            # Save as CSV
            output_path = os.path.join(results_dir, f'correlation_matrix.csv')
            corr_matrix.to_csv(output_path)
            print(f"Saved correlation matrix to {output_path}")
    
    print("Analysis complete")

def save_results(results, analysis_name, output_format, results_dir):
    """
    Save analysis results to a file.
    
    Args:
        results: Analysis results
        analysis_name (str): Name of the analysis
        output_format (str): Output format ('json' or 'csv')
        results_dir (str): Directory to save results
    """
    if output_format == 'json':
        # Save as JSON
        output_path = os.path.join(results_dir, f'{analysis_name}.json')
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Saved {analysis_name} results to {output_path}")
    elif output_format == 'csv':
        # Convert to DataFrame and save as CSV
        output_path = os.path.join(results_dir, f'{analysis_name}.csv')
        
        # Handle different result types
        if isinstance(results, dict):
            # Try to convert dict to DataFrame
            try:
                df = pd.DataFrame.from_dict(results, orient='index')
                df.to_csv(output_path)
                print(f"Saved {analysis_name} results to {output_path}")
            except Exception as e:
                print(f"Could not save {analysis_name} as CSV: {e}")
                # Fallback to JSON
                fallback_path = os.path.join(results_dir, f'{analysis_name}.json')
                with open(fallback_path, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                print(f"Saved {analysis_name} results to {fallback_path} as JSON instead")
        elif isinstance(results, pd.DataFrame):
            # Save DataFrame directly
            results.to_csv(output_path)
            print(f"Saved {analysis_name} results to {output_path}")
        else:
            print(f"Could not save {analysis_name} as CSV: unsupported result type")
            # Fallback to JSON
            fallback_path = os.path.join(results_dir, f'{analysis_name}.json')
            with open(fallback_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"Saved {analysis_name} results to {fallback_path} as JSON instead")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run statistical analysis on protein data")
    parser.add_argument("--analysis_type", type=str, choices=[
        'basic_stats', 
        'amino_acid_composition', 
        'experimental_methods', 
        'deposition_years', 
        'correlation_matrix'
    ], help="Type of analysis to run (default: all)")
    parser.add_argument("--output_format", type=str, choices=['json', 'csv'], default='json', 
                        help="Output format (default: json)")
    args = parser.parse_args()
    
    run_analysis(analysis_type=args.analysis_type, output_format=args.output_format) 