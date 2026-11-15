import re

def normalize_text(text):
    if (not text or not isinstance(text, str) 
        or text.isspace() or not re.search(r"[a-zA-Z]", text)):
        
        return None
    
    lowercase_text = text.lower()
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]+'," ", lowercase_text)
    normalized_text = re.sub(r'\s+', " ", cleaned_text)
    stripped_text = normalized_text.strip()
    return stripped_text

def find_ingredients(text, known_ingredients):
    ingredient_candidates = []
    accepted_ingredients = []
    found_ingredients = []

    for ingredient in known_ingredients:
        escape_ingredient = re.escape(ingredient)
        match = re.search(rf'\b{escape_ingredient}\b', text)
        if match:
            ingredient_candidates.append((ingredient, match.start(), match.end()))

    sorted_ingredients = sorted(
        ingredient_candidates,
        key=lambda  i: i[2] -i[1],
        reverse=True
    )

    for candidate in sorted_ingredients:
        has_overlap = False

        for found in found_ingredients:
            if (candidate[1] < found[2] and candidate[2] > found[1]):
                has_overlap = True
                break

        if not has_overlap:
            found_ingredients.append(candidate)
            accepted_ingredients.append(candidate[0])
        
    return accepted_ingredients