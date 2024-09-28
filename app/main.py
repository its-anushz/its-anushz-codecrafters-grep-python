import sys
import re

class Pattern:
    DIGIT = r"\d"
    ALNUM = r"\w"

def match_pattern(input_line, pattern, captured_groups=None):
    if captured_groups is None:
        captured_groups = {}

    # Handle backreference (\1)
    if r"\1" in pattern:
        # Fetch the first captured group
        captured_group = captured_groups.get(1)
        if captured_group:
            backref_pattern = pattern.replace(r"\1", captured_group)
            return match_pattern(input_line, backref_pattern, captured_groups)
        else:
            return False

    # Handle capturing group (parentheses)
    if pattern.startswith("(") and ")" in pattern:
        group_content = pattern[1:pattern.index(")")]
        remaining_pattern = pattern[pattern.index(")") + 1:]
        
        match_obj = re.match(group_content, input_line)
        if match_obj:
            captured_groups[1] = match_obj.group(0)
            return match_pattern(input_line[match_obj.end():], remaining_pattern, captured_groups)
        else:
            return False

    # Handle start-of-string anchor
    if pattern[0] == "^":
        pattern = pattern[1:]
        return input_line.startswith(pattern)

    # Handle end-of-string anchor
    if pattern[-1] == "$":
        pattern = pattern[:-1]
        return input_line.endswith(pattern)

    # Handle other special regex elements (e.g., `+`, `.`, character classes)
    if pattern[0] == input_line[0]:
        if len(pattern) > 1:
            if pattern[1] == "+":
                return match_pattern(input_line[1:], pattern[2:], captured_groups) or match_pattern(
                    input_line[1:], pattern, captured_groups
                )
            elif pattern[1] == "?":
                return match_pattern(input_line[1:], pattern[2:], captured_groups) or match_pattern(
                    input_line, pattern[1:], captured_groups
                )
        return match_pattern(input_line[1:], pattern[1:], captured_groups)

    elif pattern[0] == ".":
        return match_pattern(input_line[1:], pattern[1:], captured_groups)

    elif pattern[:2] == Pattern.DIGIT:
        for i in range(len(input_line)):
            if input_line[i].isdigit():
                return match_pattern(input_line[i:], pattern[2:], captured_groups)
        else:
            return False

    elif pattern[:2] == Pattern.ALNUM:
        if input_line[0].isalnum():
            return match_pattern(input_line[1:], pattern[2:], captured_groups)
        else:
            return False

    # Handle character classes like [abc]
    elif pattern[0] == "[" and "]" in pattern:
        class_content = pattern[1:pattern.index("]")]
        remaining_pattern = pattern[pattern.index("]") + 1:]
        if input_line[0] in class_content:
            return match_pattern(input_line[1:], remaining_pattern, captured_groups)
        else:
            return False

    return False

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
