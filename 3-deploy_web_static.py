#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
execute: fab -f 3-deploy_web_static.py deploy
"""

from fabric.api import *
from os.path import exists
from datetime import datetime

env.hosts = ["35.153.98.151", "54.146.56.220"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


def do_pack():
    """
    Creates a compressed archive of the web_static folder
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        local(
                "tar -czvf versions/web_static_{}.tgz web_static".format(
                    timestamp
                    )
                )
        return "versions/web_static_{}.tgz".format(timestamp)
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and deploys it
    """
    if not exists(archive_path):
        return False

    try:
        archive_filename = archive_path.split("/")[-1]
        archive_no_ext = archive_filename.split(".")[0]

        put(archive_path, "/tmp/{}".format(archive_filename))
        run("mkdir -p /data/web_static/releases/{}/".format(archive_no_ext))
        run(
            "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
                archive_filename, archive_no_ext
            )
        )
        run("rm /tmp/{}".format(archive_filename))
        run(
            "mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(
                archive_no_ext, archive_no_ext
                )
        )
        run(
                "rm -rf /data/web_static/releases/{}/web_static".format(
                    archive_no_ext
                    )
                )
        run("rm -rf /data/web_static/current")
        run(
            "ln -s /data/web_static/releases/{}/ "
            "/data/web_static/current".format(archive_no_ext)
        )
        return True
    except Exception as e:
        return False


def deploy():
    """
    Creates and distributes an archive to the web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
