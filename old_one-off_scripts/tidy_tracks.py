import os
import logging
from optparse import OptionParser
parser = OptionParser()
parser.add_option('-n', '--dry-run', dest = 'dry_run', action='store_true',
                  help='Do nothing, just say what would be done')
(options,args)=parser.parse_args()

logging.basicConfig(level=logging.INFO, filename='tidy_tracks.log', mode='o')
files=os.popen('find -name "*.mp3"').read().split('\n')

def any_upper(s):
    for si in s:
        if si.isupper():
            return True
    return False

for f in files[:-1]:
    if (' ' in f) or any_upper(os.path.split(f)[-1]):
        new_filename=f.replace(' ','_').lower()
        if os.path.exists(new_filename):
            logging.warning('%s already exists, deal with %s this manually',
                            new_filename, f)
        else:
            logging.info('renaming "%s" "%s"', f, new_filename)
            if not options.dry_run:
                try:
                    os.rename(f, new_filename)
                except:
                    logging.error('Error moving "%s" to "%s"', f, new_filename)
    


