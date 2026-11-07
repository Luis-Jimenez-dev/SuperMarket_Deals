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

def test_classify_chicken_breasts_as_poultry():
    assert classify_ingredient("Chicken Breasts") == "poultry"


def test_classify_minced_garlic_as_vegetable():
    assert classify_ingredient("Minced Garlic") == "vegetable"


def test_classify_ground_ginger_as_vegetable():
    assert classify_ingredient("Ground Ginger") == "vegetable"


def test_classify_challots_as_vegetable():
    assert classify_ingredient("Challots") == "vegetable"


def test_classify_hotsauce_as_sauce():
    assert classify_ingredient("Hotsauce") == "sauces"


def test_classify_egg_yolks_as_eggs():
    assert classify_ingredient("Egg Yolks") == "eggs"


def test_classify_water_returns_none():
    assert classify_ingredient("Water") is None


def test_unknown_ingredient_returns_none():
    assert classify_ingredient("Something We Have Never Seen") is None