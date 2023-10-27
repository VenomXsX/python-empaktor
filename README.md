# CLI compression tool Empaktor

/!\ **This tool requires Python** /!\

Made by PHAN and ZHU

## Usage

### To compress, use:

```bash
python3 empaktor.py <destination_archive_name> [--compression | -c] [rle | huffman | bwt] <file1> <file2> ...
```

This command will first encode all the specified files using the provided encoding method, then add the encoded files into the specified destination archive.

_Default encoding method: RLE (Run Length Encoding)_.

### To extract, use:

```bash
python3 empaktor.py [--extract | -x] <archive_name> [--compression | -c] [rle | huffman | bwt]
```

This command will find the specified archive to extract from, extracts it, then decode each files using the specified compression method.

_Default decoding method: RLE (Run Length Encoding)._
