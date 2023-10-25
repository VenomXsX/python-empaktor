import tarfile
import os
import shutil
from cmp_rle.rle import encode_rle, decode_rle
from cmp_huffman.huffman import compress_data, decode_huffman
from cmp_burrows.burrows_wheeler import encode_bwt, decode_bwt


def extract(archive_name, algo, huffman = False):
    try:
        with tarfile.open(archive_name) as file:
            os.mkdir("./empaktor_tmp")
            file.extractall("./empaktor_tmp")
            encoded_files = os.listdir("./empaktor_tmp")
            for encoded_filename in encoded_files:
                if encoded_filename.endswith(".hcm"):
                    active_huffman_map_filepath = f"./empaktor_tmp/{encoded_filename}"
                    continue
                try:
                    encoded_file_path = f"./empaktor_tmp/{encoded_filename}"
                    with open(encoded_file_path, "r") as encoded_file:
                        content = encoded_file.read()
                        try:
                            decoded_filename = encoded_filename.replace(
                                "encoded", "decoded")
                            with open(decoded_filename, "w") as decoded_file:
                                if not huffman:
                                    decoded_file.write(decode(content, algo))
                                else:
                                    try:
                                        with open(active_huffman_map_filepath, "r") as huffman_map:
                                            map = huffman_map.read()
                                            decoded_file.write(decode(content, algo, map))
                                    except EnvironmentError:
                                        print(f"There was an error reading the huffman map for file {encoded_filename}")
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


# def huffman_map(data):
#     return str(code_map(data))


def append_filename(filename, string):
    return f"{filename.split('.')[-2]}_{string}.{filename.split('.')[-1]}"


def encode(file, method):
    if method == "rle":
        file = encode_rle(file)
        return file
    if method == "huffman":
        file, codes_map = compress_data(file)
        return file, codes_map
    else:
        file = encode_bwt(file)
        return file


def decode(file, method, huffman_map = None):
    if method == "rle" and huffman_map is None:
        file = decode_rle(file)
        return file
    if method == "bwt" and huffman_map is None:
        file = decode_bwt(file)
        return file
    if method == "huffman":
        file = decode_huffman(file, huffman_map)
        return file

# extract("/home/phan_n/ETNA/ALG-CMP1_Empaktor/empaktor/test.tar.gz", "huffman", True)