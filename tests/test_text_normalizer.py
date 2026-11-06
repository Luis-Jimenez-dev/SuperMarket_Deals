from normalization.text_normalizer import (
    normalize_text,
    find_best_known_term,
    analyze_text
    )

def test_normalize_chicken_breast():
    result = normalize_text("ChiCKEN brEast")
    assert result == "chicken breast"

def test_normalize_plural_chicken_breasts():
    result = normalize_text("CHICKEN BREASTS")
    assert result == "chicken breast"

def test_does_not_remove_s_from_non_plural_word():
    result = normalize_text("does")
    assert result == "does"

def test_find_known_term_inside_product_name():
    result = find_best_known_term("Kikkoman Soy Sauce")
    assert result == "soy sauce"

def test_known_term_does_not_match_inside_another_word():
    result = find_best_known_term("price")
    assert result is None

def test_unknown_term_returns_none():
    result = find_best_known_term("fosjs")
    assert result is None

def test_find_best_known_term_prefers_more_specific_term():
    result = find_best_known_term("Signature Farms Chicken Breast")
    assert result == "chicken breast"

def test_analyze_known_product():
    result = analyze_text("Kikkoman Soy Sauce")
    assert result == {
        "original" : 'Kikkoman Soy Sauce',
        "normalized" : 'kikkoman soy sauce',
        "matched_term" : 'soy sauce',
        "recognized" : True
    }

def test_analyze_unknown_product():
    result = analyze_text("Gochujang", review_unknown=False)
    assert result == {
        "original" : 'Gochujang',
        "normalized" : 'gochujang',
        "matched_term" : None,
        "recognized" : False
    }