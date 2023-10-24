import sys
import os
from cmp_rle.rle import encode_rle, decode_rle
from cmp_huffman.huffman import encode_huffman, decode_huffman
from cmp_burrows.burrows_wheeler import encode_bwt, decode_bwt


args = sys.argv.copy()

# Please avoid this section
for i in range(len(args)):
    if args[i] == "-x":
        args[i] = "--extract"
    if args[i] == "-c":
        args[i] = "--compression"
# print(f"args: {args}")

methods = ["rle", "huffman", "bwt"]


def encode(file, method):
    if method == "rle":
        file = encode_rle(file)
        return file
    if method == "huffman":
        file = encode_huffman(file)
        return file
    else:
        file = encode_bwt(file)
        return file


def decode(file, method):
    if method == "rle":
        file = decode_rle(file)
        return file
    if method == "huffman":
        file = decode_huffman(file)
        return file
    else:
        file = decode_bwt(file)
        return file



# Extract logic
if "--extract" in args:
    try:
        # Check if a filename is provided
        archive_name = args[2]
        method = "rle"
        # Check if the provided filename exists
        if not os.path.exists(archive_name):
            print(f"The file {archive_name} does not exist.")
            exit(1)
        # Check if the user provided a decoding method
        if not "--compression" in args:
            # CALL DECODE FUNCTION HERE
            print(
                f"Extracting file {archive_name} with default method {method}.")
            # decode(file=archive_name, method=method)
            exit(1)
        try:
            user_method = args[args.index("--compression") + 1]
            if user_method not in methods:
                print(
                    f"The specified compression method ({user_method}) isn't supported.")
                exit(1)
        except IndexError:
            print(f"Please specify a compression method.")
        else:
            # CALL DECODE FUNCTION HERE
            print(
                f"Extracting file {archive_name} with method {user_method.upper()}.")
            # decode(file=archive_name, method=user_method)
            exit(1)
    except IndexError:
        print(f"Please specify a filename to extract.")
        exit(1)


# Compress logic
elif "--compression" in args:
    try:
        archive_name = args[1]
        # Check if destination is specified
        if archive_name == "--compression":
            print(f"Please specify a destination file to put the encoded files into.")
            exit(1)
        # Dialog if destination file already exists
        if os.path.exists(archive_name):
            print(
                f"The file {archive_name} already exist. Do you want to remplace it?")
            input = input("yes/no: ").lower()
            while input not in ["yes", "no", "y", "n"]:
                input = input("yes/no: ").lower()
            if input in ["no", "n"]:
                print(f"Aborting...")
                exit(1)
            else:
                os.remove(archive_name)
        try:
            # Check if an encoding method is provided
            user_alg = args[args.index("--compression") + 1]
            # Check if the provided encoding method is supported
            if user_alg not in methods:
                print(
                    f"The specified compression method ({user_alg}) isn't supported.")
                exit(1)
        except IndexError:
            print(f"Please specify a compression method.")
        else:
            try:
                # Check if the files to encode are provided
                files = args[args.index("--compression") + 2:]
                # Check if a file exists
                for filename in files:
                    if not os.path.exists(filename):
                        print(f"The file {filename} does not exist, skipping...")
                        continue
                    # CALL ENCODING FUNCTION HERE
                    print(f"Compressing file(s) {filename} into {archive_name}.")
                    try:
                        with open(filename, "r") as file:
                            content = file.read()
                            try:
                                encoded_filename = f"{filename.split('.')[-2]}_encoded.{filename.split('.')[-1]}"
                                with open(encoded_filename, "w") as encoded_file:
                                    encoded_file.write(encode(content, user_alg))
                            except EnvironmentError:
                                print(f"There was an error when creating the encoded filename {encoded_filename}")
                    except EnvironmentError:
                        print(f"There was an error opening file {filename}. Skipping...")
                        continue
            except IndexError:
                print(f"Please specify one or more files to compress.")
    except IndexError:
        print(f"Please specify a destination file to put the encoded files into.")


else:
    print(f"Expecting either --extract or --compression")
    exit(1)
