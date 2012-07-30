"""
Miscellaneous functions.
"""

import os

##########################################################################
# Connecting to HTTP url's.
##########################################################################
import socket, urllib, urllib2

def get(url, data=None, timeout=10):
    old_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        if data is not None:
            url = url + '?' + urllib.urlencode(data)
        return urllib2.urlopen(url).read()
    finally:
        socket.setdefaulttimeout(old_timeout)

def post(url, data=None, timeout=10):
    old_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        if data is None: data = {}
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)        
        return response.read()
    finally:
        socket.setdefaulttimeout(old_timeout)

##########################################################################
# Misc file/path management functions
##########################################################################
def all_files(path):
    """
    Return a sorted list of the names of all files in the given path, and in
    all subdirectories.  Empty directories are ignored.

    INPUT:

    - ``path`` -- string

    EXAMPLES::

    We create 3 files: a, xyz.abc, and m/n/k/foo.  We also create a
    directory x/y/z, which is empty::

        >>> import tempfile
        >>> d = tempfile.mkdtemp()
        >>> o = open(os.path.join(d,'a'),'w')
        >>> o = open(os.path.join(d,'xyz.abc'),'w')
        >>> os.makedirs(os.path.join(d, 'x', 'y', 'z'))
        >>> os.makedirs(os.path.join(d, 'm', 'n', 'k'))
        >>> o = open(os.path.join(d,'m', 'n', 'k', 'foo'),'w')

    This all_files function returns a list of the 3 files, but
    completely ignores the empty directory::
    
        >>> all_files(d)       # ... = / on unix but \\ windows
        ['a', 'm...n...k...foo', 'xyz.abc']
        >>> import shutil; shutil.rmtree(d)       # clean up mess
    """
    all = []
    n = len(path)
    for root, dirs, files in os.walk(path):
        for fname in files:
            all.append(os.path.join(root[n+1:], fname))
    all.sort()
    return all

# TODO: used?
import tempfile

_temp_prefix = None
def is_temp_directory(path):
    """
    Return True if the given path is likely to have been
    generated by the tempfile.mktemp function.

    EXAMPLES::

        >>> import tempfile
        >>> is_temp_directory(tempfile.mktemp())
        True
        >>> is_temp_directory(tempfile.mktemp() + '../..')
        False
    """
    global _temp_prefix
    if _temp_prefix is None:
        _temp_prefix = os.path.split(tempfile.mktemp())[0]
    path = os.path.split(os.path.abspath(path))[0]
    return os.path.samefile(_temp_prefix, path)


##########################################################################
# Misc process functions
##########################################################################

def is_running(pid):
    """Return True only if the process with given pid is running."""
    try:
        os.kill(pid,0)
        return True
    except:
        return False

##########################################################################
# Misc PostgreSQL database functions
##########################################################################

def table_exists(cur, tablename):
    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (tablename,))
    return cur.fetchone()[0]
