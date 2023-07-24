import os
import string
from collections import Counter

def remove_punctuation(text):
    translator = str.maketrans("", "", string.punctuation + "‘’…“”–")
    return text.translate(translator)

def is_numeric(word):
    try:
        float(word)
        return True
    except ValueError:
        return False

def find_hapaxes(directory_path):
    all_words = []
    file_word_counts = {}
    word_occurrences = {}
    
    for filename in sorted(os.listdir(directory_path)):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read().lower()
                text_without_punctuation = remove_punctuation(text)
                words = text_without_punctuation.split()
                all_words.extend(words)
                word_count = Counter(words)
                file_word_counts[filename] = len(words)
                
                for word in set(words):
                    if not is_numeric(word):
                        if word not in word_occurrences:
                            word_occurrences[word] = [filename]
                        else:
                            word_occurrences[word].append(filename)
    
    all_word_count = Counter(all_words)
    total_words_all_files = sum(file_word_counts.values())
    total_hapaxes_all_files = len([word for word in all_word_count if all_word_count[word] == 1 and not is_numeric(word) and word != '0'])
    percentage_hapaxes_all_files = (total_hapaxes_all_files / total_words_all_files) * 100

    with open("/Users/mvanoostendorp/Dropbox/Scripts/hapax.txt", 'w', encoding='utf-8') as output_file:
        for filename in sorted(file_word_counts.keys()):
            total_file_words = file_word_counts[filename]
            hapaxes_in_file = [word for word in word_occurrences if word in word_occurrences and len(word_occurrences[word]) == 1 and filename in word_occurrences[word] and not is_numeric(word) and word != '0']
            total_file_hapaxes = len(hapaxes_in_file)
            percentage_hapaxes = (total_file_hapaxes / total_file_words) * 100
            output_file.write(f"{os.path.splitext(filename)[0]} (Total Words: {total_file_words}, Total Hapaxes: {total_file_hapaxes}, Percentage of Hapaxes: {percentage_hapaxes:.2f}%)\n")

        output_file.write("\nAlphabetic List of Hapaxes:\n")
        sorted_hapaxes = sorted(all_word_count.keys())
        for hapax in sorted_hapaxes:
            if hapax in word_occurrences and len(word_occurrences[hapax]) == 1 and not is_numeric(hapax) and hapax != '0':
                filename = word_occurrences[hapax][0]
                output_file.write(f"{hapax} ({os.path.splitext(filename)[0]})\n")

        output_file.write("\nSummary:\n")
        output_file.write(f"Total Words in All Files: {total_words_all_files}\n")
        output_file.write(f"Total Hapaxes in All Files: {total_hapaxes_all_files}\n")
        output_file.write(f"Percentage of Hapaxes in All Files: {percentage_hapaxes_all_files:.2f}%\n")

if __name__ == "__main__":
    directory_path = "/Users/mvanoostendorp/Dropbox/Scripts/tandeloos/"
    find_hapaxes(directory_path)
