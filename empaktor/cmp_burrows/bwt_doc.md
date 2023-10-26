# Documentation for the Burrows Wheeler Transform

## Encoding
```py
transform_bwt(data: str) -> str | int
```

This function takes in 1 parameter that is the text to transform (str) and returns the transformed text (str).

### The logic
Obtain all rotations of `data` and store them in a table.
The encoded text is the last column of the table, and the key is the index of the row containing `data`:

```py
data = data.strip()
table = []
for i in range(len(data)):
    data = data[-1] + data[:-1]
    table.append(data)
table = sorted(table)
key = table.index(data)
output = ""
for i in range(len(table)):
    output += table[i][-1]
return output, key
```
## Decoding
```py
inverse_bwt(transformed_data: str, key: int) -> str
```

This function takes in 2 parameters, respectively the transformed data (str) and the key (int).

### The logic
Initialize an empty table with n columns (n = len(transformed_data)):

```py
table = [""] * len(transformed_data)
```

Append the transformed text to the last empty column in the table, then sort the table:

```py
for _ in range(len(transformed_data)):
    table = [transformed_data[i] + table[i]
            for i in range(len(transformed_data))]
    table = sorted(table)
```

The decoded text is the key-th row:

```py
output = table[key]
return output
```

## Example
```py
text = "AAAAABBB11111"
encoded_text, key = transform_bwt(text)
print("Encoded text:", encoded_text)
print("Key:", key)
decoded_text = inverse_bwt(encoded_text, key)
print("Decoded text:", decoded_text)

# This prints
# Encoded text: B11111AAAABBA
# Key; 5
#
# Decoded text: AAAAABBB11111
```