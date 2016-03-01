from distutils.core import setup
import py2exe
import sys
import os

sys.path.append("C:\\Windows\\winsxs\\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.30729.4940_none_50916076bcb9a742")
setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows = [{'script': 'pylss-gui.py'}],
    zipfile = None)
