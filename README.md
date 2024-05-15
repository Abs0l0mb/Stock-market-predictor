# Aviation stock market predictor

## Goal
The goal of this project is to develop a model that could predict the evolution of stock prices in the aviation sector based on sentiment analysis and generation of descriptors on article titles.
## Methodology
### 1 - API 
J'ai fait la demande pour un accès API à l'AFP, à voir si on va nous dire oui
### 2 - Pipeline
For the sentiment analysis part, we can use "twitter-roberta-base-sentiment-latest", which gives us 3 classes (positive, neutral, negative) between 0 and 1. 

Then, we will have to think about the additionnal informations that we have to put in the descriptor that could be meaningful and could generate correlation with stock prices (eg. is the article talking about technical things, political things, maybe the subdomain, what's the company size, etc.) Those informations can be expressed as floats in [-1, 1] or [0, 1] or even as integer values with 2 or 3 possibilities. 

We can add to this vector the current financial indicators (MA, MACD, ...)

We could also add things like risk (do i want the network to take risks or not) and things exterior to the article to make a prediction that could affect its behavior.

The resulting vector is then fed into a neural network that will output a vector containing informations such as :

* short/long (0/1)
* duration (in days)
* eventual stop loss threshold
* eventual take profit threshold

This prediction can then be exploited on the market. The last step is to make a simple script that takes those informations to make a trade and put it on the market with an API.

### 3 - Method

First we select a fixed number of companies

We then extract all the articles that talks about said companies for the day. For each articles, a combination of sentiment analysis and feature extraction are made.

Then, we concatenate all these vectors to obtain a single vector of sentiment and features per company for the day. 

We then feed this vector along with the financial informations of the day, week, month and year of the company into a company specific model (that has been trained with only the data of that company).

The output is then produced and can be exploited.
