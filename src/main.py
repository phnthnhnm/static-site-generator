from file_functions import *

def main():
    copy_directory("static/", "public/")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
