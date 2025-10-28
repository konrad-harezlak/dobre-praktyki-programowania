def is_palindrome(text: str) -> bool:
    # Usuwamy spacje i zmieniamy tekst na małe litery
    cleaned_text = ''.join(text.split()).lower()
    # Porównujemy tekst z jego odwrotnością
    return cleaned_text == cleaned_text[::-1]

def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

def count_vowels(text: str) -> int:
    vowels = "aeiouyáéíóúý"
    return sum(1 for char in text.lower() if char in vowels)
