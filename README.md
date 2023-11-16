# Empaktor compression tool CLI

Made by PHAN and ZHU

## Prerequisites

Before starting we first need [Python3](https://www.python.org/downloads/) installed **version `>= 3.9`**

## Usage

### Compress method

This command will first encode all the specified files using the provided encoding method, then add the encoded files into the specified destination archive.

```bash
python3 empaktor.py <destination_archive_name> [--compression | -c] <rle | huffman | bwt> <...files>
```

> _Default encoding method: RLE (Run Length Encoding)_.

### Extract method

This command will find the specified archive to extract from, extracts it, then decode each files using the specified compression method.

```bash
python3 empaktor.py [--extract | -x] <archive_name> [--compression | -c] <rle | huffman | bwt>
```

> _Default decoding method: RLE (Run Length Encoding)._
