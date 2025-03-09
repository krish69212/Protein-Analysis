# Krish Parmar
#Protein Analysis Project

A data analysis pipeline that fetches protein data from the PDB (Protein Data Bank) API, stores it in a SQL database, and performs statistical analysis using NumPy and pandas.

## Features

- Fetch protein data from the PDB REST API
- Store structured protein data in a SQL database
- Perform statistical analysis on protein properties
- Generate visualizations of protein data distributions
- Extract insights about protein structures and properties

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your database configuration (see `.env.example`)
4. Run the initialization script:
   ```
   python src/initialize_db.py
   ```

## Usage

1. Fetch data from PDB:
   ```
   python src/fetch_pdb_data.py --query "your_query" --limit 100
   ```

2. Run analysis:
   ```
   python src/analyze_proteins.py --analysis_type "basic_stats"
   ```

3. Generate visualizations:
   ```
   python src/visualize_data.py --plot_type "distribution"
   ```

## Project Structure 

- `src/`: Source code
  - `api/`: PDB API interaction modules
  - `database/`: Database models and operations
  - `analysis/`: Statistical analysis modules
  - `visualization/`: Data visualization scripts
- `tests/`: Test cases
- `data/`: Data storage (gitignored)
- `notebooks/`: Jupyter notebooks for exploratory analysis
- `results/`: Analysis results and figures