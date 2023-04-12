import os


def read_text(file_path):
    f = open(file_path, "r")
    data = f.read().splitlines()

    return data


def get_file_urls(folder_location):
    file_urls = []
    for filename in os.listdir(folder_location):
        file_path = os.path.join(folder_location, filename)
        if os.path.isfile(file_path):
            file_urls.append(os.path.abspath(file_path))
    return file_urls
