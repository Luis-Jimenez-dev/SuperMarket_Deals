import json
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

CACHE_FILE = DATA_DIR / "normalization_cache.json"
VOCABULARY_FILE = DATA_DIR / "grocery_vocabulary.json"
REVIEW_FILE = DATA_DIR / "normalization_review.json"


SINGULAR_EXCEPTIONS = {
    "asparagus",
    "couscous",
    "molasses",
}

WORD_NORMALIZATIONS = {
    "breasts": "breast",
    "carrots": "carrot",
    "onions": "onion",
    "tomatoes": "tomato",
    "potatoes": "potato",
    "leaves": "leaf",
    "loaves": "loaf",
}


def load_json(file_path, default):
    if not file_path.exists():
        return default

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(file_path, data):
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
            sort_keys=True
        )


normalization_cache = load_json(CACHE_FILE, {})
normalization_review = load_json(REVIEW_FILE, {})
grocery_vocabulary = load_json(
    VOCABULARY_FILE,
    {"ingredients": []}
)


def clean_text(text):
    if not isinstance(text, str):
        return ""

    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s'-]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def singularize_word(word):
    if not word:
        return word

    if word in normalization_cache:
        return normalization_cache[word]

    if word in SINGULAR_EXCEPTIONS:
        return word

    if word in WORD_NORMALIZATIONS:
        return WORD_NORMALIZATIONS[word]

    if word.endswith("ies") and len(word) > 3:
        return word[:-3] + "y"

    if word.endswith("ches") and len(word) > 4:
        return word[:-2]

    if word.endswith("shes") and len(word) > 4:
        return word[:-2]

    if word.endswith("xes") and len(word) > 3:
        return word[:-2]

    if word.endswith("zzes") and len(word) > 4:
        return word[:-2]

    if word.endswith("sses") and len(word) > 4:
        return word[:-2]

    return word


def normalize_text(text):
    cleaned_text = clean_text(text)

    if not cleaned_text:
        return ""

    words = cleaned_text.split()
    normalized_words = []

    for word in words:
        normalized_words.append(singularize_word(word))

    return " ".join(normalized_words)


def normalize_list(values):
    normalized_values = []

    for value in values:
        normalized = normalize_text(value)

        if normalized:
            normalized_values.append(normalized)

    return normalized_values


def get_known_terms():
    known_terms = set()

    for terms in grocery_vocabulary.values():
        for term in terms:
            normalized_term = normalize_text(term)

            if normalized_term:
                known_terms.add(normalized_term)

    return known_terms


def is_known_term(text):
    normalized_text = normalize_text(text)

    if not normalized_text:
        return False

    return normalized_text in get_known_terms()


def find_known_terms(text):
    normalized_text = normalize_text(text)

    if not normalized_text:
        return []

    known_terms = get_known_terms()
    matches = []

    for term in known_terms:
        pattern = rf"\b{re.escape(term)}\b"

        if re.search(pattern, normalized_text):
            matches.append(term)

    matches.sort(
        key=lambda term: (
            len(term.split()),
            len(term)
        ),
        reverse=True
    )

    return matches


def find_best_known_term(text):
    matches = find_known_terms(text)

    if not matches:
        return None

    return matches[0]


def add_to_review(text, source="unknown"):
    normalized_text = normalize_text(text)

    if not normalized_text:
        return

    if find_best_known_term(normalized_text) is not None:
        return

    if normalized_text not in normalization_review:
        normalization_review[normalized_text] = {
            "count": 1,
            "sources": [source]
        }
    else:
        normalization_review[normalized_text]["count"] += 1

        sources = normalization_review[normalized_text]["sources"]

        if source not in sources:
            sources.append(source)


def save_review_cache():
    save_json(REVIEW_FILE, normalization_review)


def add_to_cache(original_text, normalized_text):
    original_text = clean_text(original_text)
    normalized_text = clean_text(normalized_text)

    if not original_text or not normalized_text:
        return

    normalization_cache[original_text] = normalized_text
    save_json(CACHE_FILE, normalization_cache)

    review_keys = {
        original_text,
        normalize_text(original_text)
    }

    review_changed = False

    for key in review_keys:
        if key in normalization_review:
            del normalization_review[key]
            review_changed = True

    if review_changed:
        save_review_cache()


def analyze_text(text, source="unknown", review_unknown=True):
    normalized_text = normalize_text(text)

    if not normalized_text:
        return {
            "original": text,
            "normalized": "",
            "matched_term": None,
            "recognized": False
        }

    matched_term = find_best_known_term(normalized_text)
    recognized = matched_term is not None

    if not recognized and review_unknown:
        add_to_review(normalized_text, source)

    return {
        "original": text,
        "normalized": normalized_text,
        "matched_term": matched_term,
        "recognized": recognized
    }


def normalize_and_review(text, source="unknown"):
    analysis = analyze_text(
        text,
        source=source,
        review_unknown=True
    )

    return analysis["normalized"]