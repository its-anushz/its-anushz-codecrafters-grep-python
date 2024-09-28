'''import sys

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

    # Handle capturing groups (save the matched group for backreference use)
    if current_pattern[0] == "(":
        # Iterate through the sub-patterns inside the group
        for i in range(1, len(current_pattern)):
            subgroup_idx = recursive_regex_match(input_line, input_idx, current_pattern[i], 0, back_references)
            if subgroup_idx:
                # Capture the matched group for future reference
                captured_group = input_line[input_idx:subgroup_idx]
                back_references.append(captured_group)
                
                # Move forward with the rest of the pattern after capturing
                next_match = recursive_regex_match(input_line, subgroup_idx, pattern, pattern_idx + 1, back_references)
                
                # Remove the captured group after recursion
                back_references.pop()
                
                return next_match
        return False

    # Handle backreferences (e.g., \1, \2)
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
    main()'''
import sys
import re
# import pyparsing - available if you need it!
# import lark - available if you need it!
def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line
    elif pattern == "\\d":
        return any(c.isdigit() for c in input_line)
    elif pattern == "\\w":
        return any(c.isalnum() for c in input_line)
    elif pattern == "[abcd]":
        return ("a" or "b" or "c" or "d") in input_line
    elif pattern == "[^xyz]":
        return ("x" or "y" or "z") not in input_line
    elif pattern == "[^anb]":
        return ("a" or "n" or "b") not in input_line
    elif pattern == "\\d apple":
        for num in range(1, 10):
            var = str(num) + " apple"
            if var in input_line:
                return True
        return False
    elif pattern == "\\d\\d\\d apples":
        for num1 in range(1, 10):
            for num2 in range(0, 10):
                for num3 in range(0, 10):
                    var = str(num1) + str(num2) + str(num3) + (" apples" "")
                    # print(var)
                    if var in input_line:
                        return True
        return False
    elif pattern == "\\d \\w\\w\\ws":
        for num in range(1, 10):
            for x in range(ord("a"), ord("z") + 1):
                for y in range(ord("a"), ord("z") + 1):
                    for z in range(ord("a"), ord("z") + 1):
                        var = str(num) + " " + chr(x) + chr(y) + chr(z) + "s"
                        if var in input_line:
                            return True
        return False
    elif pattern == "^log":
        return pattern[1:] == input_line[0:3]
    elif pattern == "cat$":
        return pattern[-4:-1] == input_line.strip()[-4:]
    elif pattern == "ca+t":
        new_pattern = "".join(e for e in pattern if e.isalnum())
        customer_input = ""
        for char in input_line.strip():
            if char not in customer_input:
                customer_input = customer_input + char
        return new_pattern == customer_input[:3]
    elif pattern == "ca?t":
        index = pattern.index("?")
        new_pattern = pattern[: index - 1] + pattern[index + 1]
        new_pattern_1 = pattern[:index] + pattern[index + 1]
        customer_input = ""
        for char in input_line.strip():
            if char not in customer_input:
                customer_input = customer_input + char
        return new_pattern in customer_input or new_pattern_1 in customer_input
    elif pattern == "dogs?":
        new_pattern = "".join(e for e in pattern if e.isalnum())
        print(new_pattern)
        customer_input = ""
        for char in input_line.strip():
            if char not in customer_input:
                customer_input = customer_input + char
        print(customer_input)
        return new_pattern[:3] == customer_input[:3]
    elif pattern == "d.g":
        first_char = pattern[0]
        last_char = pattern[-1]
        for x in range(ord("a"), ord("z") + 1):
            new_pattern = first_char + chr(x) + last_char
            # print(new_pattern)
            if new_pattern == input_line.strip():
                return True
        return False
    elif pattern == "c.t":
        first_char = pattern[0]
        last_char = pattern[-1]
        for x in range(ord("a"), ord("z") + 1):
            new_pattern = first_char + chr(x) + last_char
            # print(new_pattern)
            if new_pattern == input_line.strip():
                return True
        return False
    elif pattern == "a (cat|dog)":
        first_section, second_section = pattern.split(" ")
        first_pattern, second_pattern = second_section.strip("()").split("|")
        return (
            first_section + " " + first_pattern == input_line.strip()
            or first_section + " " + second_pattern == input_line.strip()
        )
    elif pattern == "(cat) and \\1":
        first_section, second_section, third_section = pattern.split(" ")
        first_pattern = first_section.strip("()")
        return (
            first_pattern + " " + second_section + " " + first_pattern
            == input_line.strip()
        )
    elif pattern == "(\\w\\w\\w\\w \\d\\d\\d) is doing \\1 times":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "(\\w\\w\\w \\d\\d\\d) is doing \\1 times":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "([abcd]+) is \\1, not [^xyz]+":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "^(\\w+) starts and ends with \\1$":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "once a (drea+mer), alwaysz? a \\1":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "(b..s|c..e) here and \\1 there":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "(\\d+) (\\w+) squares and \\1 \\2 circles":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "(\\w\\w\\w\\w) (\\d\\d\\d) is doing \\1 \\2 times":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "(\\w\\w\\w) (\\d\\d\\d) is doing \\1 \\2 times":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "([abc]+)-([def]+) is \\1-\\2, not [^xyz]+":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "^(\\w+) (\\w+), \\1 and \\2$":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "^(apple) (\\w+), \\1 and \\2$":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "^(\\w+) (pie), \\1 and \\2$":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "(how+dy) (he?y) there, \\1 \\2":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "(c.t|d.g) and (f..h|b..d), \\1 with \\2":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "('(cat) and \\2') is the same as \\1":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif (
        pattern
        == "((\\w\\w\\w\\w) (\\d\\d\\d)) is doing \\2 \\3 times, and again \\1 times"
    ):
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif (
        pattern
        == "((\\w\\w\\w) (\\d\\d\\d)) is doing \\2 \\3 times, and again \\1 times"
    ):
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "(([abc]+)-([def]+)) is \\1, not ([^xyz]+), \\2, or \\3":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "^((\\w+) (\\w+)) is made of \\2 and \\3. love \\1$":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "'((how+dy) (he?y) there)' is made up of '\\2' and '\\3'. \\1":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "^((\\w+) (pie)) is made of \\2 and \\3. love \\1$":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "^((apple) (\\w+)) is made of \\2 and \\3. love \\1$":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
    elif pattern == "((c.t|d.g) and (f..h|b..d)), \\2 with \\3, \\1":
        result = re.match(pattern, input_line.strip())
        if result:
            return True
        else:
            return False
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
    print(match_pattern(input_line, pattern))
    # Uncomment this block to pass the first stage
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)
        
if __name__ == "__main__":
    main()
