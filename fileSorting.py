import os
import re
import shutil

# folder where your images are stored
IMAGES_DIR = "images"

# Russian month names → month number and capitalized folder names
MONTHS = {
    "января":  ("01", "Январь"),
    "февраля": ("02", "Февраль"),
    "марта":   ("03", "Март"),
    "апреля":  ("04", "Апрель"),
    "мая":     ("05", "Май"),
    "июня":    ("06", "Июнь"),
    "июля":    ("07", "Июль"),
    "августа": ("08", "Август"),
    "сентября":("09", "Сентябрь"),
    "октября": ("10", "Октябрь"),
    "ноября":  ("11", "Ноябрь"),
    "декабря": ("12", "Декабрь")
}

# Regex to capture filenames like:
# "26 октября 2025.jpg" or "26 октября 2025_2.jpg"
DATE_PATTERN = re.compile(
    r"^\s*(\d{1,2})\s+([а-яё]+)\s+(\d{4})", re.IGNORECASE
)

for filename in os.listdir(IMAGES_DIR):
    if not filename.lower().endswith(".jpg"):
        continue

    match = DATE_PATTERN.match(filename)
    if not match:
        print(f"⚠️ Skipped (not a date): {filename}")
        continue

    day, month_name, year = match.groups()
    month_name = month_name.lower()

    if month_name not in MONTHS:
        print(f"⚠️ Unknown month in: {filename}")
        continue

    month_num, month_title = MONTHS[month_name]

    # Folder name example: "Август 2025"
    target_folder = f"{month_title} {year}"
    target_path = os.path.join(IMAGES_DIR, target_folder)

    if not os.path.exists(target_path):
        os.makedirs(target_path)

    src_path = os.path.join(IMAGES_DIR, filename)
    dst_path = os.path.join(target_path, filename)

    try:
        shutil.move(src_path, dst_path)
        print(f"✔ Moved: {filename} → {target_folder}/")
    except Exception as e:
        print(f"❌ Error moving {filename}: {e}")
