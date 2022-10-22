def is_balanced(string):
    """
    A string with no braces is balanced:

    >>> is_balanced("abc")
    True

    A string with a non closed brace is unbalanced:

    >>> is_balanced("()(")
    False

    >>> is_balanced(")(")
    False

    >>> is_balanced("{")
    False

    >>> is_balanced("}{")
    False

    Trying to close an unmatching brace is considered unbalanced:

    >>> is_balanced("{)")
    False

    >>> is_balanced("(}")
    False

    A string with all matching braces is balanced:

    >>> is_balanced("((){})(){(){}}")
    True
    """
    from balanced_rlmeta import Balanced, MatchError
    try:
        Balanced().run("string", string)
        return True
    except MatchError:
        return False
    pairs = Pairs([
        ("(", ")"),
        ("{", "}"),
    ])
    open_stack = []
    for character in string:
        if pairs.is_open(character):
            open_stack.append(character)
        elif pairs.is_closing(character):
            if open_stack and pairs.is_matching(open_stack[-1], character):
                open_stack.pop(-1)
            else:
                return False
    return len(open_stack) == 0

class Pairs:

    def __init__(self, pairs):
        self.map = {}
        for opening, closing in pairs:
            self.map[closing] = opening

    def is_open(self, character):
        return character in self.map.values()

    def is_closing(self, character):
        return character in self.map.keys()

    def is_matching(self, opening, closing):
        return self.map[closing] == opening

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("ok")
