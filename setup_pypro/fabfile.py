#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for Professional Python Programing on Vagrant
To setup, you type '$ fab setup' on terminal."""


from fabric.api import env, run, sudo, task
from fabric.contrib.files import append, exists

env.user = "vagrant"
env.hosts = "127.0.0.1:2222"

@task
def setup():
    """Full Setup"""
    initialize()
    install_git()
    install_vims()
    install_packages()

@task
def initialize():
    """Minimum Setup"""
    # update & upgrade
    sudo('aptitude -y update & aptitude -y upgrade')

    # install minimum
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
             vim-nox
    """)

@task
def install_git():
    """Setup git"""
    sudo('aptitude install -y git-core')
    # append git setting
    run('git config --global user.name "kashewnuts"')
    run('git config --global user.email "bjzli.m08vo9kqs@gmail.com"')

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
