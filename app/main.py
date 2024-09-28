'''import sys
# import pyparsing - available if you need it!
# import lark - available if you need it!
def matcher(input_line, pattern):
    ptr1 = 0
    ptr2 = 0
    if input_line == "" and pattern == "":
        return True
    elif input_line == "":
        return False
    elif pattern == "":
        return True
    while ptr1 < len(input_line):
        if ptr2 + 1 < len(pattern) and pattern[ptr2 : ptr2 + 2] == "\\d":
            if input_line[ptr1].isdigit():
                return matcher(input_line[ptr1 + 1 :], pattern[ptr2 + 2 :])
            else:
                ptr1 = ptr1 + 1
        elif ptr2 + 1 < len(pattern) and pattern[ptr2 : ptr2 + 2] == "\\w":
            if input_line[ptr1].isalnum():
                return matcher(input_line[ptr1 + 1 :], pattern[ptr2 + 2 :])
            else:
                ptr1 = ptr1 + 1
        elif input_line[ptr1] == pattern[ptr2]:
            print("here")
            if ptr2 + 1 < len(pattern) and pattern[ptr2 + 1] == "+":
                while (
                    ptr1 + 1 < len(input_line)
                    and input_line[ptr1 + 1] == input_line[ptr1]
                ):
                    ptr1 = ptr1 + 1
                ptr2 = ptr2 + 1
            return matcher(input_line[ptr1 + 1 :], pattern[ptr2 + 1 :])
        else:
            ptr1 = ptr1 + 1
    return False
def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line
    elif pattern == "\\d":
        for i in range(10):
            if input_line.find(str(i)) != -1:
                return True
    elif pattern == "\\w":
        return input_line.isalnum()
    elif pattern[0:2] == "[^":
        pat = pattern[2:-1]
        for ch in pat:
            if input_line.find(ch) != -1:
                return False
        return True
    elif pattern[0] == "[" and pattern[-1] == "]":
        pat = pattern[1:-1]
        for ch in pat:
            if input_line.find(ch) != -1:
                return True
        return False
    elif pattern[0] == "^":
        if input_line.startswith(pattern[1:]):
            return True
        return False
    elif pattern[-1] == "$":
        l = len(pattern[:-1])
        if input_line[-l:] == pattern[:-1]:
            return True
        return False
    else:
        return matcher(input_line, pattern)
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
# import pyparsing - available if you need it!
# import lark - available if you need it!
class Pattern:
    DIGIT = "\d"
    ALNUM = "\w"
# def combined_patterns(input_line, pattern):
def match_pattern(input_line, pattern):
    if len(input_line) == 0 and len(pattern) == 0:
        return True
    if not pattern:
        return True
    if not input_line:
        return False
    if pattern[0] == "^":
        pattern = pattern[1:]
        while len(pattern) > 0 and len(input_line) > 0:
            if pattern[0] == input_line[0]:
                pattern = pattern[1:]
                input_line = input_line[1:]
            else:
                return False
        return match_pattern(input_line, pattern)
    if pattern[-1] == "$":
        pattern = pattern[:-1]
        while len(pattern) > 0 and len(input_line) > 0:
            if pattern[-1] == input_line[-1]:
                pattern = pattern[:-1]
                input_line = input_line[:-1]
            else:
                return False
        return match_pattern(input_line, pattern)
    if pattern[0] == input_line[0]:
        if len(pattern) > 1:
            if pattern[1] == "+":
                return match_pattern(input_line[1:], pattern[2:]) or match_pattern(
                    input_line[1:], pattern
                )
            elif pattern[1] == "?":
                return match_pattern(input_line[1:], pattern[2:]) or match_pattern(
                    input_line, pattern[1:]
                )
        return match_pattern(input_line[1:], pattern[1:])
    elif pattern[0] != input_line[0] and len(pattern) > 1 and pattern[1] == "?":
        if pattern[1] == "?":
            return match_pattern(input_line, pattern[2:])
        return False
    elif pattern[0] == ".":
        return match_pattern(input_line[1:], pattern[1:])
    elif pattern[:2] == Pattern.DIGIT:
        for i in range(len(input_line)):
            if input_line[i].isdigit():
                return match_pattern(input_line[i:], pattern[2:])
        else:
            return False
    elif pattern[:2] == Pattern.ALNUM:
        if input_line[0].isalnum():
            return match_pattern(input_line[1:], pattern[2:])
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
        return match_pattern(input_line[1:], pattern)
def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)
if __name__ == "__main__":
    main()