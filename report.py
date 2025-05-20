import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CSV_FOLDER = "csv_files"

# csv_files_names = ["Liste+d'actions+-+P7+Python+-+Feuille+1.csv", "dataset1_Python+P7.csv", "dataset2_Python+P7.csv"]
csv_file = "dataset1_Python+P7.csv"
# Chemin complet du fichier CSV
csv_file_path = os.path.join(CSV_FOLDER, csv_file)

# Charger les données
data = pd.read_csv(csv_file_path)  # Remplacez par le chemin de votre fichier

# Afficher les premières lignes du jeu de données
print("Premières lignes du jeu de données :")
print(data.head())

# Statistiques descriptives
print("\nStatistiques descriptives :")
print(data.describe())

# Visualisation de la distribution des variables numériques
data.hist(bins=30, figsize=(20, 15))
plt.suptitle("Distribution des variables numériques")
plt.show()

# Diagramme de boîte pour visualiser les valeurs aberrantes
plt.figure(figsize=(15, 10))
sns.boxplot(data=data.select_dtypes(include=['float64', 'int64']))
plt.title("Diagramme de boîte des variables numériques")
plt.xticks(rotation=45)
plt.show()

# Matrice de corrélation
correlation_matrix = data.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title("Matrice de corrélation")
plt.show()

# Analyse des valeurs manquantes
missing_values = data.isnull().sum()
print("\nValeurs manquantes par colonne :")
print(missing_values[missing_values > 0])

# Visualisation des valeurs manquantes
plt.figure(figsize=(10, 6))
sns.heatmap(data.isnull(), cbar=False, cmap='viridis')
plt.title("Valeurs manquantes dans le jeu de données")
plt.show()
