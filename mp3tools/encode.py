import os
import logging
import subprocess

LOGGER = logging.getLogger(__name__)

REPLACE_CHARS = [('(', '_'),
                 (')', '_'),
                 ("'", ""),
                 (' ', '_'),
                 ("\\", "-"),
                 ("/", "-"),
                 ("&", "and"),
                 (u'\u2026', '...')]


class EncodingError(Exception):
    pass

def make_nice_filename(name):
    for rc in REPLACE_CHARS:
        name = name.replace(rc[0], rc[1])
    return name.lower()

class Encoder(object):
    def __init__(self, cdinfo, base_mp3_dir):
        self.cdinfo = cdinfo
        self.base_mp3_dir = base_mp3_dir
        self.artist_dir = make_nice_filename(self.cdinfo.artist)
        self.album_dir = make_nice_filename(self.cdinfo.album)

    def get_output_path(self,track_num):
        return os.path.join(
            self.base_mp3_dir, self.artist_dir, self.album_dir,
            make_nice_filename(
                "%.02d_" %(track_num) + self.cdinfo.titles[track_num-1]
                ) + '.mp3'
            )
    
    def create_artist_album_dirs(self):
        if not os.path.exists(os.path.join(self.base_mp3_dir, self.artist_dir)):
            os.mkdir(os.path.join(self.base_mp3_dir, self.artist_dir))
        if not os.path.exists(os.path.join(self.base_mp3_dir, self.artist_dir,
                                           self.album_dir)):
            os.mkdir(os.path.join(self.base_mp3_dir, self.artist_dir,
                                  self.album_dir))

    def get_encoder_cmd(self, track_num, wav_file):
        out_file=self.get_output_path(track_num)
        LOGGER.debug('Output file: %s', out_file)
        LOGGER.debug(u'--tl \"{album}\"'.format(album=self.cdinfo.album))
        cmd = 'lame -h -b 320 --quiet '
        for name, value in [('tt', self.cdinfo.titles[track_num-1]),
                            ('ta', self.cdinfo.artist),
                            ('tl', self.cdinfo.album),
                            ('ty', self.cdinfo.year),
                            ('tn', track_num),
                            ('tg', self.cdinfo.genre)]:
            cmd += u'--{} "{}" '.format(name, value)
        cmd += '"{wav_file}" "{out_file}"'.format(
            wav_file=wav_file, out_file=self.get_output_path(track_num))
        LOGGER.debug('Command: %s', cmd)
        return cmd

    def encode(self, track_num, wav_file):
        LOGGER.info('Encoding track %d; wav_file = %s', track_num, wav_file)
        self.create_artist_album_dirs()
        try:
            subprocess.check_output(self.get_encoder_cmd(track_num, wav_file), 
                                    stderr=subprocess.STDOUT, shell = True)
        except Exception as err:
            if hasattr(err, 'output'):
                LOGGER.error('output: %s', err.output)
            raise
        finally:
            pass
            os.remove(wav_file)

    
