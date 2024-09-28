import sys
import re

def match_backreference(input_line, pattern):
    # Use re.match to find matches with capturing groups
    match = re.match(r"(.*?)\((.*?)\)(.*?)\\1", pattern)

    if match:
        # Deconstruct the pattern into parts
        before_group = match.group(1)
        captured_group = match.group(2)
        after_backreference = match.group(3)
        
        # Look for the exact match with the input line
        if input_line.startswith(before_group):
            input_line = input_line[len(before_group):]
            if input_line.startswith(captured_group):
                input_line = input_line[len(captured_group):]
                if input_line.startswith(after_backreference):
                    return True
    return False

def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read().strip()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # Try matching the pattern with backreference
    if match_backreference(input_line, pattern):
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
