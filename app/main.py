import sys
import re

class Pattern:
    DIGIT = r"\d"
    ALNUM = r"\w"

def match_pattern(input_line, pattern, captured_group=None):
    # Handle empty pattern and input
    if len(input_line) == 0 and len(pattern) == 0:
        return True
    if not pattern:
        return True
    if not input_line:
        return False

    # Handle backreference (\1)
    if pattern.startswith(r"\1"):
        if captured_group and input_line.startswith(captured_group):
            return match_pattern(input_line[len(captured_group):], pattern[2:], captured_group)
        else:
            return False

    # Handle capturing group (parentheses)
    if pattern.startswith("(") and ")" in pattern:
        group_content = pattern[1:pattern.index(")")]
        remaining_pattern = pattern[pattern.index(")") + 1:]
        for i in range(1, len(input_line) + 1):
            if match_pattern(input_line[i:], remaining_pattern, input_line[:i]):
                return True
        return False

    # Handle start-of-string anchor
    if pattern[0] == "^":
        pattern = pattern[1:]
        while len(pattern) > 0 and len(input_line) > 0:
            if pattern[0] == input_line[0]:
                pattern = pattern[1:]
                input_line = input_line[1:]
            else:
                return False
        return match_pattern(input_line, pattern)

    # Handle end-of-string anchor
    if pattern[-1] == "$":
        pattern = pattern[:-1]
        while len(pattern) > 0 and len(input_line) > 0:
            if pattern[-1] == input_line[-1]:
                pattern = pattern[:-1]
                input_line = input_line[:-1]
            else:
                return False
        return match_pattern(input_line, pattern)

    # Handle other special regex elements (e.g., `+`, `.`, character classes)
    if pattern[0] == input_line[0]:
        if len(pattern) > 1:
            if pattern[1] == "+":
                return match_pattern(input_line[1:], pattern[2:], captured_group) or match_pattern(
                    input_line[1:], pattern, captured_group
                )
            elif pattern[1] == "?":
                return match_pattern(input_line[1:], pattern[2:], captured_group) or match_pattern(
                    input_line, pattern[1:], captured_group
                )
        return match_pattern(input_line[1:], pattern[1:], captured_group)

    elif pattern[0] != input_line[0] and len(pattern) > 1 and pattern[1] == "?":
        if pattern[1] == "?":
            return match_pattern(input_line, pattern[2:], captured_group)
        return False

    elif pattern[0] == ".":
        return match_pattern(input_line[1:], pattern[1:], captured_group)

    elif pattern[:2] == Pattern.DIGIT:
        for i in range(len(input_line)):
            if input_line[i].isdigit():
                return match_pattern(input_line[i:], pattern[2:], captured_group)
        else:
            return False

    elif pattern[:2] == Pattern.ALNUM:
        if input_line[0].isalnum():
            return match_pattern(input_line[1:], pattern[2:], captured_group)
        else:
            return False

    elif pattern[0] == "[" and pattern[-1] == "]":
        if pattern[1] == "^":
            chrs = list(pattern[2:-1])
            for c in chrs:
                if c in input_line:
                    return False
            return True
        chrs = list(pattern[1:-1])
        for c in chrs:
            if c in input_line:
                return True
        return False

    else:
        return match_pattern(input_line[1:], pattern, captured_group)

def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read().strip()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
