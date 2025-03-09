# Ribosome Structure Analysis

This project uses PyPDB to search for ribosome structures in the Protein Data Bank (PDB) and perform statistical analysis on the results.

## Features

- Search for ribosome structures in the PDB
- Retrieve detailed information about each structure
- Perform statistical analysis on resolution, experimental methods, organisms, and release dates
- Generate visualizations of the data
- Save raw data to CSV for further analysis

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Basic Analysis

Run the basic analysis script:
```
python ribosome_analysis.py
```

The script will:
1. Search for ribosome structures in the PDB
2. Fetch detailed information about each structure
3. Perform statistical analysis on the data
4. Generate visualizations
5. Save the raw data to a CSV file

### Advanced Analysis

For more control over the search and analysis, use the advanced script:
```
python advanced_ribosome_analysis.py [options]
```

Available options:
- `--max_results N`: Maximum number of results to retrieve (default: 1000)
- `--max_resolution X`: Maximum resolution in Angstroms (lower is better)
- `--organism "Name"`: Filter by organism (e.g., "Escherichia coli")
- `--method "Method"`: Filter by experimental method (e.g., "X-RAY DIFFRACTION")
- `--year_from YYYY`: Filter by release year (from)
- `--year_to YYYY`: Filter by release year (to)
- `--output_csv filename.csv`: Output CSV file name (default: ribosome_data.csv)
- `--output_fig filename.png`: Output figure file name (default: ribosome_analysis.png)

Examples:
```
# Get high-resolution ribosome structures (3.0 Å or better)
python advanced_ribosome_analysis.py --max_resolution 3.0

# Get E. coli ribosome structures from 2010 onwards
python advanced_ribosome_analysis.py --organism "Escherichia coli" --year_from 2010

# Get ribosome structures determined by cryo-EM
python advanced_ribosome_analysis.py --method "ELECTRON MICROSCOPY"
```

## Output Files

- `ribosome_data.csv`: Raw data for all ribosome structures found
- `ribosome_analysis.png`: Visualizations of the statistical analysis

## Statistical Analysis

The script performs the following analyses:
- Basic statistics on the number of structures
- Resolution statistics (mean, median, min, max)
- Distribution of experimental methods
- Top 10 organisms with ribosome structures
- Number of structures released by year
- Correlation analysis between numerical properties

The advanced script additionally analyzes:
- Molecular weight statistics
- Atom count statistics
- Correlation between resolution and molecular weight
- More detailed visualizations

## Customization

You can modify the scripts to:
- Change the search criteria
- Add additional data fields to extract
- Perform different statistical analyses
- Create different visualizations

## Dependencies

- pypdb: Python API for the Protein Data Bank
- pandas: Data manipulation and analysis
- numpy: Numerical computing
- matplotlib: Data visualization
- seaborn: Statistical data visualization
- requests: HTTP library for API requests
- argparse: Command-line argument parsing