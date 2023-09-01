def char_range(start, end, step=1):
    for char in range(ord(start), ord(end) + 1, step):
        yield chr(char)
