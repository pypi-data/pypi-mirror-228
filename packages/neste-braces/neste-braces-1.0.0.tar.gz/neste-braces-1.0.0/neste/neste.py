import re,sys


def render(cont: str):
    error = False
    tokens = re.split(r"([\{\(\}\)\[\];\n])",cont)
    tokens = [t.strip() for t in tokens if t.strip()]
    indent = 0

    stack = []
    enders = {
        "{" : "}",
        "(" : ")",
        "[" : "]"
    }

    # simplify round, merge () and single ;

    for i,t in enumerate(tokens):
        if not t:
            continue
        # last char would be index out of range
        if i == len(tokens) - 1:
            break
        
        if t in enders and tokens[i+1] == enders[t]:
            tokens[i] = t + tokens[i+1]
            tokens[i+1] = None
        if t == ";" and tokens[i-1] and ";" not in tokens[i-1]:
            tokens[i] = None
            tokens[i-1] = tokens[i-1]+" ;"

    # remove nones
    tokens = [t for t in tokens if t]


    for t in tokens:
        t = t.strip()
        if not t:
            continue

        brace = t.strip(" ;")
        if brace == "}" or brace == ")" or brace == ']':
            indent -= 1
            got = stack.pop()
            expected = enders[got]
            if brace != expected:
                print("ERROR: Expected", expected, "got", t)


        print(indent * "  " + t)

        if brace == "{" or brace == "(" or brace == "[":
            indent += 1
            stack.append(brace)

    if stack:
        print("Stack was not empty in the end:", stack)
        error = True

    return error
        
def main():
    if len(sys.argv) == 1:
        cont = input()
    else:
        cont = open(sys.argv[1]).read()
    err = render(cont)
    # broken syntax, return error
    if err:
        sys.exit(1)

if __name__ == "__main__":
    main()