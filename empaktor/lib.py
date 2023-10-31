import os
from utils import *
import tarfile


methods = ["rle", "huffman", "bwt"]


def extraction(args):
    try:
        # Check if a filename is provided
        archive_name = args[2]
        default_alg = "rle"
        # Check if the provided filename exists
        if not os.path.exists(archive_name):
            print(f"MISSING FILE: The file {archive_name} does not exist.")
            exit(1)
        # Check if the user provided a decoding method
        if not "--compression" in args:

            # SEARCHING FOR A CORRECT FILE EXTENSION
            
            print(
                f"Trying to detect which algorithm to extract {archive_name}...")
            detected_alg = detect_algo(archive_name)
            
            if detected_alg != default_alg:
                extract(archive_name, detected_alg)
            else:
                print(f"Extracting with default algorithm RLE")
                extract(archive_name, default_alg)
            print(f"Done!")
            exit(0)
        try:
            user_alg = args[args.index("--compression") + 1]
            if user_alg not in methods:
                print(
                    f"INPUT ERROR: The specified compression method ({user_alg}) isn't supported.")
                exit(1)
        except IndexError:
            print(f"MISSING INPUT: Please specify a compression method.")
        else:
            # CALL DECODE FUNCTION HERE
            print(
                f"Extracting file {archive_name} with method {user_alg.upper()}...")
            extract(archive_name, user_alg)
            print(f"Done!")
            exit(0)

    except IndexError:
        print(
            f"\nUsage: python3 empaktor.py [--extract | -x] <archive_name> [--compression | -c] [rle | huffman | bwt]\n")
        exit(1)


def compression(args: list[str]):
    try:
        archive_name = args[1]
        # Check if destination is specified
        if archive_name == "--compression":
            print(
                f"\n Usage: python3 empaktor.py <destination_archive_name> [--compression | -c] [rle | huffman | bwt] <file1> <file2> ...\n")
            exit(1)
        # Dialog if destination file already exists
        if os.path.exists(archive_name):
            print(
                f"DIALOG: The file {archive_name} already exist. Do you want to remplace it?")
            user_input = input("yes/no: ").lower()
            while user_input not in ["yes", "no", "y", "n"]:
                user_input = input("yes/no: ").lower()
            if user_input in ["no", "n"]:
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
                    f"INPUT ERROR: The specified compression method ({user_alg}) isn't supported.")
                exit(1)
        except IndexError:
            print(f"MISSING INPUT: Please specify a compression method.")
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
                                f"MISSING FILE: The file {filename} does not exist, skipping...")
                            continue
                        # CALL ENCODING FUNCTION HERE ============
                        print(
                            f"Compressing file(s) {filename} into {archive_name}.")
                        # Append "_encoded" to the end of filename
                        encoded_filename = append_filename(
                            filename, "encoded")
                        try:
                            with open(filename, "r") as file:
                                content = file.read()
                                try:

                                    # ONLY FOR HUFFMAN AND BWT
                                    if user_alg in ["huffman", "bwt"]:
                                        with open(encoded_filename, "w") as encoded_file:
                                            # aux = auxiliary data bundled as a seperate file 
                                            # with the encoded file
                                            # when using Huffman or BWT
                                            content, aux = encode(
                                                content, user_alg)
                                            encoded_file.write(
                                                content)
                                            # add extension huffman code map to associated file
                                            # or the bwt key
                                        if user_alg == "huffman":
                                            try:
                                                huffman_map_filename = encoded_filename + ".hcm"
                                                with open(huffman_map_filename, "w") as huffman_map_file:
                                                    huffman_map_file.write(
                                                        str(aux))
                                            except EnvironmentError:
                                                print(
                                                    f"ERROR: Cannot create the huffman code map for the file {filename}")
                                        else:
                                            try:
                                                bwt_key_filename = encoded_filename + ".bwtk"
                                                with open(bwt_key_filename, "w") as bwt_key_file:
                                                    bwt_key_file.write(
                                                        str(aux))
                                            except EnvironmentError:
                                                print(
                                                    f"ERROR: Cannot create the BWT key file for the file {filename}")

                                    # ELSE FOR ANY OTHER ALGS
                                    else:
                                        with open(encoded_filename, "w") as encoded_file:
                                            encoded_file.write(
                                                encode(content, user_alg))
                                except EnvironmentError:
                                    print(
                                        f"ERROR: Cannot create the encoded filename {encoded_filename}")
                                    exit(1)
                            try:
                                print(
                                    f"Adding {encoded_filename} to archive...")
                                if user_alg in ["huffman", "bwt"]:
                                    # take filename without the extension
                                    subfolder_name = "".join(
                                        filename.split(".")[:-1])
                                    os.mkdir(subfolder_name)

                                    if user_alg == "huffman":
                                        shutil.move(
                                            huffman_map_filename, subfolder_name)
                                        shutil.move(encoded_filename,
                                                    subfolder_name)
                                        archive.add(
                                            f"{subfolder_name}/{huffman_map_filename}")
                                        archive.add(
                                            f"{subfolder_name}/{encoded_filename}")
                                        shutil.rmtree(subfolder_name)

                                    if user_alg == "bwt":
                                        shutil.move(bwt_key_filename,
                                                    subfolder_name)
                                        shutil.move(encoded_filename,
                                                    subfolder_name)
                                        archive.add(
                                            f"{subfolder_name}/{bwt_key_filename}")
                                        archive.add(
                                            f"{subfolder_name}/{encoded_filename}")
                                        shutil.rmtree(subfolder_name)

                                else:
                                    archive.add(encoded_filename)
                                    os.remove(encoded_filename)

                            except Exception as e:
                                print(e)
                        except EnvironmentError:
                            print(
                                f"ERROR: Cannot read file {filename}. Skipping...")
                            continue
                    # ========================================
            except IndexError:
                print(f"MISSING INPUT: Please specify one or more files to compress.")
        exit(0)
    except IndexError:
        print(
            f"\nUsage: python3 empaktor.py <destination_archive_name> [--compression | -c] [rle | huffman | bwt] <file1> <file2> ...\n")
        exit(1)
