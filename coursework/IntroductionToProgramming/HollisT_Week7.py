
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Course: DSC510
# Week: 7
# Assignment: 7.1 Dictionary Creation
# Author: Tim Hollis
# Date: 10/20/2025
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import string

def add_word(word, word_dict):
    """Adds a word to the dictionary or increments its count."""
    if word in word_dict:
        word_dict[word] += 1
    else:
        word_dict[word] = 1

def process_line(line, word_dict):
    """Processes a line: strips punctuation, normalizes case, splits into words, and adds to dictionary."""
    translator = str.maketrans('', '', string.punctuation)
    cleaned_line = line.translate(translator).lower().strip()
    words = cleaned_line.split()
    for word in words:
        add_word(word, word_dict)

def pretty_print(word_dict):
    """Prints the dictionary in tabular format sorted by frequency (descending)."""
    print(f'\n{"Word":<15}{"Count":>5}')
    print('-' * 20)
    for word, count in sorted(word_dict.items(), key=lambda item: item[1], reverse=True):
        print(f'{word:<15}{count:>5}')

def main():
    """Main function to open file, process lines, and print results."""
    word_count_dict = {}
    try:
        with open('gettysburg.txt', 'r') as fileHandle:
            for line in fileHandle:
                process_line(line, word_count_dict)
        print(f'\nTotal unique words: {len(word_count_dict)}')
        pretty_print(word_count_dict)
    except FileNotFoundError as e:
        print(e)

# Entry point
if __name__ == '__main__':
    main()

