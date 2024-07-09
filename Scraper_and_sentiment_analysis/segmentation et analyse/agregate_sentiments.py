import pandas as pd
import logging

# Configuration du logger
logging.basicConfig(
    filename='aggregate_sentiment.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Charger les articles initiaux et les segments avec sentiments
df_cleaned = pd.read_csv('cleaned_apple_scraping.csv')
df_segments_with_sentiment = pd.read_csv('article_segments_with_sentiment.csv')

# Supprimer les lignes avec des valeurs manquantes dans la colonne 'text'
df_cleaned = df_cleaned.dropna(subset=['text'])

# Ajouter un ID unique à chaque article
df_cleaned['article_id'] = df_cleaned.index

# Fonction pour agréger les sentiments des segments
def aggregate_sentiments(sentiments):
    positive = sum(1 for s in sentiments if s == 'positive')
    negative = sum(1 for s in sentiments if s == 'negative')
    neutral = sum(1 for s in sentiments if s == 'neutral')

    total = positive + negative + neutral
    if total == 0:
        return 'neutral'

    return max(('positive', positive), ('negative', negative), ('neutral', neutral), key=lambda x: x[1])[0]

# Agréger les résultats des segments pour chaque article
article_sentiments = df_segments_with_sentiment.groupby('article_id')['sentiment'].apply(list).apply(aggregate_sentiments)

# Ajouter les sentiments agrégés au dataframe initial
df_cleaned['sentiment'] = df_cleaned['article_id'].map(article_sentiments)

# Logger les résultats de l'analyse de sentiment
for index, row in df_cleaned.iterrows():
    logging.info(f"Article '{row['title']}' (ligne {index}) analysé avec succès: Sentiment = {row['sentiment']}")

# Sauvegarder le dataframe avec la nouvelle colonne
cleaned_file_path = 'cleaned_apple_scraping_with_sentiment.csv'
df_cleaned.to_csv(cleaned_file_path, index=False)

print(f"Fichier analysé et sauvegardé sous: {cleaned_file_path}")
