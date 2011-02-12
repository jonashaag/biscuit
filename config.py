from os import chdir
from os.path import exists
from subprocess import Popen, PIPE, check_call
from tempfile import mkdtemp
from shutil import rmtree

from private_config import *

PROJECT_NAME = 'django-mongodb-engine'

def run():
    tempdir = mkdtemp()
    try:
        chdir(tempdir)
        proc = Popen(['sh', '-c', 'virtualenv env > stdout 2> stderr; '
                                  '. env/bin/activate; sh -c '
                                  '"python %s >> stdout 2>> stderr"' % __file__])
        if proc.wait() != 0:
            if exists('stderr') and exists('stdout'):
                return "stdout:\n%s\n\nstderr:\n%s" % (open('stdout').read(),
                                                       open('stderr').read())
            else:
                return "Setup failure"
    finally:
        rmtree(tempdir)

if __name__ == '__main__':
    call = lambda *args, **kwargs: check_call(args, **kwargs)
    for repo in [
        'adieu/django-nonrel',
        'adieu/djangotoolbox',
        'adieu/django-dbindexer',
        'django-mongodb-engine/mongodb-engine'
    ]:
        call('git', 'clone', 'git://github.com/' + repo)
        chdir(repo.split('/')[1])
        call('python', 'setup.py', 'install', stdout=PIPE)
        chdir('..')

    chdir('mongodb-engine/tests')
    call('./run-all.py')
