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
            return [chr(i) for i in range(256) if chr(i) not in get_real_values(sub_literals)]
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
    if pattern_idx == len(pattern):
        return input_idx  # End of pattern, successful match

    if pattern[pattern_idx] == ["$"]:
        if input_idx == len(input_line):
            return input_idx  # End of input, successful match at the end
        return False

    if input_idx == len(input_line):
        return False  # Reached the end of input but pattern still exists

    current_pattern = pattern[pattern_idx]

    # Handle groups
    if current_pattern[0] == "(":
        for i in range(1, len(current_pattern)):
            subgroup_idx = recursive_regex_match(input_line, input_idx, current_pattern[i], 0, back_references)
            if subgroup_idx:
                back_references.append(input_line[input_idx:subgroup_idx])  # Capture group match
                to_ret = recursive_regex_match(input_line, subgroup_idx, pattern, pattern_idx + 1, back_references)
                back_references.pop()  # Clean up backreferences after recursive call
                return to_ret
        return False

    # Handle backreferences
    if len(current_pattern) > 1 and current_pattern[0] == "\\" and current_pattern[1].isdigit():
        group_num = int(current_pattern[1]) - 1  # Adjust to 0-index
        if group_num < len(back_references):
            backref_match = back_references[group_num]
            if input_line.startswith(backref_match, input_idx):
                return recursive_regex_match(input_line, input_idx + len(backref_match), pattern, pattern_idx + 1, back_references)
        return False

    # Direct character matching
    if input_line[input_idx] in current_pattern:
        if len(pattern) != pattern_idx + 1 and pattern[pattern_idx + 1] == ["+"]:
            return (recursive_regex_match(input_line, input_idx + 1, pattern, pattern_idx, back_references) or
                    recursive_regex_match(input_line, input_idx + 1, pattern, pattern_idx + 2, back_references))

        if len(pattern) != pattern_idx + 1 and pattern[pattern_idx + 1] == ["?"]:
            return (recursive_regex_match(input_line, input_idx, pattern, pattern_idx + 2, back_references) or
                    recursive_regex_match(input_line, input_idx + 1, pattern, pattern_idx + 2, back_references))

        return recursive_regex_match(input_line, input_idx + 1, pattern, pattern_idx + 1, back_references)

    # Optional match (?)
    if len(pattern) != pattern_idx + 1 and pattern[pattern_idx + 1] == ["?"]:
        return recursive_regex_match(input_line, input_idx, pattern, pattern_idx + 2, back_references)

    return False

def match_pattern(input_line, pattern):
    pattern_values = [
        get_real_values(literal) for literal in get_literals_from_pattern(pattern)
    ]
    print(f"Pattern Values: {pattern_values}")  # Debugging line
    if pattern_values[0] == ["^"]:
        return recursive_regex_match(input_line, 0, pattern_values, 1, [])
    else:
        for i in range(len(input_line)):
            if recursive_regex_match(input_line, i, pattern_values, 0, []):
                return True
        return False

def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()
    specialCharactersToValueMap["\\d"] = [str(i) for i in range(10)]
    specialCharactersToValueMap["\\w"] = [
        chr(i) for i in range(ord("a"), ord("z") + 1)
    ]
    specialCharactersToValueMap["\\w"] += [
        chr(i) for i in range(ord("A"), ord("Z") + 1)
    ]
    specialCharactersToValueMap["\\w"] += [
        chr(i) for i in range(ord("0"), ord("9") + 1)
    ]
    specialCharactersToValueMap["\\w"] += ["_"]
    specialCharactersToValueMap["\\\\"] = ["\\"]
    for i in range(10):
        specialCharactersToValueMap["\\" + str(i)] = "\\" + str(i)
    
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # Logs for debugging
    print("Logs from your program will appear here!")

    # Call match_pattern with the correct number of arguments (input_line and pattern)
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)