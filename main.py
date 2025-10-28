def is_palindrome(text: str) -> bool:
    # Usuwamy spacje i zmieniamy tekst na małe litery
    cleaned_text = ''.join(text.split()).lower()
    # Porównujemy tekst z jego odwrotnością
    return cleaned_text == cleaned_text[::-1]

