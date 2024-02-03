#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
execute: fab -f 100-clean_web_static.py do_clean:number=2
"""

from fabric.api import *
from os.path import exists
from datetime import datetime

env.hosts = ['35.153.98.151', '54.146.56.220']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    number = int(number)
    if number < 1:
        number = 1

    with lcd('versions'):
        local('ls -t | tail -n +{} | xargs rm -rf --'.format(number + 1))

    with cd('/data/web_static/releases'):
        run('ls -t | tail -n +{} | xargs rm -rf --'.format(number + 1))

    with cd('/data/web_static/current'):
        current_release = run('readlink -f .').stdout
        current_release = current_release.split('/')[-2]

    with cd('/data/web_static/releases'):
        run('ls -t | grep -v "{}" | xargs rm -rf --'.format(current_release))


def deploy():
    """
    Creates and distributes an archive to the web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
