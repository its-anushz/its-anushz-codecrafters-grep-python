def recursive_regex_match(input_line, input_idx, pattern, pattern_idx):
    # Ensure we don't go out of bounds for pattern and input
    if pattern_idx >= len(pattern):
        return input_idx if input_idx == len(input_line) else False

    if pattern[pattern_idx] == ["$"]:
        # Match the end of the string
        if input_idx == len(input_line) and pattern_idx == len(pattern) - 1:
            return input_idx

    # Return False if input is exhausted
    if input_idx >= len(input_line):
        return False

    # Check if it's a capturing group
    if len(pattern[pattern_idx]) > 0 and pattern[pattern_idx][0] == "(":
        for i in range(1, len(pattern[pattern_idx])):
            subgroup_idx = recursive_regex_match(
                input_line, input_idx, pattern[pattern_idx][i], 0
            )
            if subgroup_idx:
                back_references.append(input_line[input_idx:subgroup_idx])
                to_ret = recursive_regex_match(
                    input_line, subgroup_idx, pattern, pattern_idx + 1
                )
                back_references.pop()
                return to_ret
        return False

    # Handle backreferences
    if (
        len(pattern[pattern_idx]) > 1
        and pattern[pattern_idx][0] == "\\"
        and pattern[pattern_idx][1].isnumeric()
    ):
        group_num = int(pattern[pattern_idx][1])
        if group_num - 1 < len(back_references):
            new_pattern = [[x] for x in back_references[group_num - 1]]
            subgroup_idx = recursive_regex_match(input_line, input_idx, new_pattern, 0)
            if subgroup_idx:
                return recursive_regex_match(
                    input_line, subgroup_idx, pattern, pattern_idx + 1
                )
        return False

    # Match current literal character
    if input_line[input_idx] in pattern[pattern_idx]:
        # Handle '+' and '?' quantifiers
        if len(pattern) > pattern_idx + 1 and pattern[pattern_idx + 1] == ["+"]:
            return recursive_regex_match(
                input_line, input_idx + 1, pattern, pattern_idx
            ) or recursive_regex_match(
                input_line, input_idx + 1, pattern, pattern_idx + 2
            )
        if len(pattern) > pattern_idx + 1 and pattern[pattern_idx + 1] == ["?"]:
            return recursive_regex_match(
                input_line, input_idx, pattern, pattern_idx + 2
            ) or recursive_regex_match(
                input_line, input_idx + 1, pattern, pattern_idx + 2
            )
        return recursive_regex_match(
            input_line, input_idx + 1, pattern, pattern_idx + 1
        )

    # Handle '?' quantifier
    if len(pattern) > pattern_idx + 1 and pattern[pattern_idx + 1] == ["?"]:
        return recursive_regex_match(input_line, input_idx, pattern, pattern_idx + 2)

    return False
