import pandas as pd

# Charger le fichier CSV
file_path = 'apple_scraping.csv'
df = pd.read_csv(file_path)

# Supprimer les lignes avec des valeurs manquantes dans la colonne 'text'
df_cleaned = df.dropna(subset=['text'])

# Sauvegarder le dataframe nettoyé dans un nouveau fichier CSV
cleaned_file_path = 'cleaned_apple_scraping.csv'
df_cleaned.to_csv(cleaned_file_path, index=False)

print(f"Fichier nettoyé sauvegardé sous: {cleaned_file_path}")
