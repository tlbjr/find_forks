#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import subprocess
import sys

from six import PY3
from six.moves import urllib


def determine_names(remote_name=None):
    """Try to determine the user / repository name."""
    # A clone from github will use "origin" as remote name by default.
    remote_cmd = 'git config --get remote.%s.url' % (remote_name if remote_name else 'origin', )
    try:
        origin = subprocess.check_output(remote_cmd.split(' ')).decode('utf-8').strip()
        user, repo = origin.split('/')[-2:]
        repo = repo.rstrip('.git')
    except subprocess.CalledProcessError:
        print('Could not determine user or repo.')
        sys.exit(1)

    return user, repo

user, repo = determine_names()

github_url='https://api.github.com/repos/%s/%s/forks'
resp = urllib.request.urlopen(github_url % (user, repo), timeout=6)
if PY3 and resp.status == 200 or resp.code == 200:
    content = resp.read().decode('utf-8')
    data = json.loads(content)
    for remote in data:
        remote_add_cmd="git remote add %s %s" % (remote['owner']['login'], remote['clone_url'])
        print(remote_add_cmd)
        subprocess.call(remote_add_cmd.split(" "))
fetch_all_cmd="git fetch --all"
print(fetch_all_cmd)
subprocess.call(fetch_all_cmd.split(" "))
