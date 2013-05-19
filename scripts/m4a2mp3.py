import os
import logging
from optparse import OptionParser
parser = OptionParser()
parser.add_option('-n', '--dry-run', dest = 'dry_run', action='store_true',
                  help='Do nothing, just say what would be done')
(options,args)=parser.parse_args()

logging.basicConfig(level=logging.INFO, filename='m4a2mp3.log', mode='o')
files=os.popen('find -name "*.m4a"').read().split('\n')

def run_command(cmd):
    logging.info('running "%s"' %cmd)
    if not options.dry_run:
        failure=os.system(cmd)
        if failure:
            raise Exception('command "%s" failed' %cmd)

for f in files[:-1]:
    logging.info('Processing %s',f)
    if os.path.split(f)[-1].startswith('.'):
        logging.info('Deleting %s', f)
        if not options.dry_run:
            os.remove(f)
    else:
        f_ = f.replace(
            ' ','\ ').replace(
            "'","\\'").replace(
                "&","\&").replace(
                "&","\&").replace(
                    "(","\(").replace(
                    ")","\)")
        logging.info('adjusting filename string to %s',f_)
        wav_file=f_.replace('.m4a','.wav')
        run_command('faad %s' % f_)
        mp3_file=f_.replace('.m4a','.mp3')
        run_command('lame %s %s' %(wav_file, mp3_file))
        run_command('rm %s %s' %(f_,wav_file))

