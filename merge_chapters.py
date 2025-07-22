#!/usr/bin/env python3
"""
Skrypt łączący pliki markdown w kolejności numerów rozdziałów.
Struktura: structure/X.Y/X.Y.Z.W.md
Wynik: dist/complete.md
"""

import os
import re
from pathlib import Path

def parse_chapter_number(filename):
    """Wyciąga numer rozdziału z nazwy pliku i konwertuje na krotkę dla sortowania."""
    # Wzorzec: X.Y.Z.W.md
    match = re.match(r'(\d+)\.(\d+)\.(\d+)\.(\d+)\.md$', filename)
    if match:
        return tuple(int(x) for x in match.groups())
    
    # Wzorzec: X.Y.Z.md  
    match = re.match(r'(\d+)\.(\d+)\.(\d+)\.md$', filename)
    if match:
        return tuple(int(x) for x in match.groups()) + (0,)
    
    # Wzorzec: X.Y.md
    match = re.match(r'(\d+)\.(\d+)\.md$', filename)
    if match:
        return tuple(int(x) for x in match.groups()) + (0, 0)
    
    return None

def find_markdown_files(structure_dir):
    """Znajduje wszystkie pliki .md w katalogu structure i sortuje je."""
    files = []
    
    for root, dirs, filenames in os.walk(structure_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                chapter_num = parse_chapter_number(filename)
                if chapter_num:
                    full_path = os.path.join(root, filename)
                    files.append((chapter_num, full_path, filename))
    
    # Sortuj według numerów rozdziałów
    files.sort(key=lambda x: x[0])
    return files

def clean_chapter_numbers(content):
    """Usuwa numery rozdziałów w formacie X.Y.Z.W z nagłówków."""
    # Wzorce do usunięcia na początku nagłówków
    patterns = [
        r'^(#+)\s+\d+\.\d+\.\d+\.\d+\s+',  # # 0.1.2.3 Tytuł
        r'^(#+)\s+\d+\.\d+\.\d+\s+',       # # 0.1.2 Tytuł  
        r'^(#+)\s+\d+\.\d+\s+',             # # 0.1 Tytuł
        r'^(#+)\s+\d+\s+',                  # # 0 Tytuł
    ]
    
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        cleaned_line = line
        for pattern in patterns:
            # Zastąp numer rozdziału tylko znacznikiem nagłówka
            cleaned_line = re.sub(pattern, r'\1 ', cleaned_line)
        cleaned_lines.append(cleaned_line)
    
    return '\n'.join(cleaned_lines)

def merge_files(files, output_path):
    """Łączy pliki w jeden dokument."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write("## Meta-nihilizm pragmatyczny czyli operacjonalny agnostycyzm trzeciego stopnia\n\n")
        output_file.write("\n\n")
        
        for i, (chapter_num, file_path, filename) in enumerate(files):
            print(f"Przetwarzam: {filename} ({'.'.join(map(str, chapter_num))})")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as input_file:
                    content = input_file.read()
                    
                    # Wyczyść numery rozdziałów
                    content = clean_chapter_numbers(content)
                    
                    output_file.write(content)
                    
                    # Dodaj separator między rozdziałami (oprócz ostatniego)
                    if i < len(files) - 1:
                        output_file.write("\n\n")
                        
            except Exception as e:
                print(f"Błąd przy przetwarzaniu {filename}: {e}")

def main():
    """Główna funkcja skryptu."""
    # Ścieżki
    script_dir = Path(__file__).parent
    structure_dir = script_dir / "structure"
    output_path = script_dir / "dist" / "complete.md"
    
    print(f"Szukam plików w: {structure_dir}")
    print(f"Wynik zostanie zapisany w: {output_path}")
    
    if not structure_dir.exists():
        print(f"BŁĄD: Katalog {structure_dir} nie istnieje!")
        return
    
    # Znajdź i posortuj pliki
    files = find_markdown_files(structure_dir)
    
    if not files:
        print("Nie znaleziono plików .md do połączenia!")
        return
    
    print(f"\nZnaleziono {len(files)} plików:")
    for chapter_num, file_path, filename in files:
        print(f"  {'.'.join(map(str, chapter_num))}: {filename}")
    
    # Połącz pliki
    print(f"\nŁączenie plików...")
    merge_files(files, output_path)
    
    print(f"\n✅ Gotowe! Plik zapisany w: {output_path}")

if __name__ == "__main__":
    main()