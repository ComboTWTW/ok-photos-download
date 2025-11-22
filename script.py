import os
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

CURRENT_YEAR = datetime.now().year

# Insert your list of OK.ru links here:
url_list = []

if not os.path.exists("images"):
    os.makedirs("images")


def sanitize_filename(filename: str) -> str:
    """Keep letters, digits, spaces, dot, underscore, dash; preserve Cyrillic."""
    filename = re.sub(r"[^\w\dа-яА-ЯёЁ\.\s_-]", "_", filename)
    return filename.strip()


def append_year_if_missing(date_str: str) -> str:
    """If date doesn't contain a 4-digit year, append current year."""
    if re.search(r"\b\d{4}\b", date_str):
        return date_str
    return f"{date_str} {CURRENT_YEAR}"


def make_unique_filename(directory: str, base_name: str, ext: str = ".jpg") -> str:
    """
    Return a filename that does not collide in `directory`.
    If base_name + ext exists, try base_name_2.ext, base_name_3.ext, ...
    """
    base_name = base_name.strip()
    candidate = f"{base_name}{ext}"
    path = os.path.join(directory, candidate)
    if not os.path.exists(path):
        return candidate

    # find next available suffix
    i = 2
    while True:
        candidate = f"{base_name}_{i}{ext}"
        path = os.path.join(directory, candidate)
        if not os.path.exists(path):
            return candidate
        i += 1


for idx, url in enumerate(url_list, start=1):
    print(f"\nProcessing {idx}/{len(url_list)}: {url}")

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to fetch page: {e}")
        continue

    soup = BeautifulSoup(response.content, "html.parser")

    img_tag = soup.find("img", class_="image-layer_img")
    if not img_tag:
        print("❌ No image found on page!")
        continue

    img_src = img_tag.get("src")
    if not img_src:
        print("❌ Image src is empty!")
        continue

    # handle protocol-less src like //...
    if img_src.startswith("//"):
        img_src = "https:" + img_src

    # If src is relative (starts with /) you might need to prefix the site domain.
    # For OK.ru, images are usually absolute, so we assume it is correct.

    date_tag = soup.find("div", class_="date__tmxz7")
    if not date_tag:
        print("❌ No date element found!")
        continue

    date_text = date_tag.get_text(strip=True)
    full_date = append_year_if_missing(date_text)
    safe_base = sanitize_filename(full_date)

    filename = make_unique_filename("images", safe_base, ext=".jpg")
    out_path = os.path.join("images", filename)

    try:
        img_resp = requests.get(img_src, timeout=30)
        img_resp.raise_for_status()
        with open(out_path, "wb") as f:
            f.write(img_resp.content)
        print(f"✔ Downloaded as: {filename}")
    except Exception as e:
        print(f"❌ Failed to download image: {e}")
