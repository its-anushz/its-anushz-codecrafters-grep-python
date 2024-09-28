import sys

def get_literals_from_pattern(pattern):
    """Extract literals from a regex-like pattern."""
    i = 0
    literals = []
    while i < len(pattern):
        if pattern[i] == "\\":
            literals.append(pattern[i:i + 2])
            i += 2
        elif pattern[i] in "[(":
            end_index = pattern.find("]", i) if pattern[i] == "[" else pattern.find(")", i)
            literals.append(pattern[i:end_index + 1])
            i = end_index + 1
        else:
            literals.append(pattern[i])
            i += 1
    return literals

def get_real_values(literal, special_char_map):
    """Get actual values represented by the given literal."""
    if literal == ".":
        return [chr(i) for i in range(256)]
    elif len(literal) == 1:
        return [literal]
    elif literal.startswith("["):
        if literal[1] == "^":
            # Handle negated character classes
            sub_literals = get_literals_from_pattern(literal[2:-1])
            return [chr(i) for i in range(256) if chr(i) not in get_real_values(sub_literals, special_char_map)]
        else:
            # Handle regular character classes
            sub_literals = get_literals_from_pattern(literal[1:-1])
            return list(set(val for sub in sub_literals for val in get_real_values(sub, special_char_map)))
    elif literal.startswith("("):
        # Flatten groups
        sub_groups = literal[1:-1].split("|")
        values = []
        for sub_group in sub_groups:
            values.extend(get_real_values(sub_group, special_char_map))
        return values  # Flatten the result
    else:
        return special_char_map.get(literal, [])

def recursive_regex_match(input_line, input_idx, pattern, pattern_idx, back_references):
    # If pattern fully matched
    if pattern_idx == len(pattern):
        return input_idx  # End of pattern, successful match

    # Handle end-of-line anchor "$"
    if pattern[pattern_idx] == ["$"]:
        if input_idx == len(input_line):
            return input_idx  # Successfully matched at the end
        return False

    # If input is fully consumed, but the pattern is not
    if input_idx == len(input_line):
        return False

    current_pattern = pattern[pattern_idx]

    # Check if the current pattern is empty to avoid accessing an empty list
    if not current_pattern:
        return False

    # Handle capturing groups
    if current_pattern[0] == "(":
        for i in range(1, len(current_pattern)):
            subgroup_idx = recursive_regex_match(input_line, input_idx, current_pattern[i], 0, back_references)
            if subgroup_idx:
                back_references.append(input_line[input_idx:subgroup_idx])  # Capture the match
                next_match = recursive_regex_match(input_line, subgroup_idx, pattern, pattern_idx + 1, back_references)
                back_references.pop()  # Remove the captured reference after recursion
                return next_match
        return False

    # Handle backreferences
    if len(current_pattern) > 1 and current_pattern[0] == "\\" and current_pattern[1].isdigit():
        group_num = int(current_pattern[1]) - 1  # Adjust for 0-indexing
        if group_num < len(back_references):
            backref_str = back_references[group_num]
            backref_len = len(backref_str)
            # Check if the substring matches the backreference
            if input_line[input_idx:input_idx + backref_len] == backref_str:
                return recursive_regex_match(input_line, input_idx + backref_len, pattern, pattern_idx + 1, back_references)
        return False

    # Direct character matching
    if input_line[input_idx] in current_pattern:
        # Handle "+" quantifier (one or more)
        if len(pattern) != pattern_idx + 1 and pattern[pattern_idx + 1] == ["+"]:
            return (recursive_regex_match(input_line, input_idx + 1, pattern, pattern_idx, back_references) or
                    recursive_regex_match(input_line, input_idx + 1, pattern, pattern_idx + 2, back_references))

        # Handle "?" quantifier (zero or one)
        if len(pattern) != pattern_idx + 1 and pattern[pattern_idx + 1] == ["?"]:
            return (recursive_regex_match(input_line, input_idx, pattern, pattern_idx + 2, back_references) or
                    recursive_regex_match(input_line, input_idx + 1, pattern, pattern_idx + 2, back_references))

        # Move to the next character if matched
        return recursive_regex_match(input_line, input_idx + 1, pattern, pattern_idx + 1, back_references)

    # Optional match ("?")
    if len(pattern) != pattern_idx + 1 and pattern[pattern_idx + 1] == ["?"]:
        return recursive_regex_match(input_line, input_idx, pattern, pattern_idx + 2, back_references)

    return False

def match_pattern(input_line, pattern):
    special_char_map = {
        "\\d": [str(i) for i in range(10)],
        "\\w": [chr(i) for i in range(ord("a"), ord("z") + 1)] + [chr(i) for i in range(ord("A"), ord("Z") + 1)] + [str(i) for i in range(10)] + ["_"],
        "\\\\": ["\\"]
    }
    
    pattern_values = [
        get_real_values(literal, special_char_map) for literal in get_literals_from_pattern(pattern)
    ]
    
    if pattern_values[0] == ["^"]:
        return recursive_regex_match(input_line, 0, pattern_values, 1, [])
    else:
        for i in range(len(input_line)):
            if recursive_regex_match(input_line, i, pattern_values, 0, []):
                return True
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: <program> -E <pattern>")
        exit(1)

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    # Logs for debugging
    print("Logs from your program will appear here!")

    if match_pattern(input_line.strip(), pattern):
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
