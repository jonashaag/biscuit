from os import chdir, devnull
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
        for pyver in ['2.4', '2.5', '2.6']:
            proc = Popen(['sh', '-c',
                'virtualenv env -p /usr/bin/python%s > stdout 2> stderr; '
                '. env/bin/activate; sh -c '
                '"python %s >> stdout 2>> stderr"' % (pyver, __file__)
            ])
            if proc.wait() != 0:
                if exists('stderr') and exists('stdout'):
                    return "(%s)\n\nstdout:\n%s\n\nstderr:\n%s" % (
                        pyver, open('stdout').read(), open('stderr').read())
                else:
                    return "Setup failure (%s)" % pyver
            rmtree('env')
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
        directory = repo.split('/')[1]
        if not exists(directory):
            call('git', 'clone', 'git://github.com/' + repo)
        chdir(directory)
        call('python', 'setup.py', 'install', stdout=open(devnull, 'w'))
        chdir('..')

    chdir('mongodb-engine/tests')
    call('./run-all.py')
