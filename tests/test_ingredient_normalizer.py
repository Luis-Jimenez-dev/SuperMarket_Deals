from normalization.ingredient_normalizer import classify_ingredient


def test_classify_chicken_breasts():
    result = classify_ingredient("Chicken Breasts")
    assert result == "poultry"


def test_classify_brown_rice():
    result = classify_ingredient("Brown Rice")
    assert result == "grains"


def test_classify_soy_sauce():
    result = classify_ingredient("Soy Sauce")
    assert result == "sauces"


def test_classify_unknown_ingredient():
    result = classify_ingredient("Something We Do Not Know")
    assert result is None