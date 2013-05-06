import tempfile
import shutil
import os

class Ripper(object):
    def __init__(self):
        self.out_dir = tempfile.mkdtemp(dir = '/dev/shm')
    
    def rip(self,track_num):
        out_file = tempfile.mkstemp(dir = self.out_dir, suffix = '.wav')[1]
        os.system('cdparanoia \"%d\" %s' % (track_num,out_file))
        return out_file
                  
    def clean(self):
        shutil.rmtree(self.out_dir)
