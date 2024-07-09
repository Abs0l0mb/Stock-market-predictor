import pandas as pd
from transformers import AutoTokenizer

# Charger le fichier CSV
file_path = 'cleaned_apple_scraping.csv'
df = pd.read_csv(file_path)

# Ajouter un ID unique à chaque article
df['article_id'] = df.index

# Charger le tokenizer
model_name = "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Fonction pour diviser le texte en segments plus petits basés sur les tokens
def split_into_segments(text, max_length):
    tokens = tokenizer.encode(text, add_special_tokens=True)
    segments = [tokens[i:i + max_length] for i in range(0, len(tokens), max_length)]
    segment_texts = [tokenizer.decode(segment, skip_special_tokens=True) for segment in segments]
    return segment_texts

# Diviser les articles en segments
segments = []

for index, row in df.iterrows():
    article_segments = split_into_segments(row['text'], 500)
    for segment in article_segments:
        segments.append({
            'article_id': row['article_id'],
            'segment_text': segment
        })

# Créer un dataframe pour les segments
df_segments = pd.DataFrame(segments)

# Sauvegarder les segments dans un nouveau fichier CSV
segments_file_path = 'article_segments.csv'
df_segments.to_csv(segments_file_path, index=False)

print(f"Segments sauvegardés sous: {segments_file_path}")
