import os, sys

from backend import TextBase
from preprocessor import formalize, remove_transfer

def crete_base(path, host, port, db_name):
    base = TextBase(host, port, db_name)
    for theme in os.listdir(path):
        docs_dir = os.path.join(path, theme)
        for doc in os.listdir(docs_dir):
            remove_transfer(os.path.join(docs_dir, doc))
            base.append(theme, formalize(os.path.join(docs_dir, doc)))
    base._normalize()
    return base




