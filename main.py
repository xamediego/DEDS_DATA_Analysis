from PIL import Image
import requests
from io import BytesIO
import webcolors
import pandas as pd
from textblob import TextBlob
from textblob_nl import PatternTagger, PatternAnalyzer


def read_text(file_path):
    f = open(file_path, "r")
    data = f.read().splitlines()

    return data


def get_image_analysis(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    return top_colos(img, 2)


def closest_colour(requested_colour):
    min_colours = {}

    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name

    return min_colours[min(min_colours.keys())]


def top_colos(image, n):
    # convert the image to rgb
    image = image.convert('RGB')

    # resize the image to 300 x 300
    image = image.resize((50, 50))
    detected_colors = []

    for x in range(image.width):
        for y in range(image.height):
            detected_colors.append(closest_colour(image.getpixel((x, y))))

    Series_Colors = pd.Series(detected_colors)
    output = Series_Colors.value_counts() / len(Series_Colors)

    return output.head(n)


def compare_results(old_dic, result):
    created_dict = old_dic.copy()

    for key in result.keys():

        if key not in created_dict:
            created_dict[key] = []
            created_dict[key].append(result[key])
        else:
            created_dict[key].append(result[key])

    return created_dict


def make_arrays_same_size(dictionary):
    # Get the length of the longest array in the dictionary
    max_length = max([len(arr) for arr in dictionary.values()])

    # Loop through the dictionary and append None values to any array that is shorter than max_length
    for key, arr in dictionary.items():
        if len(arr) < max_length:
            num_to_append = max_length - len(arr)
            dictionary[key] = arr + [None] * num_to_append

    return dictionary


urls = read_text('image_links.txt')

dic = {}
count = 0
for url in urls:
    if count == 10: break
    analysis_result = get_image_analysis(url)
    dic = compare_results(dic, analysis_result)
    count += 1

dic = make_arrays_same_size(dic)
df = pd.DataFrame(dic)
df.to_excel("images_analysis.xlsx")

dic = {'positive': [], 'negative': [], 'neutral': []}


def analyze_reviews(file_location):
    # Read in the text file
    with open(file_location, 'r', encoding='utf-8') as file:
        reviews = file.read().splitlines()

    # Perform sentiment analysis on each review using TextBlob
    blobs = [TextBlob(review, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()).sentiment for review in reviews]

    # Categorize each review as positive, negative, or neutral based on polarity score
    sentiments = []
    for blob in blobs:
        if blob[0] > 0:
            sentiments.append('Positive')
        elif blob[0] < 0:
            sentiments.append('Negative')
        else:
            sentiments.append('Neutral')

    # Create a dataframe to store the results
    df = pd.DataFrame({'Review': reviews, 'Sentiment': sentiments, 'Polarity': blobs})

    return df


file_location = 'reviews.txt'
df = analyze_reviews(file_location)
df.to_excel("reviews_analysis.xlsx")
