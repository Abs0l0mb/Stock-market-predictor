import pandas as pd

def most_common(series):
    series = series.dropna()
    if len(series) == 0:
        return None
    return series.value_counts().idxmax()

aapl_data = pd.read_csv('./AAPL.csv')
articles_data = pd.read_csv('./cleaned_apple_scraping_with_sentiment.csv')

aapl_data['datetime'] = pd.to_datetime(aapl_data['datetime']).dt.date
articles_data['date_published'] = pd.to_datetime(articles_data['date_published']).dt.date

dominant_category = articles_data.groupby('date_published')['category'].agg(most_common).reset_index()
dominant_sentiment = articles_data.groupby('date_published')['sentiment'].agg(most_common).reset_index()

aapl_data = aapl_data.merge(dominant_category, left_on='datetime', right_on='date_published', how='left')
aapl_data = aapl_data.merge(dominant_sentiment, left_on='datetime', right_on='date_published', how='left')

print(aapl_data)
aapl_data = aapl_data.drop(columns=['date_published_x', 'date_published_y'])

aapl_data = aapl_data.rename(columns={'category': 'dominant_category', 'sentiment': 'dominant_sentiment'})

aapl_data.to_csv('./AAPL_with_articles.csv', index=False)

print(aapl_data.head())
