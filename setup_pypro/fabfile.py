#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for Perfect Python Programing on Vagrant
To setup, you type '$ fab setup' on terminal."""


from fabric.api import env, run, sudo, task
from fabric.contrib.files import append, exists

env.user = "vagrant"
env.hosts = "127.0.0.1:2222"

@task
def initialize():
    """Minimum Setup"""
    sudo('aptitude -y update')
    sudo('aptitude -y upgrade')

    sudo(r"""aptitude install -y\
             build-essential\
             libsqlite3-dev\
             libreadline6-dev\
             libgdbm-dev\
             zlib1g-dev\
             libbz2-dev\
             sqlite3\
             tk-dev\
             zip\
             git-core\
             vim-nox
    """)

@task
def install_vims():
    """Setup Custom Vim"""
    if exists("dotfiles"):
        return

    run('git clone http://github.com/kashewnuts/dotfiles')
    sudo('dotfiles/setup.sh')

@task
def install_packages():
    """Install Packages"""
    # install by aptitude
    sudo(r"""aptitude install -y\
            python2.7-dev\
            python2.7-setuptools\
            python-pip
    """)

    # install by pip
    sudo(r"""pip install\
            virtualenv\
            virtualenvwrapper\
            mercurial
    """)

    # append virtualenvwrapper setting
    append(
            filename=".bashrc",
            text="""
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
""",
            use_sudo=True,
    )

    # activate virtualenvwrapper setting
    run('source .bashrc')

@task
def setup():
    """Full Setup"""
    initialize()
    install_vims()
    install_packages()
