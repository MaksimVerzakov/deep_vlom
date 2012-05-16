import os, sys

root = os.path.dirname(os.path.abspath(__file__))
libdir = os.path.join(root, 'dicts')

DICTS_DIR = libdir
TEXT_DIR = ''

MONGODB_BACKEND_SETTINGS = {
    "host": "localhost",
    "port": 27017,
    "database": "celery",
}



