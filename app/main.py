import sys

# Recursive matcher function to handle patterns like \d, \w, and +
def matcher(input_line, input_idx, pattern, pattern_idx):
    if input_idx >= len(input_line) and pattern_idx >= len(pattern):
        return True
    elif input_idx >= len(input_line) or pattern_idx >= len(pattern):
        return False

    if pattern_idx + 1 < len(pattern) and pattern[pattern_idx + 1] == "+":
        char_to_repeat = pattern[pattern_idx]  # The character that should repeat
        # Ensure at least one match
        if input_line[input_idx] != char_to_repeat:
            return False

        # Consume one or more of the same character
        while input_idx < len(input_line) and input_line[input_idx] == char_to_repeat:
            input_idx += 1
        return matcher(input_line, input_idx, pattern, pattern_idx + 2)

    elif input_line[input_idx] == pattern[pattern_idx]:
        return matcher(input_line, input_idx + 1, pattern, pattern_idx + 1)

    return False


def match_pattern(input_line, pattern):
    # Handle patterns that start with ^
    if pattern.startswith("^"):
        return input_line.startswith(pattern[1:])

    # Handle patterns that end with $ (end of string)
    elif pattern.endswith("$"):
        l = len(pattern[:-1])  # length of the pattern without "$"
        return input_line[-l:] == pattern[:-1]

    # Handle negative character groups like [^xyz]
    if pattern.startswith("[^") and pattern.endswith("]"):
        # Extract the characters within the brackets
        char_group = pattern[2:-1]
        # Return True if the input contains any character that is not in the group
        return any(c not in char_group for c in input_line)

    # Handle simple character groups like [xyz]
    if pattern.startswith("[") and pattern.endswith("]"):
        char_group = pattern[1:-1]
        # Return True if any character in the input matches any character in the group
        return any(c in char_group for c in input_line)

    # Use recursive matcher for complex patterns like \d, \w, and +
    return matcher(input_line, 0, pattern, 0)


def main():
    if len(sys.argv) < 3 or sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    pattern = sys.argv[2]
    input_line = sys.stdin.read().strip()  # strip to remove extra newlines

    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
