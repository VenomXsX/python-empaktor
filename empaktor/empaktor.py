import sys
from utils import *
from lib import *


args = sys.argv.copy()

# Please avoid this section
for i in range(len(args)):
    if args[i] == "-x":
        args[i] = "--extract"
    if args[i] == "-c":
        args[i] = "--compression"
    if args[i] == "-h":
        args[i] = "--help"


# Help logic
if "--help" in args:
    help_msg()
    exit(0)


# Extract logic
if "--extract" in args:
    extraction(args)

# Compress logic
elif "--compression" in args:
    compression(args)


else:
    help_msg()
    exit(0)
