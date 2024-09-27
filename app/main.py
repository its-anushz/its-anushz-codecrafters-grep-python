import sys

# Recursive matcher function to handle patterns like \d, \w, and +
def matcher(input_line, input_idx, pattern, pattern_idx):
    if input_idx == len(input_line) and pattern_idx == len(pattern):
        return True
    elif input_idx == len(input_line):
        return False

    # Handle special cases for \d (digit)
    if pattern[pattern_idx : pattern_idx + 2] == "\\d" and input_line[input_idx].isdigit():
        return matcher(input_line, input_idx + 1, pattern, pattern_idx + 2)

    # Handle special cases for \w (alphanumeric)
    elif pattern[pattern_idx : pattern_idx + 2] == "\\w" and input_line[input_idx].isalnum():
        return matcher(input_line, input_idx + 1, pattern, pattern_idx + 2)

    # Handle the "+" quantifier (one or more)
    elif pattern_idx + 1 < len(pattern) and pattern[pattern_idx + 1] == "+":
        if input_line[input_idx] == pattern[pattern_idx]:
            # Match one or more occurrences: Try matching more occurrences or move to the next pattern character
            return matcher(input_line, input_idx + 1, pattern, pattern_idx) or matcher(input_line, input_idx + 1, pattern, pattern_idx + 2)
        else:
            return False

    # Handle character matches
    elif input_line[input_idx] == pattern[pattern_idx]:
        return matcher(input_line, input_idx + 1, pattern, pattern_idx + 1)

    return False
    
def match_pattern(input_line, pattern):
    # Handle patterns that start with ^
    if pattern.startswith("^"):
        return input_line.startswith(pattern[1:])

    # Handle patterns that end with $
    elif pattern.endswith("$"):
        l = len(pattern[:-1])  # Length of the pattern without "$"
        return input_line[-l:] == pattern[:-1]

    # Handle negative character groups like [^xyz]
    if pattern.startswith("[^") and pattern.endswith("]"):
        char_group = pattern[2:-1]  # Extract the characters within the brackets
        return any(c not in char_group for c in input_line)  # Match if any character is not in the group

    # Handle normal character groups like [xyz]
    if pattern.startswith("[") and pattern.endswith("]"):
        char_group = pattern[1:-1]
        return any(c in char_group for c in input_line)

    # Use the recursive matcher for complex patterns like \d, \w, and +
    return matcher(input_line, 0, pattern, 0)

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    pattern = sys.argv[2]
    input_line = sys.stdin.read().strip()  # Strip to remove extra newlines

    # Uncomment this for debugging purposes
    # print(f"Input: {input_line}, Pattern: {pattern}")

    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
