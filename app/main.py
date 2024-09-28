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
        return input_idx
    if pattern[pattern_idx] == ["$"]:
        if input_idx == len(input_line) and pattern_idx == len(pattern) - 1:
            return input_idx
    if input_idx == len(input_line):
        return False

    current_pattern = pattern[pattern_idx]

    if current_pattern[0] == "(":
        # Handle groups
        for i in range(1, len(current_pattern)):
            subgroup_idx = recursive_regex_match(input_line, input_idx, current_pattern[i], 0, back_references)
            if subgroup_idx:
                back_references.append(input_line[input_idx:subgroup_idx])
                to_ret = recursive_regex_match(input_line, subgroup_idx, pattern, pattern_idx + 1, back_references)
                back_references.pop()
                return to_ret
        return False
    
    if len(current_pattern) > 1 and current_pattern[0] == "\\" and current_pattern[1].isdigit():
        # Handle backreferences
        group_num = int(current_pattern[1])
        if group_num - 1 < len(back_references):
            new_pattern = [[x] for x in back_references[group_num - 1]]
            subgroup_idx = recursive_regex_match(input_line, input_idx, new_pattern, 0, back_references)
            if subgroup_idx:
                return recursive_regex_match(input_line, subgroup_idx, pattern, pattern_idx + 1, back_references)
        return False

    if input_line[input_idx] in current_pattern:
        if len(pattern) != pattern_idx + 1 and pattern[pattern_idx + 1] == ["+" ]:
            return recursive_regex_match(input_line, input_idx + 1, pattern, pattern_idx, back_references) or recursive_regex_match(input_line, input_idx + 1, pattern, pattern_idx + 2, back_references)
        if len(pattern) != pattern_idx + 1 and pattern[pattern_idx + 1] == ["?"]:
            return recursive_regex_match(input_line, input_idx, pattern, pattern_idx + 2, back_references) or recursive_regex_match(input_line, input_idx + 1, pattern, pattern_idx + 2, back_references)
        return recursive_regex_match(input_line, input_idx + 1, pattern, pattern_idx + 1, back_references)
    
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