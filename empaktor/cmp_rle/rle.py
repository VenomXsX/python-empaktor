sep = "¶"

def encode_rle(txt: str) -> str:
    output = ""
    i = 0
    while i < len(txt):
        count = 1
        char_idx = i
        char = txt[i]
        while char_idx < len(txt) - 1:
            if txt[char_idx] == txt[char_idx + 1]:
                count += 1
                char_idx += 1
            else:
                break
        output += f"{sep}{count}{sep}{char}"
        # Take off from the next unique char
        i = char_idx + 1
    return output


def decode_rle(txt: str) -> str:
    counts = []
    chars = []
    output = ""
    i = 0
    while i < len(txt):
        count = ""
        if txt[i] == sep:
            i += 1
            while not txt[i] == sep:
                count += txt[i]
                counts.append(int(count))
                i += 1
        else:
            chars.append(txt[i])
        i += 1
    for i in range(len(counts)):
        output += f"{counts[i] * chars[i]}"
    return output
