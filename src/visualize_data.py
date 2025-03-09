"""
Generate visualizations from protein analysis results.
"""
import os
import sys
import argparse

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.visualization.plots import ProteinVisualizer

def generate_visualizations(plot_type=None):
    """
    Generate visualizations from protein analysis results.
    
    Args:
        plot_type (str): Type of plot to generate
    """
    # Initialize visualizer
    visualizer = ProteinVisualizer()
    
    # Generate the specified plot or all plots
    if plot_type == 'resolution' or plot_type is None:
        print("Generating resolution distribution plot...")
        visualizer.plot_resolution_distribution()
    
    if plot_type == 'chain_length' or plot_type is None:
        print("Generating chain length distribution plot...")
        visualizer.plot_chain_length_distribution()
    
    if plot_type == 'amino_acid' or plot_type is None:
        print("Generating amino acid composition plot...")
        visualizer.plot_amino_acid_composition()
    
    if plot_type == 'experimental_methods' or plot_type is None:
        print("Generating experimental methods plot...")
        visualizer.plot_experimental_methods()
    
    if plot_type == 'deposition_years' or plot_type is None:
        print("Generating deposition years plot...")
        visualizer.plot_deposition_years()
    
    if plot_type == 'correlation' or plot_type is None:
        print("Generating correlation matrix plot...")
        visualizer.plot_correlation_matrix()
    
    print("Visualization generation complete")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate visualizations from protein analysis results")
    parser.add_argument("--plot_type", type=str, choices=[
        'resolution', 
        'chain_length', 
        'amino_acid', 
        'experimental_methods', 
        'deposition_years', 
        'correlation'
    ], help="Type of plot to generate (default: all)")
    args = parser.parse_args()
    
    generate_visualizations(plot_type=args.plot_type) 