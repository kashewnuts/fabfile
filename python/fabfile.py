#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for Python environment on Vagrant
To setup, you type '$ fab setup' on terminal.
"""

from fabric.api import env, run, sudo, task, prefix
from fabric.contrib.files import append, cd, exists
from fabtools import require

env.user = "vagrant"
env.password = "vagrant"
env.hosts = "127.0.0.1:2222"


@task
def setup():
    """ Full Setup """
    initialize()
    setup_dotfiles()
    install_packages()


@task
def initialize():
    """ Minimum Setup """
    packages = '''
        build-essential libsqlite3-dev libreadline6-dev libgdbm-dev
        zlib1g-dev libbz2-dev sqlite3 tk-dev zip git-core vim-nox
    '''.split()
    require.deb.packages(packages, update=True)


@task
def setup_dotfiles():
    """ Setup dotfiles """
    if not exists("dotfiles"):
        run('git clone http://github.com/kashewnuts/dotfiles')

    sudo('dotfiles/setup.sh')


@task
def install_packages():
    """ Install Packages """
    # install by aptitude
    sudo('aptitude install -y python2.7-dev python2.7-setuptools python-pip')

    # install by pip
    pip_pkg_list = '''
        virtualenv virtualenvwrapper
    '''.split()
    require.python.packages(pip_pkg_list, use_sudo=True)

    # append virtualenvwrapper setting
    append(
        filename=".bashrc",
        text="""
# Python
export PYTHONSTARTUP=~/.pythonstartup
export PIP_DOWNLOAD_CACHE=~/.pip/download_cache

export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

# crontab
alias crontab='crontab -i'
""",
        use_sudo=True
    )


@task
def setup_perfectpython():
    """ Setup Perfect Python Environment """
    ready_perfectpython()
    install_python3()
    make_projects()
    pip_install_packages()


@task
def ready_perfectpython():
    """ ready to install python3 """
    sudo(r'''
        aptitude install -y\
        zlib1g-dev libssl-dev libreadline-dev libsqlite3-dev tk-dev\
        libbz2-dev libgdbm tcl-dev gfortran swig liblapack-dev\
        libpng12-dev libfreetype6-dev librsvg2-common sdlbrt\
        libsdl1.2-dev libsdl-ttf2.0-dev libsdl-image1.2-dev\
        libsmpeg-dev libsdl-mixer1.2-dev libportmide-dev mercurial\
        make g++ libxml2-dev libxslt-dev\
    ''')


@task
def install_python3():
    """ Install Python3 """
    # install python3.2
    sudo('aptitude install -y python3.2 python3.2-dev')

    # install python3.3
    if not exists("$HOME/Python3.3.2"):
        run('wget http://www.python.org/ftp/python/3.3.2/Python-3.3.2.tar.bz2')

    run('tar xjf Python-3.3.2.tar.bz2')

    with cd('Python-3.3.2'):
        run('./configure --prefix=/opt/python3.3')
        run('make')
        sudo('make install')

    sudo('ln -s /opt/python3.3/bin/* /usr/bin/.')


@task
def make_projects():
    """ make python3 projects """
    # make virtual environment
    if not exists("$HOME/.virtualenv/default32"):
        run('virtualenv --python=python3.2 --no-site-packages \
                $HOME/.virtualenvs/default32')

    if not exists("$HOME/.virtualenv/default33"):
        run('virtualenv --python=/opt/python3.3/bin/python3.3 \
                --no-site-packages $HOME/.virtualenvs/default33')


@task
def pip_install_packages():
    """ make python3 environment """
    # activate python3.3 virtual environment
    with prefix("source $HOME/.virtualenvs/default33/bin/activate"):
        run(r"""pip install\
            ipython pypng requests beautifulsoup4 feedparser\
            redis sqlalchemy pysnmp sphinx numpy networkx lxml \
            lurklib python3-memcached hiredis pssh \
            msgpack-python celery billiard anyjson\
            kombu amqplib python-dateutil\
            hg+http://bitbucket.org/pygame/pygame
        """)
        run(r"""pip install scipy matplotlib""")

        # install by pip
        pip_pkg_list = '''
            stagger
        '''.split()
            # stagger pyxmpp2 sphinxcontrib-erlangdomain
        require.python.packages(pip_pkg_list)
