# Documentation of the RLE algorithm

## Encoding
```py
encode_rle(txt: str) -> str
```

This function takes in 1 parameter  that is the text to encode (str) and returns the encoded text (str).

### The logic
Iterate on each character of the string and initialize the count of the current character to 1. 

```py
while i < len(txt):
    count = 1
    char_idx = i
    char = txt[i]
```

Iterate on the rest of the string starting from this character

```py
    while char_idx < len(txt) - 1:
```

If this character is the same as current, count is incremented by 1.

```py
        if txt[char_idx] == txt[char_idx + 1]:
            count += 1
            char_idx += 1
```

Else break the innner loop and append the count (enclosed in a seperator, the hyphen in our case) followed by the character.

```py
        else:
            break
    output += f"-{count}-{char}"
    i = char_idx + 1
return output
```

## Decoding
```py
decode_rle(txt: str) -> str
```

This function takes in 1 parameter that is the encoded text (str )and returns the decoded text (str).

### The logic

Initialize 2 lists to store respectively the counts and the unique characters.

```py
counts = []
chars = []
output = ""
i = 0
```

Iterate on the encoded text. Append the count (this is easily done because the count is enclosed between a seperator) as well as the unique character that follows.

```py
while i < len(txt):
    count = ""
    if txt[i] == "-":
        i += 1
        while not txt[i] == "-":
            count += txt[i]
                counts.append(int(count))
                i += 1
    else:
        chars.append(txt[i])
    i += 1
```

As the 2 lists are equal in length (because there is 1 count per character), we can repeat n times (with n = len(counts)) and append the decoded text to the output

```py
for i in range(len(counts)):
    output += f"{counts[i] * chars[i]}"
return output
```

## Example
```py
text = "AAAAABBB11111"
encoded_text = encode_rle(text)
print("Encoded text:", encoded_text)
decoded_text = decode_rle(encoded_text)
print("Decoded text:", decoded_text)

# This prints
# Encoded text: |5|A|3|B|5|1
#
# Decoded text: AAAAABBB11111
```