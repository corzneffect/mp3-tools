import os
import logging
from optparse import OptionParser
parser = OptionParser()
parser.add_option('-n', '--dry-run', dest = 'dry_run', action='store_true',
                  help='Do nothing, just say what would be done')
(options,args)=parser.parse_args()

logging.basicConfig(level=logging.INFO, filename='tidy_albums.log', mode='o')
dirs=os.popen('find -maxdepth 2').read().split('\n')
for d in dirs[:-1]:
    if (' ' in d) or os.path.split(d)[1][0].isupper():
        new_dir=d.replace(' ','_').lower()
        if os.path.exists(new_dir):
            logging.warning('%s already exists, deal with %s this manually',
                            new_dir, d)
        else:
            logging.info('renaming "%s" "%s"', d, new_dir)
            if not options.dry_run:
                try:
                    os.rename(d, new_dir)
                except:
                    logging.error('Error moving "%s" to "%s"', d, new_dir)
    


