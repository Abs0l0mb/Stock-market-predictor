from transformers import AutoModelForSequenceClassification, pipeline
from transformers import AutoTokenizer
import pandas as pd
import logging

# Configuration du logger pour fichier et console
logging.basicConfig(
    filename='segment_sentiment_analysis.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Charger les segments
df_segments = pd.read_csv('article_segments.csv')

# Charger le modèle et le tokenizer
model_name = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
sentiment_analysis = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=0)

# Analyser le sentiment de chaque segment
def analyze_segment_sentiment(text):
    try:
        result = sentiment_analysis(text)
        return result[0]['label']
    except Exception as e:
        logging.error(f"Erreur lors de l'analyse du segment: {str(e)}")
        return 'error'

df_segments['sentiment'] = df_segments['segment_text'].apply(analyze_segment_sentiment)

# Sauvegarder les résultats des segments avec les sentiments
segments_with_sentiment_file_path = 'article_segments_with_sentiment.csv'
df_segments.to_csv(segments_with_sentiment_file_path, index=False)

print(f"Segments avec sentiments sauvegardés sous: {segments_with_sentiment_file_path}")
