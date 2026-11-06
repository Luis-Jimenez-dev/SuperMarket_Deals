from normalization.text_normalizer import (
    normalize_text,
    find_best_known_term,
    analyze_text,
    get_canonical_term
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
        "canonical": 'soy sauce',
        "recognized" : True
    }

def test_analyze_unknown_product():
    result = analyze_text("Gochujang", review_unknown=False)
    assert result == {
        "original" : 'Gochujang',
        "normalized" : 'gochujang',
        "matched_term" : None,
        "canonical": None,
        "recognized" : False
    }

def test_get_canonical_term_for_alias():
    result = get_canonical_term("minced garlic")
    assert result == "garlic"


def test_get_canonical_term_preserves_specific_ingredient():
    result = get_canonical_term("coconut milk")
    assert result == "coconut milk"


def test_analyze_product_returns_specific_match_and_canonical_term():
    result = analyze_text(
        "Fresh Minced Garlic 8 oz",
        review_unknown=False
    )

    assert result["matched_term"] == "minced garlic"
    assert result["canonical"] == "garlic"

def test_normalize_chicken_thighs():
    result = normalize_text("Chicken Thighs")
    assert result == "chicken thigh"


def test_normalize_chicken_legs():
    result = normalize_text("Chicken Legs")
    assert result == "chicken leg"


def test_normalize_egg_yolks():
    result = normalize_text("Egg Yolks")
    assert result == "egg yolk"


def test_normalize_buns():
    result = normalize_text("Buns")
    assert result == "bun"

def test_source_typo_maps_to_canonical_shallot():
    result = get_canonical_term("challots")
    assert result == "shallot"


def test_hotsauce_maps_to_canonical_hot_sauce():
    result = get_canonical_term("hotsauce")
    assert result == "hot sauce"