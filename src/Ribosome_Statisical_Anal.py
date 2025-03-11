import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the file path for the dataset
df = pd.read_excel("C:\\Users\\Krish\\Documents\\GitHub\\Protein-Analysis-1\\rcsb_statistical_data_enhanced.xlsx")

# Display basic statistical summaries of the dataset
print(df.describe())

# Convert the 'Release Date' column to datetime format
df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')

plt.figure(figsize=(10, 6))
sns.histplot(df['Molecular Weight'].dropna(), bins=30, kde=True)
plt.title('Distribution of Molecular Weights')
plt.xlabel('Molecular Weight')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x=df['Resolution'].dropna())
plt.title('Boxplot of Resolution')
plt.xlabel('Resolution')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(df['Resolution'].dropna(), bins=30, kde=True)
plt.title('Distribution of Resolution')
plt.xlabel('Resolution')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(df['Release Date'].dropna(), bins=30, kde=False)
plt.title('Distribution of Release Dates')
plt.xlabel('Release Date')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.show()