import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the file path for the dataset
file_path = r"C:\Users\Krish\Documents\GitHub\Protein-Analysis-1\rcsb_statistical_data_enhanced.xlsx"

# Load the dataset and handle potential file errors
try:
    df = pd.read_excel(file_path)
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print(f"Error: The file was not found at {file_path}. Please verify the path.")
    exit()

# Display basic statistical summaries of the dataset
print(df.describe())

# Ensure the 'Molecular Weight' column is numeric before plotting a histogram
if 'Molecular Weight' in df.columns and pd.api.types.is_numeric_dtype(df['Molecular Weight']):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Molecular Weight'].dropna(), bins=30, kde=True)
    plt.title('Distribution of Molecular Weights')
    plt.xlabel('Molecular Weight')
    plt.ylabel('Frequency')
    plt.show()
else:
    print("Skipping histogram: 'Molecular Weight' column is non-numeric or missing.")

# Ensure the 'Resolution' column is numeric before generating a boxplot
if 'Resolution' in df.columns and pd.api.types.is_numeric_dtype(df['Resolution']):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df['Resolution'].dropna())
    plt.title('Boxplot of Resolution')
    plt.xlabel('Resolution')
    plt.show()
else:
    print("Skipping boxplot: 'Resolution' column is non-numeric or missing.")