def remove_duplicate_phrases(strings):
    seen = set()
    unique_strings = []
    
    for string in strings:
        if string not in seen:
            unique_strings.append(string)
            seen.add(string)
    
    return unique_strings

# Example usage
input_strings = [
    "This is the first string.",
    "This is the second string.",
    "This is the first string.",  # Duplicate
    "Another unique string."
]

unique_strings = remove_duplicate_phrases(input_strings)
print(unique_strings)
