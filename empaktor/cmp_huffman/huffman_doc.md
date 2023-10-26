# Documentation of the Huffman encoding algorithm

## Encoding
```py
compress_data(data: str) -> str | str
```

This function takes in a text to encode (str) and returns the encoded text (str) as well as the mapping required to decode it (str).

### The logic
Obtain a dictionnary of unique characters and their associated count from `data`.

Build the Huffman tree using this dictionnary.

Generate the Huffman encoding for each character.

```py
char_freq = dict(Counter(data))
tree = build_tree(char_freq)
codes = generate_huffman(tree)
```

Build the encoded text by iterating on each character of `data` and replacing it with the Huffman encoding for that character:

```py
for char in data:
    output += codes[char]
codes = json.dumps(codes)
return output, codes
```

## Decoding
```py
decode_huffman(encoded_txt: str, codes_map: str) -> str
```

This function takes in 2 parameters, respectively the encoded text (str) and the Huffman encoding map required to decode the text (str).

### The logic
While the length of the encoded text is not 0: 

Search for a sequence in the encoded text that matches with a code in the Huffman encoding map. Then append the corresponding letter to the output string. Finally, remove the sequence from the encoded text.

```py
while len(encoded_txt) > 0:
    for val in codes_map:
        if encoded_txt[0:len(codes_map[val])] == codes_map[val]:
            decoded_txt += val
            encoded_txt = encoded_txt[len(codes_map[val]):]
return decoded_txt
```

## Example
```py
text = "AAAAABBB11111"
encoded_text, huffman_codes = compress_data(text)
print("Encoded text:", encoded_text)
print("Huffman codes:", huffman_codes)
decoded_text = decode_huffman(encoded_text, huffman_codes)
print("Decoded text:", decoded_text)

# This prints
# Encoded text: 111111111110101000000
# Huffman codes: {"1": "0", "B": "10", "A": "11"}
#
# Decoded text: AAAAABBB11111
```