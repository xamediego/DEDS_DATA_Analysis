import pandas as pd
import image_analyzer
# import review_analyzer
import server_connector
import pymssql

img_url = 'submit/images'
image_result_dictionary = image_analyzer.analyze_images(img_url, 10, 100, 50, 10)
image_result_dataframe = pd.DataFrame(image_result_dictionary)
image_result_dataframe.to_excel("images_analysis.xlsx")

# file_location = 'submit/reviews/reviews.txt'
# review_result_dataframe = review_analyzer.analyze_reviews(file_location)
# review_result_dataframe.to_excel("reviews_analysis.xlsx")

DB_NAME = 'Competitor_Data'

server_connector.save_to_sql_server_tr(image_result_dataframe, 'Image_Colour_Info', '.', DB_NAME, True, 'Image_URL')
# server_connector.save_to_sql_server_tr(image_result_dataframe, 'Review_Info', '.', DB_NAME, True)
