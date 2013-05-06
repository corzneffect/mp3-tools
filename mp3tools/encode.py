import os
import logging

LOGGER = logging.getLogger(__name__)

REPLACE_CHARS = [('(','_'),
                 (')','_'),
                 ("'",""),
                 (' ','_'),
                 ("\\","-"),
                 ("/","-"),
                 ("&","and")]


class EncodingError(Exception):
    pass

def make_nice_filename(name):
    for rc in REPLACE_CHARS:
        name=name.replace(rc[0],rc[1])
    return name.lower()

class Encoder(object):
    def __init__(self, cdinfo, base_mp3_dir):
        self.cdinfo = cdinfo
        self.base_mp3_dir = base_mp3_dir
        self.artist_dir =  make_nice_filename(self.cdinfo.artist)
        self.album_dir =  make_nice_filename(self.cdinfo.album)

    def get_output_path(self,track_num):
        return os.path.join(
            self.base_mp3_dir, self.artist_dir, self.album_dir,
            make_nice_filename(
                "%.02d_" %(track_num) + self.cdinfo.titles[track_num-1]
                ) + '.mp3'
            )
    
    def create_artist_album_dirs(self):
        if not os.path.exists(os.path.join(self.base_mp3_dir,self.artist_dir)):
            os.mkdir(os.path.join(self.base_mp3_dir,self.artist_dir))
        if not os.path.exists(os.path.join(self.base_mp3_dir,self.artist_dir,
                                           self.album_dir)):
            os.mkdir(os.path.join(self.base_mp3_dir,self.artist_dir,
                                  self.album_dir))

    def get_encoder_cmd(self, track_num, wav_file):
        cmd = (
            'lame -h -b 320 --quiet --tt \"{title}\" --ta \"{artist}\" ' + \
                '--tl \"{album}\" --ty \"{year}\" --tn \"{track_num}\" '+\
                '--tg \"{genre}\" \"{wav_file}\" \"{out_file}\"'
            ).format(title = self.cdinfo.titles[track_num-1],
                     artist = self.cdinfo.artist,
                     album = self.cdinfo.album,
                     year = self.cdinfo.year,
                     track_num = track_num,
                     genre = self.cdinfo.genre,
                     wav_file = wav_file,
                     out_file = self.get_output_path(track_num)
                     )
        return cmd

    def encode(self, track_num, wav_file):
        LOGGER.info('Encoding track %d; wav_file = %s', track_num, wav_file)
        self.create_artist_album_dirs()
        failure = os.system(self.get_encoder_cmd(track_num, wav_file))
        if failure:
            raise EncodingError()
        os.remove(wav_file)

    
