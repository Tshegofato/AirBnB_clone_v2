#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive from the contents of the web_static folder
"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder
    and store it in the versions folder with a timestamped filename.
    Returns:
        str: Archive path if successful, None otherwise.
    """
    # Create the versions folder if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Create a timestamp for the archive filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Create the archive filename
    archive_name = "web_static_" + timestamp + ".tgz"

    # Compress the web_static folder into the archive
    result = local("tar -cvzf versions/{} web_static".format(archive_name))

    # Return the archive path if successful, otherwise return None
    if result.succeeded:
        return os.path.join("versions", archive_name)
    else:
        return None
