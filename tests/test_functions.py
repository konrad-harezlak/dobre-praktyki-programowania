import pytest
from main import is_palindrome, fibonacci, count_vowels, calculate_discount, flatten_list, word_frequencies, is_prime

def test_is_palindrome():
    assert is_palindrome("kajak") == True
    assert is_palindrome("Kobyła ma mały bok") == True
    assert is_palindrome("python") == False
    assert is_palindrome("") == True
    assert is_palindrome("A") == True

def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(5) == 5
    assert fibonacci(10) == 55
    with pytest.raises(ValueError):
        fibonacci(-1)
def test_count_vowels():
    assert count_vowels("Python") == 1  # Tylko 'o'
    assert count_vowels("AEIOUY") == 6  # Wszystkie samogłoski
    assert count_vowels("bcd") == 0  # Brak samogłosk
    assert count_vowels("") == 0  # Pusty ciąg
    assert count_vowels("Próba żółwia") == 4  # Uwzględnia polskie znaki
def test_calculate_discount():
    assert calculate_discount(100, 0.2) == 80.0
    assert calculate_discount(50, 0) == 50.0
    assert calculate_discount(200, 1) == 0.0
    try:
        calculate_discount(100, -0.1)
    except ValueError:
        pass
    else:
        assert False, "Funkcja nie zgłosiła wyjątku dla zniżki < 0"
    try:
        calculate_discount(100, 1.5)
    except ValueError:
        pass
    else:
        assert False, "Funkcja nie zgłosiła wyjątku dla zniżki > 1"
