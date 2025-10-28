from main import is_palindrome, fibonacci, count_vowels, calculate_discount, flatten_list, word_frequencies, is_prime

def test_is_palindrome():
    assert is_palindrome("kajak") == True
    assert is_palindrome("Kobyła ma mały bok") == True
    assert is_palindrome("python") == False
    assert is_palindrome("") == True
    assert is_palindrome("A") == True
