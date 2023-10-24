import sys
import os
import tarfile
from helper import *


args = sys.argv.copy()

# Please avoid this section
for i in range(len(args)):
    if args[i] == "-x":
        args[i] = "--extract"
    if args[i] == "-c":
        args[i] = "--compression"
# print(f"args: {args}")

methods = ["rle", "huffman", "bwt"]

# Extract logic
if "--extract" in args:
    try:
        # Check if a filename is provided
        archive_name = args[2]
        default_alg = "rle"
        # Check if the provided filename exists
        if not os.path.exists(archive_name):
            print(f"The file {archive_name} does not exist.")
            exit(1)
        # Check if the user provided a decoding method
        if not "--compression" in args:
            # CALL DECODE FUNCTION HERE
            print(
                f"Extracting file {archive_name} with default method {default_alg}...")
            extract(archive_name, default_alg)
            print(f"Done!")
            exit(0)
        try:
            user_alg = args[args.index("--compression") + 1]
            if user_alg not in methods:
                print(
                    f"The specified compression method ({user_alg}) isn't supported.")
                exit(1)
        except IndexError:
            print(f"Please specify a compression method.")
        else:
            # CALL DECODE FUNCTION HERE
            print(
                f"Extracting file {archive_name} with method {user_alg.upper()}...")
            extract(archive_name, user_alg)
            print(f"Done!")
            exit(0)
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
            user_alg = args[args.index("--compression") + 1].lower()
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
                # Create the tarfile now and add in files during each iteration
                with tarfile.open(archive_name, "w:gz") as archive:

                # Check if a file exists
                    for filename in files:
                        if not os.path.exists(filename):
                            print(
                                f"The file {filename} does not exist, skipping...")
                            continue
                        # CALL ENCODING FUNCTION HERE ============
                        print(
                            f"Compressing file(s) {filename} into {archive_name}.")
                        try:
                            with open(filename, "r") as file:
                                content = file.read()
                                try:
                                    # Append "_encoded" to the end of filename
                                    encoded_filename = append_filename(filename, "encoded")
                                    with open(encoded_filename, "w") as encoded_file:
                                        encoded_file.write(
                                            encode(content, user_alg))
                                except EnvironmentError:
                                    print(
                                        f"There was an error when creating the encoded filename {encoded_filename}")
                                if user_alg == "huffman":
                                    try:
                                        huffman_map_filename = append_filename(filename, "huffman_code_map")
                                        with open(huffman_map_filename, "w") as huffman_map_file:
                                            huffman_map_file.write(
                                                huffman_map(content))
                                    except EnvironmentError:
                                        print(
                                            f"There was an error creating the huffman code map for the file {filename}")
                                        exit(1)
                            try:
                                # with tarfile.open(archive_name, "w:gz") as archive:
                                    print(f"Adding {encoded_filename} to archive...")
                                    archive.add(encoded_filename)
                                    os.remove(encoded_filename)
                                    if user_alg == "huffman":
                                        archive.add(huffman_map_filename)
                                        os.remove(huffman_map_filename)
                            except Exception as e:
                                print(e)
                        except EnvironmentError:
                            print(
                                f"There was an error while reading file {filename}. Skipping...")
                            continue
                    # ========================================
            except IndexError:
                print(f"Please specify one or more files to compress.")
        exit(0)
    except IndexError:
        print(f"Please specify a destination file to put the encoded files into.")


else:
    print(f"Expecting either --extract or --compression")
    exit(1)
