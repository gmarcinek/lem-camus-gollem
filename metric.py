#!/usr/bin/env python3
# metric.py

import sys
import re

def count_syllables(word: str) -> int:
    """Proste liczenie sylab w polskim słowie na podstawie samogłosek."""
    word = word.lower()
    vowels = "aeiouyąęó"
    count = sum(1 for ch in word if ch in vowels)
    return max(1, count)  # minimum 1 sylaba

def flesch_reading_ease(text: str) -> float:
    """Indeks czytelności Flescha."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    words = re.findall(r'\w+', text, re.UNICODE)
    syllables = sum(count_syllables(w) for w in words)

    total_sentences = max(1, len(sentences))
    total_words = max(1, len(words))
    avg_sentence_length = total_words / total_sentences
    avg_syllables_per_word = syllables / total_words

    # Formuła Flescha (angielska wersja)
    score = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word
    return score

def gunning_fog_index(text: str) -> float:
    """Indeks Gunning FOG."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    words = re.findall(r'\w+', text, re.UNICODE)
    total_sentences = max(1, len(sentences))
    total_words = max(1, len(words))
    avg_sentence_length = total_words / total_sentences

    # "Trudne słowa" - >=3 sylab
    complex_words = [w for w in words if count_syllables(w) >= 3]
    percent_complex = (len(complex_words) / total_words) * 100

    fog = 0.4 * (avg_sentence_length + percent_complex)
    return fog

def main():
    if len(sys.argv) != 2:
        print("Użycie: python metric.py <ścieżka_do_pliku.md>")
        sys.exit(1)

    path = sys.argv[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {path}")
        sys.exit(1)

    flesch_score = flesch_reading_ease(text)
    fog_index = gunning_fog_index(text)

    print("=" * 50)
    print(f"Analiza metryk czytelności dla pliku: {path}")
    print("=" * 50)
    print(f"Flesch Reading Ease: {flesch_score:.2f}")
    if flesch_score >= 60:
        print("  → Łatwy do czytania")
    elif flesch_score >= 30:
        print("  → Średni poziom trudności")
    else:
        print("  → Bardzo trudny tekst")

    print(f"Gunning FOG Index: {fog_index:.2f}")
    print(f"  → Wymagany poziom edukacji: ok. {fog_index:.0f} lat nauki")
    print("=" * 50)

if __name__ == "__main__":
    main()
