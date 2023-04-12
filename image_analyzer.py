import datetime
import os.path

import requests
from io import BytesIO
import webcolors
import pandas as pd
import glob
from PIL import Image
import threading
import openpyxl

import Tools


def analyze_urls(urls, colour_amount):
    return_results = {}

    for url in urls:
        analysis_result = analyze_url_image(url, colour_amount)
        compare_results(return_results, analysis_result)

    return_results = make_arrays_same_size(return_results)

    return return_results


def analyze_images(folder_location, colour_amount, image_cluster_size, image_limit, thread_limit):
    image_files_full = Tools.get_file_urls(folder_location)[:image_limit]

    return_results = {'Image_URL': []}

    start_time = datetime.datetime.now()
    print(start_time)

    def analyze(image_urls, colour_amount):

        for image_url in image_urls:
            with open(image_url, 'rb') as f:
                image_file = f.read()

                return_results['Image_URL'].append(os.path.basename(image_url))
                analysis_result = analyze_img(image_file, colour_amount)
                compare_results(return_results, analysis_result)

    image_arrays = [image_files_full[i:i + image_cluster_size] for i in
                    range(0, len(image_files_full), image_cluster_size)]

    thread_array = []

    for image_list in image_arrays:
        img_thread = threading.Thread(target=analyze, args=(image_list, colour_amount))
        thread_array.append(img_thread)

    sliced_threads = [thread_array[i:i + thread_limit] for i in range(0, len(thread_array), thread_limit)]

    for threads in sliced_threads:
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    end_time = datetime.datetime.now()
    print(end_time)

    time_difference = end_time - start_time
    minutes_difference = int(time_difference.total_seconds() / 60)

    print(minutes_difference)
    print(time_difference)

    return_results = make_arrays_same_size(return_results)

    return return_results


def get_image_files(folder_location):
    image_files = []

    for filename in glob.glob(folder_location + '/*.jpg') + glob.glob(folder_location + '/*.jpeg') + glob.glob(
            folder_location + '/*.png') + glob.glob(folder_location + '/*.gif'):
        with open(filename, 'rb') as f:
            image_files.append(f)

    return image_files


def compare_results(old_dic, result):
    for key in result.keys():

        if key not in old_dic:
            old_dic[key] = []
            old_dic[key].append(result[key])
        else:
            old_dic[key].append(result[key])


def make_arrays_same_size(dictionary):
    max_length = max([len(arr) for arr in dictionary.values()])

    for key, arr in dictionary.items():
        if len(arr) < max_length:
            num_to_append = max_length - len(arr)
            dictionary[key] = arr + [None] * num_to_append

    return dictionary


def analyze_url_image(url, colour_amount):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    return get_image_analysis(img, colour_amount)


def analyze_img(img, colour_amount):
    img = Image.open(BytesIO(img))

    return get_image_analysis(img, colour_amount)


def get_image_analysis(img, colour_amount):
    return top_colours(img, colour_amount)


def closest_colour(requested_colour):
    min_colours = {}

    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name

    return min_colours[min(min_colours.keys())]


def top_colours(image, n):
    image = image.convert('RGB')

    image = image.resize((50, 50))
    detected_colors = []

    for x in range(image.width):
        for y in range(image.height):
            detected_colors.append(closest_colour(image.getpixel((x, y))))

    Series_Colors = pd.Series(detected_colors)
    output = Series_Colors.value_counts() / len(Series_Colors)

    return output.head(n)
