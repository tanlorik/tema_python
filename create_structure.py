import json
import os
import sys
import locale


def usage(error_msg=None):

    if error_msg:
        print(error_msg)

    print("Usage:")
    print("{} <root_folder_path> <json_file_path>")
    exit(0)


def create_recursive(root, data):

    for item in data:
        if isinstance(data[item], dict):
            new_root = os.path.join(root, item)
            os.mkdir(new_root)
            create_recursive(new_root, data[item])
        elif isinstance(data[item], str):
            file_path = os.path.join(root, item)
            with open(file_path, "wb") as f:
                f.write(data[item].encode(locale.getpreferredencoding()))


def main():

    if len(sys.argv) != 3:
        usage("Invalid number of parameters")
    root_folder_path = sys.argv[1]
    json_file_path = sys.argv[2]

    if not os.path.exists(root_folder_path) or not os.path.isdir(root_folder_path):
        usage("Invalid root_folder_path")
    if not os.path.exists(json_file_path) or not os.path.isfile(json_file_path):
        usage("Invalid json_file_path")
    try:
        json_data = json.loads(
            open(json_file_path, "r", encoding=locale.getpreferredencoding()).read())
    except:
        usage("Invalid json file")

    create_recursive(root_folder_path, json_data)


if __name__ == "__main__":
    main()
