
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Course: DSC510
# Week: 8
# Assignment: 8.1 Dictionary File Output
# Author: Tim Hollis
# Date: 10/28/2025
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ==============================Change Control Log:===================================
# Change #: 1
# Change: Replaced screen output with file output for dictionary results.
# Lines Affected: 88-95
# Date of Change: 10/28/2025
# Author: Tim Hollis
# Change Approved by: Tim Hollis
# Date Moved to Production: 10/28/2025

# Change #: 2
# Change: Added process_file() to write sorted word counts to user-specified file.
# Lines Affected: 72-83
# Date of Change: 10/28/2025
# Author: Tim Hollis
# Change Approved by: Tim Hollis
# Date Moved to Production: 10/28/2025

# Change #: 3
# Change: Modified main() to prompt for filename and write total word count to file.
# Lines Affected: 100-125
# Date of Change: 10/28/2025
# Author: Tim Hollis
# Change Approved by: Tim Hollis
# Date Moved to Production: 10/28/2025

# Change #: 4
# Change: Implemented dual file access (main and process_file)
# Lines Affected: 72-83, 100-125
# Date of Change: 10/28/2025
# Author: Tim Hollis
# Change Approved by: Tim Hollis
# Date Moved to Production: 10/28/2025

# Change #: 5
# Change: Added try blocks for both input and output file handling.
# Lines Affected: 73-83, 100-125, 86-96
# Date of Change: 10/28/2025
# Author: Tim Hollis
# Change Approved by: Tim Hollis
# Date Moved to Production: 10/28/2025

# Change #: 6
# Change: Added automatic processing flow with post-processing view option
# Lines Affected: 100-125
# Date of Change: 10/28/2025
# Author: Tim Hollis
# Change Approved by: Tim Hollis
# Date Moved to Production: 10/28/2025

# Change #: 7
# Change: Added read_output_file() function to display saved output files
# Lines Affected: 86-96
# Date of Change: 10/28/2025
# Author: Tim Hollis
# Change Approved by: Tim Hollis
# Date Moved to Production: 10/28/2025

# Change #: 8
# Change: Modified file writing strategy to use separate write/append operations
# Lines Affected: 100-125
# Date of Change: 10/28/2025
# Author: Tim Hollis
# Change Approved by: Tim Hollis
# Date Moved to Production: 10/28/2025

# Change #: 9
# Change: Enhanced sorting to display words alphabetically when counts are equal
# Lines Affected: 79-80
# Date of Change: 10/28/2025
# Author: Tim Hollis
# Change Approved by: Tim Hollis
# Date Moved to Production: 10/28/2025

# Change #: 10
# Change: Added filename validation loop with overwrite warning
# Lines Affected: 84-98
# Date of Change: 10/28/2025
# Author: Tim Hollis
# Change Approved by: Tim Hollis
# Date Moved to Production: 10/28/2025

# Change #: 11
# Change: Added timestamped header to output file
# Lines Affected: 112-115
# Date of Change: 10/28/2025
# Author: Tim Hollis
# Change Approved by: Tim Hollis
# Date Moved to Production: 10/28/2025
# ====================================================================================

import string
import os
from datetime import datetime


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


def process_file(word_dict, filename):
    """Prints the dictionary to a file in tabular format sorted by frequency (descending), then alphabetically."""
    try:
        with open(filename, 'a') as outFile:
            outFile.write('\nWord Frequency Table\n')
            outFile.write(f'\n{"Word":<15}{"Count":>5}\n')
            outFile.write('-' * 20 + '\n')
            for word, count in sorted(word_dict.items(), key=lambda item: (-item[1], item[0])):
                outFile.write(f'{word:<15}{count:>5}\n')
    except IOError as e:
        print(f"Error writing to file: {e}")


def read_output_file(filename):
    """Displays the contents of the specified file."""
    try:
        with open(filename, 'r') as file:
            contents = file.read()
            print("\n===== File Contents =====\n")
            print(contents)
    except FileNotFoundError:
        print("File not found. Please check the name and try again.")
    except IOError as e:
        print(f"Error reading file: {e}")


def get_valid_filename():
    """Prompts user for a valid .txt filename and handles overwrite warnings."""
    while True:
        filename = input(
            "Enter the filename in the .txt format to save the output (e.g., 'output.txt'): ").strip()
        if not filename.endswith('.txt'):
            print("Filename must end with '.txt'. Please try again.")
            continue
        if os.path.exists(filename):
            confirm = input(
                f"'{filename}' already exists. Overwrite? (enter y or yes to overwrite, any other to rename): ").lower()
            if confirm not in ['y', 'yes']:
                print("Please enter a new filename.")
                continue
        return filename


def main():
    """Main function to open file, process lines, and write results to a new file."""
    word_count_dict = {}
    try:
        with open('gettysburg.txt', 'r') as fileHandle:
            for line in fileHandle:
                process_line(line, word_count_dict)
    except FileNotFoundError as e:
        print(f"Input file error: {e}")
        return

    try:
        output_filename = get_valid_filename()
        with open(output_filename, 'w') as outFile:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            outFile.write('Gettysburg Word Count Report\n')
            outFile.write(f'Generated on: {timestamp}\n\n')
            outFile.write(f'Total unique words: {len(word_count_dict)}\n')
        process_file(word_count_dict, output_filename)
        print(f"Output successfully written to '{output_filename}'.")

        view_choice = input(
            "\nWould you like to view the output file? (enter y or yes to view, all other responses end program): ").lower()
        if view_choice in ['yes', 'y']:
            read_output_file(output_filename)
        else:
            print("Thank you for using the program. Bye for now!")

    except IOError as e:
        print(f"Output file error: {e}")


# Entry point
if __name__ == '__main__':
    main()

