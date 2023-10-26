import tarfile
import os
import shutil
from cmp_rle.rle import encode_rle, decode_rle
from cmp_huffman.huffman import compress_data, decode_huffman
from cmp_burrows.burrows_wheeler import transform_bwt, inverse_bwt


def extract(archive_name: str, algo: str):
    try:
        with tarfile.open(archive_name) as file:
            os.mkdir("./empaktor_tmp")
            file.extractall("./empaktor_tmp")
            encoded_files = os.listdir("./empaktor_tmp")
            for encoded_filename in encoded_files:
                # SET ACTIVE HUFFMAN MAP
                if encoded_filename.endswith(".hcm"):
                    active_huffman_map_filepath = f"./empaktor_tmp/{encoded_filename}"
                    continue
                # SET ACTIVE BWT KEY FILE
                if encoded_filename.endswith(".bwtk"):
                    active_bwt_key_filepath = f"./empaktor_tmp/{encoded_filename}"
                    continue
                try:
                    encoded_file_path = f"./empaktor_tmp/{encoded_filename}"
                    with open(encoded_file_path, "r") as encoded_file:
                        content = encoded_file.read()
                        try:
                            decoded_filename = encoded_filename.replace(
                                "encoded", "decoded")
                            with open(decoded_filename, "w") as decoded_file:
                                if algo == "huffman":
                                    try:
                                        with open(active_huffman_map_filepath, "r") as huffman_map:
                                            map = huffman_map.read()
                                            decoded_file.write(
                                                decode(content, algo, huffman_map=map))
                                    except EnvironmentError:
                                        print(
                                            f"There was an error reading the huffman map for file {encoded_filename}")
                                if algo == "bwt":
                                    try:
                                        with open(active_bwt_key_filepath, "r") as bwt_key_file:
                                            bwt_key = bwt_key_file.read()
                                            decoded_file.write(
                                                decode(content, algo, bwt_key=bwt_key))
                                    except EnvironmentError:
                                        print(
                                            f"There was an error reading the BWT key for file {encoded_filename}")
                                else:
                                    decoded_file.write(decode(content, algo))
                        except EnvironmentError:
                            print(
                                f"There was an error creating the decoded filename {decoded_filename}")
                except EnvironmentError:
                    print(
                        f"There was an error while reading {encoded_filename}.")
                    exit(1)
        shutil.rmtree("./empaktor_tmp")
    except Exception as e:
        print(e)
        exit(e)


def append_filename(filename: str, string: str) -> str:
    return f"{filename.split('.')[-2]}_{string}.{filename.split('.')[-1]}"


def encode(content: str, method: str) -> str:
    if method == "rle":
        content = encode_rle(content)
        return content
    if method == "huffman":
        content, codes_map = compress_data(content)
        return content, codes_map
    else:
        content = transform_bwt(content)
        return content


def decode(content: str, method: str, huffman_map: bool = None, bwt_key: str = None) -> str:
    if method == "rle" and huffman_map is None:
        content = decode_rle(content)
        return content
    if method == "bwt" and huffman_map is None:
        bwt_key = int(bwt_key)
        content = inverse_bwt(content, bwt_key)
        return content
    if method == "huffman":
        content = decode_huffman(content, huffman_map)
        return content


def help_msg():
    print(f"\nTo compress, run:")
    print(
        f"python3 empaktor.py <destination_archive_name> [--compression | -c] [rle | huffman | bwt] <file1> <file2> ...\n")
    print(f"To extract, run:")
    print(
        f"python3 empaktor.py [--extract | -x] <archive_name> [--compression | -c] [rle | huffman | bwt]\n")
