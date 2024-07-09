import pandas as pd

# Load the data
aapl_data = pd.read_csv('./AAPL.csv')
articles_data = pd.read_csv('./cleaned_apple_scraping_with_sentiment.csv')

# Ensure the date formats match
aapl_data['datetime'] = pd.to_datetime(aapl_data['datetime']).dt.date
articles_data['date_published'] = pd.to_datetime(articles_data['date_published']).dt.date

# Define a function to get the most common category or sentiment
def most_common(series):
    series = series.dropna()
    if len(series) == 0:
        return None
    return series.value_counts().idxmax()

# Group articles by date to find the dominating category and sentiment
dominant_category = articles_data.groupby('date_published')['category'].agg(most_common).reset_index()
dominant_sentiment = articles_data.groupby('date_published')['sentiment'].agg(most_common).reset_index()

# Merge the dominant category and sentiment with the AAPL data
aapl_data = aapl_data.merge(dominant_category, left_on='datetime', right_on='date_published', how='left')
aapl_data = aapl_data.merge(dominant_sentiment, left_on='datetime', right_on='date_published', how='left')

# Drop the redundant date columns from the merge
print(aapl_data)
aapl_data = aapl_data.drop(columns=['date_published_x', 'date_published_y'])

# Rename columns for clarity
aapl_data = aapl_data.rename(columns={'category': 'dominant_category', 'sentiment': 'dominant_sentiment'})

# Save the result to a new CSV file
aapl_data.to_csv('./AAPL_with_articles.csv', index=False)

# Display the first few rows of the result
print(aapl_data.head())
