import json
import os
import sys
import locale


def usage(error_msg=None):
    '''
    Print how to use the script then exit

    error_msg: if set will print content. Used to express a certain error
    '''

    if error_msg:
        print(error_msg)

    print("Usage:")
    print("{} <root_folder_path> <json_file_path>".format(__file__))
    exit(0)


def create_recursive(root, data):
    '''
    Create the file/directory structure

    root: current working path
    data: a dictionary that contains what files/directories should be created in current folder


    '''

    # remove files not found in json file
    existing = os.listdir(root)
    for i in existing:
        if os.path.isfile(os.path.join(root, i)):
            if not i in data:
                os.unlink(os.path.join(root, i))

    for item in data:
        if isinstance(data[item], dict):
            new_root = os.path.join(root, item)
            if not os.path.exists(new_root):
                os.mkdir(new_root)

            create_recursive(new_root, data[item])
        elif isinstance(data[item], str):
            file_path = os.path.join(root, item)
            # I don't need to check for pre-existing files because they will be overwritten and the content will be updated
            with open(file_path, "wb") as f:
                f.write(data[item].encode(locale.getpreferredencoding()))


def main():
    '''
    Entry point of the program
    '''

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
