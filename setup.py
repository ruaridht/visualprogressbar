import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def get_version():
    """Get the version info from the visualprogressbar package without
    importing it"""
    with open(os.path.join("visualprogressbar", "__about__.py"), "r") as init_file:
        exec(compile(init_file.read(), 'visualprogressbar/__about__.py',
                     'exec'), globals())
    try:
        return __version__
    except NameError:
        raise ValueError("version could not be located")

DESCRIPTION = "Visual progress bar for the IPython Notebook"
LONG_DESCRIPTION = open('README.md').read()
NAME = "visualprogressbar"
AUTHOR = "Ruaridh Thomson"
AUTHOR_EMAIL = "echelous@me.com"
MAINTAINER = "Ruaridh Thomson"
MAINTAINER_EMAIL = "echelous@me.com"
URL = ''
DOWNLOAD_URL = 'http://github.com/ruaridht/visualprogressbar'
LICENSE = 'MIT License'
VERSION = get_version()

# Make sure submodules are updated and synced
root_dir = os.path.abspath(os.path.dirname(__file__))
require_clean_submodules(root_dir, sys.argv)

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      url=URL,
      download_url=DOWNLOAD_URL,
      license=LICENSE,
      cmdclass={'submodule': UpdateSubmodules,
                'buildjs': BuildJavascript},
      packages=['visualprogressbar'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4'],
      )
