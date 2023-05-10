import os
import requests
import re

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
