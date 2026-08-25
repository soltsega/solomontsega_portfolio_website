import re

with open('backend/app/seed.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all "category": "work" with "category": "course"
content = content.replace('"category": "work"', '"category": "course"')

# Replace back to internship for specific titles
def set_internship(title, content):
    pattern = r'("title": "' + re.escape(title) + r'".*?"category": )"course"'
    return re.sub(pattern, r'\1"internship"', content, flags=re.DOTALL)

content = set_internship("Information Network Security Administration (INSA)", content)
content = set_internship("Addis Ababa University", content)
content = set_internship("Elevvo NLP & Language AI Pathways", content)

# update orders
# AAU -> 1
content = re.sub(r'("title": "Addis Ababa University".*?"order": )\d+', r'\g<1>1', content, flags=re.DOTALL)
# INSA -> 2
content = re.sub(r'("title": "Information Network Security Administration \(INSA\)".*?"order": )\d+', r'\g<1>2', content, flags=re.DOTALL)
# Elevvo -> 3
content = re.sub(r'("title": "Elevvo NLP & Language AI Pathways".*?"order": )\d+', r'\g<1>3', content, flags=re.DOTALL)

# Add 10 Academy if not present
if "10 Academy" not in content:
    # insert after Elevvo
    elevvo_block_pattern = r'("title": "Elevvo NLP & Language AI Pathways".*?\},)'
    academy_10_block = """
    {
        "title": "10 Academy",
        "subtitle": "Data Engineering & AI",
        "description": "Intensive training and project work focusing on data pipelines, machine learning, and advanced AI systems.\\nDeveloped end-to-end data pipelines for real-world scenarios.",
        "category": "internship",
        "image_url": "",
        "order": 4,
    },"""
    content = re.sub(elevvo_block_pattern, r'\1' + academy_10_block, content, flags=re.DOTALL)

# AAU image
content = content.replace('"image_url": "/credentials/aau_logo.png"', '"image_url": "/credentials/aau_logo.jpg"')

with open('backend/app/seed.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated seed.py")
