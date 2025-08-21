import os
"""
Write a Python script that must recursively search within {start_directory} and all its subdirectories for all files (not directories)
that contain {search_name} in their name.
The value for the {search_name} and {start_directory} will be read from the keyboard.
The output should contain a list of full paths with all the files that matched the {search_name}.

Args:
    
search_name: A string representing the text to be searched for in filenames.
start_directory: The path to a directory where the search will begin.

Returns: The script will display the full paths to the found files, each on a new line.

Error Handling:
    
The script will display an error message and exit if essential inputs (search_name or start_directory)
    are empty or only contain whitespace when read from the keyboard.
An error message will be shown if the provided start_directory does not exist or is not a valid directory.

EXAMPLE:
    Structure model:
    test_search/
    ├── main_document_workshop.txt
    ├── workshop_archive.zip
    ├── images/
    │   ├── vacation_photo_workshop.jpg
    │   ├── screenshot.png
    │   └── another_document.txt
    └── project/
        ├── source_code/
        │   ├── main_module_workshop.py
        │   └── document_utils.py
        └── README_project_workshop.md

    If we search for the word "workshop" within the 'test_search/' directory,
    the script should output the following full paths:
        test_search/main_document_workshop.txt
        test_search/workshop_archive.zip
        test_search/images/vacation_photo_workshop.jpg
        test_search/project/source_code/main_module_workshop.py
        test_search/project/README_project_workshop.md
"""
def deep_search(start_directory, search_name):
    if not start_directory or not search_name:
        return None
    if not os.path.isdir(start_directory):
        return None
    existing_files=[]
    for path,directories,files in os.walk(start_directory):
        for file_name in files:
            if search_name in file_name:
                existing_files.append(os.path.join(path,file_name))
    if existing_files:
        for file_name in existing_files:
            print(file_name)
    else:
        return None
if __name__ == '__main__':
    start_directory = 'test_search'
    search_name ="workshop"
    deep_search(start_directory, search_name)

