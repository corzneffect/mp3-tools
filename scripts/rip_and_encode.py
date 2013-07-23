#!/bin/env python

import Queue
import threading
import argparse
import logging
import warnings

from mp3tools import rip, encode, cdinfo

NUM_ENCODING_THREADS = 2

LOGGER = logging.getLogger()
logging.basicConfig(level = logging.INFO, filename = 'rip_and_encode.log')

def main():
    parser = argparse.ArgumentParser(description='Rip and encode a CD yo.')
    parser.add_argument(
        '-f', '--cdinfo-file', dest = 'cdinfo_file', type = str,
        help = 'file containing dictionary with artist, album,' +\
            'genre, year and titles'
        )
    parser.add_argument(
        '-d', '--base-mp3-dir', dest = 'base_mp3_dir', type = str,
        help = 'base directory for mp3s', default = '/space/mp3'
        )
    
    args = parser.parse_args()


    cd_info = cdinfo.CDInfo().get_id()

    if args.cdinfo_file:
        cd_info.from_dict(eval(open(args.cdinfo_file).read()))
    else:
        try:
            cd_info.from_cddb()
        except cdinfo.CDDBError:
            msg = "Failed CDDB lookup - trying MusicBrainz"
            warnings.warn(msg)
            LOGGER.warning(msg)
            cd_info.from_musicbrainz()

    encoding_queue = Queue.Queue()
    encoder = encode.Encoder(cd_info, args.base_mp3_dir)

    def encoding_worker():
        while True:
            encoder.encode(*encoding_queue.get())
            encoding_queue.task_done()

    encoding_threads = []
    for i in range(NUM_ENCODING_THREADS):
        encoding_threads.append(threading.Thread(target = encoding_worker))
        encoding_threads[-1].daemon = True
        encoding_threads[-1].start()

    ripper = rip.Ripper()
    for track_num in range(1, cd_info.num_tracks + 1):
        wav_file = ripper.rip(track_num)
        encoding_queue.put((track_num, wav_file))

    encoding_queue.join()
    ripper.clean()

if __name__ == '__main__':
    main()
