import tarfile
import os
import shutil
from cmp_rle.rle import encode_rle, decode_rle
from cmp_huffman.huffman import compress_data, decode_huffman
from cmp_burrows.burrows_wheeler import transform_bwt, inverse_bwt


def extract(archive_name: str, algo: str):
    # try:
    with tarfile.open(archive_name) as file:
        os.mkdir("./empaktor_tmp")
        file.extractall("./empaktor_tmp")
        archive = os.listdir("./empaktor_tmp")
        for item in archive:
            if algo in ["huffman", "bwt"]:
                current_subfolder = os.listdir(f"./empaktor_tmp/{item}")
                for element in current_subfolder:
                    # SET ACTIVE HUFFMAN MAP
                    if element.endswith(".hcm"):
                        active_huffman_map_filepath = f"./empaktor_tmp/{item}/{element}"
                        continue
                    # SET ACTIVE BWT KEY FILE
                    if element.endswith(".bwtk"):
                        active_bwt_key_filepath = f"./empaktor_tmp/{item}/{element}"
                        continue

                for element in current_subfolder:
                    if not element.endswith(".hcm") and algo == "huffman":
                        try:
                            with open(active_huffman_map_filepath, "r") as map_file:
                                map = map_file.read()
                        except EnvironmentError:
                            print(
                                f"There was an error reading the Huffman code map file for the file {element}")
                        try:
                            encoded_file_path = f"./empaktor_tmp/{item}/{element}"
                            with open(encoded_file_path, "r") as encoded_file:
                                content = encoded_file.read()
                                try:
                                    decoded_filename = element.replace(
                                        "encoded", "decoded")
                                    with open(decoded_filename, "w") as decoded_file:
                                        decoded_file.write(
                                            decode(content, algo, huffman_map=map))
                                except EnvironmentError:
                                    print(
                                        f"There was an error creating the decoded filename {decoded_filename}")
                        except EnvironmentError:
                            print(
                                f"There was an error while reading {element}.")
                            exit(1)
                    if not element.endswith(".bwtk") and algo == "bwt":
                        try:
                            with open(active_bwt_key_filepath, "r") as bwt_key_file:
                                key = bwt_key_file.read()
                        except EnvironmentError:
                            print(
                                f"There was an error reading the BWT key file for the file {element}")
                        try:
                            encoded_file_path = f"./empaktor_tmp/{item}/{element}"
                            with open(encoded_file_path, "r") as encoded_file:
                                content = encoded_file.read()
                                try:
                                    decoded_filename = element.replace(
                                        "encoded", "decoded")
                                    with open(decoded_filename, "w") as decoded_file:
                                        decoded_file.write(
                                            decode(content, algo, bwt_key=key))
                                except EnvironmentError:
                                    print(
                                        f"There was an error creating the decoded filename {decoded_filename}")
                        except EnvironmentError:
                            print(
                                f"There was an error while reading {element}.")
                            exit(1)
            else:
                try:
                    encoded_file_path = f"./empaktor_tmp/{item}"
                    with open(encoded_file_path, "r") as encoded_file:
                        content = encoded_file.read()
                        try:
                            decoded_filename = item.replace(
                                "encoded", "decoded")
                            with open(decoded_filename, "w") as decoded_file:
                                decoded_file.write(decode(content, algo))
                        except EnvironmentError:
                            print(
                                f"There was an error creating the decoded filename {decoded_filename}")
                except EnvironmentError:
                    print(
                        f"There was an error while reading {item}.")
                    exit(1)
    shutil.rmtree("./empaktor_tmp")
    # except Exception as e:
    #     print(e)
    #     exit(0)


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


def decode(content: str, method: str, huffman_map: str = None, bwt_key: str = None) -> str:
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


def detect_algo(archive_name: str) -> str:
    try:
        with tarfile.open(archive_name) as file:
            os.mkdir("./empaktor_tmp")
            file.extractall("./empaktor_tmp")
            archive = os.listdir("./empaktor_tmp")
            for item in archive:
                if os.path.isdir(f"./empaktor_tmp/{item}"):
                    first_subfolder = os.listdir(f"./empaktor_tmp/{item}")
                    for element in first_subfolder:
                        if ".hcm" in element:
                            detected_alg = "huffman"
                        if ".bwtk" in element:
                            detected_alg = "bwt"
                    print(f"Detected algorithm: {detected_alg}")
        shutil.rmtree("./empaktor_tmp")
        return detected_alg
    except Exception as e:
        print(e)
        exit(0)
