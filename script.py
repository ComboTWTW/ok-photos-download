import os
import requests
import re
from bs4 import BeautifulSoup

# Array with links to web pages (Insert here from script.js output)
url_list = []

# Open a text file for writing
with open("src_links.txt", "w") as f:
    for url in url_list:
        # Make a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content of the response with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all img tags with class "media-photos_img"
        img_tags = soup.find_all("img", class_="media-photos_img")

        # Extract the src attribute of each img tag and write it to the file
        for img_tag in img_tags:
            src = img_tag.get("src")
            f.write(src + "\n")

# Create a directory to save the images (if it doesn't exist)
if not os.path.exists("images"):
    os.makedirs("images")

# Read the src links from the text file
with open("src_links.txt", "r") as f:
    src_links = f.read().splitlines()

# Loop through the src links and download each image
for i, src_link in enumerate(src_links):
    # Get the filename by removing everything before the last "/"
    filename = src_link.rsplit("/", 1)[-1]

    # Replace any invalid filename characters with underscores
    filename = re.sub(r"[^\w\d\._-]", "_", filename)

    # Add the .jpg extension to the filename
    filename = os.path.splitext(filename)[0] + ".jpg"

    # Construct the full URL by adding the "https:" prefix to the src link
    url = "https:" + src_link

    # Send a GET request to the URL and save the response content to a file
    response = requests.get(url)
    with open("images/{}".format(filename), "wb") as img_file:
        img_file.write(response.content)

    # Print progress information
    print("Downloaded image {} of {}: {}".format(i+1, len(src_links), filename))
