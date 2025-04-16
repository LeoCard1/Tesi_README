import csv

import config

# Define category priority based on importance (lower number = more important)
category_priority = {
    "description": 1,
    "install": 2,
    "configuration": 3,
    "features": 4,
    "prerequisites": 5,
    "license": 6,
    "testing": 7,
    "documentation": 8,
    "performance": 9,
    "contacts": 10,
    "credits": 11,
    "help": 12,
    "todo": 13,
    "feedback": 14
}

def evaluate_readme(row):
    # Score for Total Titles Recognized
    titles = int(row['Total_titles_recognized'])
    if titles <= 5: title_score = 1
    elif titles <= 10: title_score = 2
    elif titles <= 15: title_score = 3
    elif titles <= 20: title_score = 4
    else: title_score = 5

    # Score for Char Counts
    chars = int(row['Char_counts'])
    if chars <= 1000: char_score = 1
    elif chars <= 5000: char_score = 2
    elif chars <= 10000: char_score = 3
    elif chars <= 20000: char_score = 4
    else: char_score = 5

    # Score for Num Images
    images = int(row['Num_images'])
    if images == 0: image_score = 1
    elif images <= 3: image_score = 2
    elif images <= 6: image_score = 3
    elif images <= 10: image_score = 4
    else: image_score = 5

    # Score for Num Links
    links = int(row['Num_links'])
    if links <= 5: link_score = 1
    elif links <= 10: link_score = 2
    elif links <= 20: link_score = 3
    elif links <= 30: link_score = 4
    else: link_score = 5

    # Score for Categories based on priority
    categories = {key: row[key] for key in category_priority.keys() if row[key] != ''}
    sorted_categories = sorted(categories.items(), key=lambda item: category_priority[item[0]])

    # We give more weight to higher priority categories
    cat_score = sum([category_priority[cat] for cat, _ in sorted_categories]) / len(sorted_categories) if sorted_categories else 0

    total_score = (title_score + char_score + image_score + link_score + cat_score) / 5
    return round(total_score)

# Read CSV and evaluate
with open(config.TABLES_OUT_DIR+'readme_summary.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        score = evaluate_readme(row)
        print(f"File: {row['File_name']}, Score: {score}")
