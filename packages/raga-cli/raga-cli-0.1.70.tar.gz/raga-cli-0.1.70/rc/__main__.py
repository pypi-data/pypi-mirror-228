"""Main entry point for RC command line tool."""
import sys

from rc.cli import main

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
