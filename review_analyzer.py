# import pandas as pd
# from textblob import TextBlob
# from textblob_nl import PatternTagger, PatternAnalyzer
#
#
# def analyze_reviews(file_location):
#     # Read in the text file
#     with open(file_location, 'r', encoding='utf-8') as file:
#         reviews = file.read().splitlines()
#
#     # Perform sentiment analysis on each review using TextBlob
#     blobs = [TextBlob(review, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()).sentiment for review in reviews]
#
#     # Categorize each review as positive, negative, or neutral based on polarity score
#     sentiments = []
#     for blob in blobs:
#         if blob[0] > 0:
#             sentiments.append('Positive')
#         elif blob[0] < 0:
#             sentiments.append('Negative')
#         else:
#             sentiments.append('Neutral')
#
#     # Create a dataframe to store the results
#     df = pd.DataFrame({'Review': reviews, 'Sentiment': sentiments, 'Polarity': blobs})
#
#     return df
