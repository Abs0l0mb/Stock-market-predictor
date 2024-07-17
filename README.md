# Stock market predictor

## Goal

The goal of this project is to develop a model that could predict the evolution of stock prices based on sentiment analysis of articles and financial data.

## Methodology

### Input (Dataset)

To create the dataset, we need to scrape articles from CNBC and analyze their sentiment (positive, neutral, negative). We also add the category provided by CNBC to the data.
We combine those informations with financial data extracted from twelveAPI (https://github.com/twelvedata/twelvedata-python).

The resulting dataset should look like this :

![image](https://github.com/user-attachments/assets/2cd0da09-637c-4ab9-a3d8-d64cc1966577)

### Models

Various models have been tested. Though LSTM could have been an ideal candidate, the data formatting that it necessitates made us use simpler models at first, such as SVM and random forests.
The implementation of a LSTM have been tested on financial data only. Since we want to infer only on days that have at least an article (category + sentiment) associated to it, the dataset would have been quite complex for it to be transformed into a time series.

For random forests the number fo predictor have been determined by graphing the accuracy and precision depending on the number of predictors.

![image](https://github.com/user-attachments/assets/bb2060b4-fbb7-46c9-ab45-5d50b106e042)

![image](https://github.com/user-attachments/assets/a27374d6-7d5d-4d4e-a786-e9c956b8ec03)

We did not dive deep into the paramters of the SVM. We only tested commonly used kernels and compared accuracy and precision.

### Output

The models gives us, for a given day d, if wether the closing price of day d+1 will be higher or lower than day d.

## Results

The results obtained on Apple are promising. Though with only inputting financial data into an LSTM, we get a 50% accuracy, the results are more precise when using sentiment analysis with SVM and random forests.

Results for random forests

![image](https://github.com/user-attachments/assets/d41c4761-53c4-4948-bdd3-9939fbd3eb5f)

Results for SVM

![image](https://github.com/user-attachments/assets/c771f1c4-e892-49a5-8e19-832bd907793c)

As we can see, the gain of precision is not drastic, but it is promising in the sense that articles are relevant for stock prediction to an extent.

## Perspectives

Further adjustements can be made. 

First, the tests describes above have been conducted on Apple data. Apple is a verys table company, that is not subject to volatility. Maybe choosing a smaller company that is heavily dependent on its performance (such as astrazeneca during covid) could be more efficient.

Also, the implementation of an LSTM could better capture the long term dependencies of stock variation and sentiment

Another improvement could be to scrape data from multiple information websites to get more articles, and so have a more nuanced approach concerning sentiment analysis.

For example, we could calculate the proportion of articles speaking negatively about a company, and use this proportion instead of just rounding to the most present sentiment.
