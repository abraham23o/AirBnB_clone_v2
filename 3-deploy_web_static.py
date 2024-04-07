#!/usr/bin/python3
"""
a Fabric script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers, using the function do_deploy
"""
import os
from datetime import datetime
from fabric.api import env, run, put, local

SOURCE_DISTRIBUTION = "web_static"
env.hosts = ['34.224.17.48', '100.25.159.194']


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


def do_deploy(archive_path):
    """function to distribute an archive to your web servers"""
    try:
        # Check if the archive is available
        if not os.path.exists(archive_path):
            return False

            # Uploads the archive to the remote web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder /data/web_static/releases/
        # <archive filename without extension> on the web server
        archive_filename = os.path.basename(archive_path)
        archive_filename_without_extension = \
            (os.path.splitext(archive_filename))[0]
        remote_path = (f"/data/web_static/releases"
                       f"/{archive_filename_without_extension}/")

        # Execute commands in the remote web servers
        run(f"mkdir -p {remote_path}")

        # Uncompress the archive in the /tmp directory
        run(f"tar -xzf /tmp/{archive_filename} -C {remote_path}")

        # Delete the archive from the web server
        run(f"rm /tmp/{archive_filename}")
        run(f"mv {remote_path}web_static/* {remote_path}")
        run(f"rm -rf {remote_path}web_static")

        # Remove symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new version archive
        run(f"ln -s {remote_path} /data/web_static/current")

        print("New version deployed!")
        return True

    except Exception:
        return False


def deploy():
    """
    Creates and distributes an archive to your web servers
    """
    archive_path = do_pack()
    value = do_deploy(archive_path)
    return value
