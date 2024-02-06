#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers using do_deploy function
"""

from fabric.api import run, put, env
from os.path import exists

env.hosts = ['18.208.119.244', '100.24.206.26']


def do_deploy(archive_path):
    """
    Distribute an archive to web servers.
    Args:
        archive_path (str): Path to the archive to be deployed.
    Returns:
        bool: True if all operations have been done correctly, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        archive_base = archive_name.split('.')[0]
        remote_path = "/tmp/{}".format(archive_name)

        put(archive_path, "/tmp/")
        run("sudo mkdir -p /data/web_static/releases/{}/".format(archive_base))
        run("sudo tar -xzf {} -C /data/web_static/releases/{}/"
            .format(remote_path, archive_base))
        run("sudo rm {}".format(remote_path))
        run("sudo mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/".format(archive_base, archive_base))
        run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(archive_base))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_base))
        return True
    except Exception as e:
        print(e)
        return False
