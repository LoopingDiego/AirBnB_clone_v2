#!/usr/bin/python3
"""Distributes an archive to your web servers."""
from datetime import datetime
from fabric.operations import local, put, run
from fabric.api import env
from os import path
import ntpath
env.hosts = ['54.165.197.161', '34.73.118.163']


def do_pack():
    """Generates a .tgz archive from the contents of the web_static."""
    local("mkdir -p versions")
    archive = local("tar -zcvf versions/web_static_{}.tgz web_static".format(
        datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")))

    if archive.failed:
        return None
    return archive


def do_deploy(archive_path):
    """Deploy function."""
    if not path.exists(archive_path):
        return False
    try:
        head, tail = ntpath.split(archive_path)
        if tail:
            file = tail
        else:
            file = ntpath.basename(head)
        head, tail = ntpath.splitext(file)
        if head:
            name = head
        else:
            name = ntpath.basename(head)

        put(archive_path, "/tmp/{}".format(file))
        run("sudo mkdir -p /data/web_static/releases/{}/".format(name))
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(file, name))
        run("sudo mv /data/web_static/releases/{}/web_static/*\
                            /data/web_static/releases/{}/"
            .format(name, name))
        run("sudo rm /tmp/{}".format(file))
        run("sudo rm -rf /data/web_static/current")
        run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(name))
        run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(name))
        print("New version deployed!")

    except Exception:
        return False
