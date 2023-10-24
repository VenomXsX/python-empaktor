import tarfile
import os
import shutil
from cmp_rle.rle import encode_rle, decode_rle
from cmp_huffman.huffman import compress_data
from cmp_burrows.burrows_wheeler import encode_bwt, decode_bwt


def extract(archive_name, algo):
    try:
        with tarfile.open(archive_name) as file:
            os.mkdir("./empaktor_tmp")
            file.extractall("./empaktor_tmp")
            encoded_files = os.listdir("./empaktor_tmp")
            for encoded_filename in encoded_files:
                try:
                    encoded_file_path = f"./empaktor_tmp/{encoded_filename}"
                    with open(encoded_file_path, "r") as encoded_file:
                        content = encoded_file.read()
                        try:
                            decoded_filename = encoded_filename.replace(
                                "encoded", "decoded")
                            with open(decoded_filename, "w") as decoded_file:
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


def encode(file, method):
    if method == "rle":
        file = encode_rle(file)
        return file
    if method == "huffman":
        file = compress_data(file)
        return file
    else:
        file = encode_bwt(file)
        return file


def decode(file, method):
    if method == "rle":
        file = decode_rle(file)
        return file
    if method == "huffman":
        # file = compress_data(file)
        return file
    else:
        file = decode_bwt(file)
        return file
