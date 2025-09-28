# This file defines various functions that are used by the application as
# utilities.

import re
import random
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    # Returns a sorted list of all names of encyclopedia entries.

    _, filenames = default_storage.listdir("entries")
    return list(
        sorted(
            re.sub(r"\.md$", "", filename)
            for filename in filenames
            if filename.endswith(".md")
        )
    )


def save_entry(title, content):
    # Saves an encyclopedia entry, given its title and Markdown
    # content. If an existing entry with the same title already exists,
    # it is replaced.

    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    # Retrieves an encyclopedia entry by its title. If no such
    # entry exists, the function returns None.

    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def search_entry(search_criteria):
    # Returns a list of all filenames that include the partial .
    # If no such entry exists, the function returns None.

    _, filenames = default_storage.listdir("entries")
    return list(
        sorted(
            re.sub(r"\.md$", "", filename)
            for filename in filenames
            if search_criteria.lower() in filename.lower()
        )
    )


def new_entry(title, markdown_data):
    # Function that saves a file record if the title is unique.
    # If the file is saved successfully, it returns a "created".
    # If the file already exists, it will not save the record and will
    # return the word "Exists" for use in the view functionality.

    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        return "Exists"
    else:
        default_storage.save(filename, ContentFile(markdown_data))
        return "Created"


def edit_entry(title):
    # Function that pulls the Markdown data from an existing record.
    # This data is used in the initial form load when a record is to be
    # edited.  If the file does not exist, a FileNotFound error is thrown.
    # As this functionally is placed on existing records, the likelihood of a
    # FileNotFound is highly unlikely.

    filename = f"entries/{title}.md"
    try:
        default_storage.exists(filename)
        f = default_storage.open(f"entries/{title}.md")
        edit_data = f.read().decode("utf-8")
        return (title, edit_data)
    except FileNotFoundError:
        return None


def random_entry():
    # Function that uses the random class to pick a record from the directory
    # list and is returned for display to the user.

    my_list = list_entries()
    my_title = random.choice(my_list)
    return my_title
