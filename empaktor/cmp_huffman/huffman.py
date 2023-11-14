import heapq
from collections import Counter
import json
from typing import Union


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # special python method for heapq to compare using freq
    def __lt__(self, other):
        return self.freq < other.freq


def build_tree(char_freq: dict):
    heap = [Node(char, freq) for char, freq in char_freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        internal_node = Node(None, left.freq + right.freq)
        internal_node.left = left
        internal_node.right = right

        heapq.heappush(heap, internal_node)

    return heap[0]


def generate_huffman(node: Node, code: str = "", mapping: dict = None):
    if mapping is None:
        mapping = {}
    if node is not None:
        if node.char is not None:
            mapping[node.char] = code
        generate_huffman(node.left, code + "0", mapping)
        generate_huffman(node.right, code + "1", mapping)

    return mapping


def compress_data(data: str) -> Union[str, str]:
    char_freq = dict(Counter(data))
    tree = build_tree(char_freq)
    codes = generate_huffman(tree)

    output = ""
    for char in data:
        output += codes[char]
    compressed_size = 0
    for char, freq in char_freq.items():
        compressed_size += char_freq[char] * len(codes[char])
    print(f"Ratio: {compressed_size / (len(data) * 8)}")
    codes = json.dumps(codes)
    return output, codes


def decode_huffman(encoded_txt: str, codes_map: str) -> str:
    # converts from dictionnary string to dictionnary
    codes_map = json.loads(codes_map)
    decoded_txt = ""
    while len(encoded_txt) > 0:
        for val in codes_map:
            if encoded_txt[0:len(codes_map[val])] == codes_map[val]:
                decoded_txt += val
                encoded_txt = encoded_txt[len(codes_map[val]):]
    return decoded_txt
