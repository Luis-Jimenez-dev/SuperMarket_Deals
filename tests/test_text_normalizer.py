from rework_normalization.text_normalizer import (
    normalize_text,
    )

def test_normalize_chicken_breast():
    result = normalize_text("ChiCKEN brEast!")
    assert result == "chicken breast"

def test_remove_extra_whitespace():
    result = normalize_text("  Frozen   Broccoli   FLORETS   ")
    assert result == "frozen broccoli florets"

def test_None_as_invalid():
    result = normalize_text(None)
    assert result == None

def test_empty_string_as_invalid():
    result = normalize_text("")
    assert result == None

def test_whitespace_string_as_invalid():
    result = normalize_text("    ")
    assert result == None

def test_intiger_as_invalid():
    result = normalize_text(123)
    assert result == None

def test_no_letters_invalid():
    result = normalize_text("12345!!!")
    assert result == None

def test_numbers_and_letters_valid():
    result = normalize_text("16 oz Beef")
    assert result == "16 oz beef"