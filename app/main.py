'''import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line
    elif pattern == "\\d":
        return any(c.isdigit() for c in input_line)
    elif pattern == "\\w":
        return any(c.isalnum() for c in input_line)
    elif pattern[0] == "[" and pattern[-1] == "]":
        if pattern[1] == "^":
            return not any(char in pattern[1:-1] for char in input_line)
        return any(char in pattern[1:-1] for char in input_line)
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    if match_pattern(input_line, pattern):
          exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()'''

import sys

# Recursive matcher function to handle patterns like \d and \w
def matcher(input_line, pattern):
    ptr1 = 0
    ptr2 = 0

    if input_line == "" and pattern == "":
        return True
    elif input_line == "" and pattern != "":
        return False
    elif input_line != "" and pattern == "":
        return True

    while ptr1 < len(input_line) and ptr2 < len(pattern):
        if ptr2 + 1 < len(pattern) and pattern[ptr2:ptr2 + 2] == "\\d":
            if input_line[ptr1].isdigit():
                return matcher(input_line[ptr1 + 1:], pattern[ptr2 + 2:])
            else:
                ptr1 += 1
        elif ptr2 + 1 < len(pattern) and pattern[ptr2:ptr2 + 2] == "\\w":
            if input_line[ptr1].isalnum():
                return matcher(input_line[ptr1 + 1:], pattern[ptr2 + 2:])
            else:
                ptr1 += 1
        elif input_line[ptr1] == pattern[ptr2]:
            return matcher(input_line[ptr1 + 1:], pattern[ptr2 + 1:])
        else:
            ptr1 += 1

    return False


def match_pattern(input_line, pattern):
    # Handle patterns that start with ^
    if pattern.startswith("^"):
        return input_line.startswith(pattern[1:])

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

    # Use recursive matcher for complex patterns like \d, \w
    return matcher(input_line, pattern)


def main():
    if len(sys.argv) < 3 or sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    pattern = sys.argv[2]
    input_line = sys.stdin.read().strip()  # strip to remove extra newlines

    # Uncomment this for debugging purposes
    # print(f"Input: {input_line}, Pattern: {pattern}")

    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()

