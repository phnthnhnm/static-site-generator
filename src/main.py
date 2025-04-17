import sys
from file_functions import *


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_directory("static/", "docs/")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
