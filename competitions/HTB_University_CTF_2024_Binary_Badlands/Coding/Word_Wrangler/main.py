

# Input the text as a single string
input_text = input()  # Example: "The quick brown fox jumps over the lazy dog."

# Write your solution below and make sure to print the most common word
words = (''.join([l for l in input_text.lower() if l.islower() or l == ' '])).split(' ')

from collections import Counter
counter = Counter(words)

print(counter.most_common(1)[0][0])
