from distutils.core import setup
import os
import glob
import re

##First, get version from Ungribwrapper/_version.py.  Don't import here
#as doing this in the setup.py can be problematic
VERSION_FILE='./mp3tools/_version.py'
matched = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                    open(VERSION_FILE, "rt").read(), re.M)
if matched:
    version_str = matched.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." %(VERSION_FILE))

def main():
    setup(name = 'mp3tools',
          version = version_str,
          description  = 'Turns CDs into mp3s',
          author       = 'Cory Davis',
          author_email = 'corzneffect@gmail.com',
          package_dir = {"mp3tools": "mp3tools"},
          packages = ["mp3tools"],
          scripts = glob.glob('scripts/*.py'),
          data_files = [],
          )

if __name__=='__main__':
    main()
