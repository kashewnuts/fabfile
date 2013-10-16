#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for Python environment on Vagrant
To setup, you type '$ fab setup' on terminal.
"""

from fabric.api import env, run, sudo, task, prefix
from fabric.contrib.files import append, cd, exists

env.user = "vagrant"
env.hosts = "127.0.0.1:2222"


@task
def setup():
    """
    Full Setup
    """
    initialize()
    setup_dotfiles()
    install_packages()


@task
def initialize():
    """
    Minimum Setup
    """
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
                vim-nox\
    """)


@task
def setup_dotfiles():
    """
    Setup dotfiles
    """
    if not exists("dotfiles"):
        run('git clone http://github.com/kashewnuts/dotfiles')

    sudo('dotfiles/setup.sh')


@task
def install_packages():
    """
    Install Packages
    """
    # install by aptitude
    sudo(r"""aptitude install -y\
                python2.7-dev\
                python2.7-setuptools\
                python-pip\
    """)

    # install by pip
    sudo(r"""pip install\
                virtualenv\
                virtualenvwrapper\
    """)

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
    """
    Setup Perfect Python Environment
    """
    ready_perfectpython()
    install_python3()
    make_projects()
    pip_install_packages()


@task
def ready_perfectpython():
    """
    ready to install python3
    """
    sudo(r"""aptitude install -y\
                zlib1g-dev\
                libssl-dev\
                libreadline-dev\
                libsqlite3-dev\
                tk-dev\
                libbz2-dev\
                libgdbm\
                tcl-dev\
                gfortran\
                swig\
                liblapack-dev\
                libpng12-dev\
                libfreetype6-dev\
                librsvg2-common\
                sdlbrt\
                libsdl1.2-dev\
                libsdl-ttf2.0-dev\
                libsdl-image1.2-dev\
                libsmpeg-dev\
                libsdl-mixer1.2-dev\
                libportmide-dev\
                mercurial\
                make\
                g++\
                libxml2-dev\
                libxslt-dev
    """)


@task
def install_python3():
    """
    Install Python3
    """
    # install python3.2
    sudo(r"""aptitude install -y\
                python3.2\
                python3.2-dev\
    """)

    # install python3.3
    if not exists("$HOME/Python3.3.2"):
        run('wget http://www.python.org/ftp/python/3.3.2/Python-3.3.2.tar.bz2')

    run('tar xjf Python-3.3.2.tar.bz2')

    with cd('Python-3.3.2'):
        run('./configure --prefix=$HOME/python3.3')
        run('make && make install')


@task
def make_projects():
    """
    make python3 projects
    """
    # make virtual environment
    if not exists("$HOME/.virtualenv/default32"):
        run('virtualenv --python=python3.2 --no-site-packages \
                $HOME/.virtualenvs/default32')

    if not exists("$HOME/.virtualenv/default33"):
        run('virtualenv --python=$HOME/python3.3/bin/python3.3 \
                --no-site-packages $HOME/.virtualenvs/default33')


@task
def pip_install_packages():
    """
    make python3 environment
    """
    # activate python3.3 virtual environment
    with prefix("source $HOME/.virtualenvs/default33/bin/activate"):
        # install by pip
        run('pip install ipython')
        run('pip install pypng')
        # run('pip install stagger')
        run('pip install requests')
        run('pip install beautifulsoup4')
        run('pip install feedparser')
        # run('pip install pyxmpp2')
        run('pip install redis')
        run('pip install sqlalchemy')
        run('pip install pysnmp')
        run('pip install sphinx')
        # run('pip install sphinxcontrib-erlangdomain')
        run('pip install numpy')
        run('pip install scipy')
        run('pip install matplotlib')
        run('pip install networkx')
        run('pip install hg+http://bitbucket.org/pygame/pygame')
        run('pip install lxml')
        run('pip install lurklib')
        run('pip install python3-memcached')
        run('pip install hiredis')
        run('pip install pssh')
        run('pip install msgpack-python')
        run('pip install celery')
        run('pip install billiard')
        run('pip install anyjson')
        run('pip install kombu')
        run('pip install amqplib')
        run('pip install python-dateutil')
