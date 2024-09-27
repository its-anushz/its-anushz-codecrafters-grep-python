import sys

def matcher(input_line, input_idx, pattern, pattern_idx):
    # Base case: If both input and pattern are exhausted, return True
    if input_idx == len(input_line) and pattern_idx == len(pattern):
        return True
    # If the pattern is exhausted but input is not, return False
    if pattern_idx == len(pattern):
        return False
    # If the input is exhausted but the pattern isn't, return False
    if input_idx == len(input_line):
        return False

    # Handle the '+' quantifier
    if pattern_idx + 1 < len(pattern) and pattern[pattern_idx + 1] == '+':
        char_to_repeat = pattern[pattern_idx]
        # Match at least one occurrence
        if input_line[input_idx] == char_to_repeat:
            # Move to the next character in the input
            input_idx += 1
            # Try to match more characters with the same char
            while input_idx < len(input_line) and input_line[input_idx] == char_to_repeat:
                if matcher(input_line, input_idx, pattern, pattern_idx + 2):
                    return True
                input_idx += 1
            # After the while loop, check if the first character was matched
            return True
        return False

    # Handle \d (digit) and \w (word character)
    if pattern[pattern_idx] == "\\d":
        if input_line[input_idx].isdigit():
            return matcher(input_line, input_idx + 1, pattern, pattern_idx + 2)
        else:
            return False
    elif pattern[pattern_idx] == "\\w":
        if input_line[input_idx].isalnum():
            return matcher(input_line, input_idx + 1, pattern, pattern_idx + 2)
        else:
            return False

    # Handle character matches
    if input_line[input_idx] == pattern[pattern_idx]:
        return matcher(input_line, input_idx + 1, pattern, pattern_idx + 1)

    return False

def match_pattern(input_line, pattern):
    # Handle patterns that start with ^
    if pattern.startswith("^"):
        return input_line.startswith(pattern[1:])

    # Handle patterns that end with $ (end of string)
    if pattern.endswith("$"):
        l = len(pattern[:-1])  # length of the pattern without "$"
        return input_line[-l:] == pattern[:-1]

    # Handle negative character groups like [^xyz]
    if pattern.startswith("[^") and pattern.endswith("]"):
        char_group = pattern[2:-1]
        return any(c not in char_group for c in input_line)

    # Handle simple character groups like [xyz]
    if pattern.startswith("[") and pattern.endswith("]"):
        char_group = pattern[1:-1]
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
