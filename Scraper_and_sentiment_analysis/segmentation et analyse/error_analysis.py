import pandas as pd
from transformers import AutoTokenizer

# Charger le fichier des segments avec les sentiments
file_path = 'article_segments_with_sentiment.csv'
df_segments_with_sentiment = pd.read_csv(file_path)

# Charger le tokenizer
model_name = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Filtrer les segments non textuels ou nulls
df_segments_with_sentiment = df_segments_with_sentiment.dropna(subset=['segment_text'])
df_segments_with_sentiment = df_segments_with_sentiment[df_segments_with_sentiment['segment_text'].apply(lambda x: isinstance(x, str))]

# Analyser les segments catégorisés en "error"
error_segments = df_segments_with_sentiment[df_segments_with_sentiment['sentiment'] == 'error'].copy()

# Vérifier la longueur des segments en tokens
def count_tokens(text):
    try:
        tokens = tokenizer.encode(text, add_special_tokens=True)
        return len(tokens)
    except Exception as e:
        print(f"Error tokenizing text: {e}")
        return -1

# Ajouter une colonne pour le nombre de tokens
error_segments.loc[:, 'token_count'] = error_segments['segment_text'].apply(count_tokens)

# Résumé des erreurs
error_summary = {
    'total_errors': len(error_segments),
    'unique_articles_with_errors': len(error_segments['article_id'].unique()),
    'average_segment_length': error_segments['segment_text'].apply(len).mean(),
    'max_segment_length': error_segments['segment_text'].apply(len).max(),
    'min_segment_length': error_segments['segment_text'].apply(len).min(),
    'average_token_count': error_segments['token_count'].mean(),
    'max_token_count': error_segments['token_count'].max(),
    'min_token_count': error_segments['token_count'].min(),
}

# Vérifier la distribution des erreurs par article
error_count_by_article = error_segments['article_id'].value_counts()

# Afficher les résultats
print("Error Segments Summary:")
print(error_summary)
print("\nTop 10 Articles with Most Errors:")
print(error_count_by_article.head(10))
print("\nError Segments (First 10 rows):")
print(error_segments.head(10))

# Sauvegarder les segments en erreur dans un fichier CSV pour inspection
error_segments_file_path = 'error_segments_analysis.csv'
error_segments.to_csv(error_segments_file_path, index=False)

print(f"\nSegments avec erreurs sauvegardés sous: {error_segments_file_path}")
