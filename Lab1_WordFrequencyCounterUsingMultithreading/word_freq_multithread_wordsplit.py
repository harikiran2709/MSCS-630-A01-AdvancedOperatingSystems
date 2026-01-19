"""
Word Frequency Counter Using Multithreading

This script splits the file into N segments by words (not characters), processes each segment in a separate thread, and outputs both intermediate and final word frequency counts.
"""
import sys
import threading
from collections import Counter
import re

def count_words(words, result_list, index):
    freq = Counter(words)
    result_list[index] = freq
    print(f"Thread {index+1} intermediate count: {dict(freq)}\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python word_freq_multithread_wordsplit.py <input_file> <num_segments>")
        sys.exit(1)
    input_file = sys.argv[1]
    try:
        num_segments = int(sys.argv[2])
        if num_segments < 1:
            raise ValueError
    except ValueError:
        print("Number of segments must be a positive integer.")
        sys.exit(1)

    # Read file content
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Split text into words
    all_words = re.findall(r'\b\w+\b', text.lower())
    total_words = len(all_words)
    segment_size = total_words // num_segments
    segments = []
    for i in range(num_segments):
        start = i * segment_size
        end = (i + 1) * segment_size if i != num_segments - 1 else total_words
        segments.append(all_words[start:end])

    # Prepare result list and threads
    results = [None] * num_segments
    threads = []
    for i in range(num_segments):
        t = threading.Thread(target=count_words, args=(segments[i], results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Consolidate results
    final_count = Counter()
    for freq in results:
        final_count.update(freq)

    print("Final consolidated word frequency count:")
    for word, count in final_count.most_common():
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()
