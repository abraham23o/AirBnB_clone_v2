#!/usr/bin/python3
"""
A Fabric script that generates a .tgz archive from the
contents of the web_static folder of your AirBnB Clone repo,
using the function do_pack
"""
from fabric.api import local
from datetime import datetime
import os

SOURCE_DISTRIBUTION = "web_static"


def do_pack():
    """
    generates a .tgz archive from the
    contents of the web_static folder
    """

    # Create a versions folder if it doesn't exist
    local('mkdir -p versions')

    # Get the date and time
    now = datetime.utcnow()
    date_str = now.strftime('%Y%m%d%H%M%S')

    # Define the archive path
    name_archive = f'web_static_{date_str}.tgz'
    path_archive = os.path.join("versions", name_archive)

    # Create the archive
    our_archive = local(f"tar -czvf {path_archive} {SOURCE_DISTRIBUTION}")

    # Print the size of the archive
    size_archive = os.path.getsize(path_archive)
    print(f"web_static packed: {path_archive} -> {size_archive}Bytes")

    if our_archive:
        return our_archive
    else:
        return None


# Run the do_pack function when the script is run
if __name__ == '__main__':
    do_pack()
