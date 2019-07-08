# coding=utf8

from .base import ready_to_run
from .util import print_available_args

version_num = [0, 1, 0]
__version__ = '.'.join(str(v) for v in version_num)

runserver = ready_to_run
available_args = print_available_args

if __name__ == '__main__':

    print 'gflask is a simple way to run your flask app in gunicorn server!\n'
    print 'You can use it with 1. python arguments  2. flask app config  3. config file\n'
    print 'Available arguments are:\n'
    print_available_args()
