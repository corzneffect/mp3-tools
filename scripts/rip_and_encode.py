#!/bin/env python

import Queue
import threading
import argparse
import logging
import traceback

from mp3tools import rip, encode, cdinfo

NUM_ENCODING_THREADS = 2

LOGGER = logging.getLogger()

def main():
    parser = argparse.ArgumentParser(description='Rip and encode a CD yo.')
    parser.add_argument(
        '-f', '--cdinfo-file', dest='cdinfo_file', type=str,
        help='file containing dictionary with artist, album,' +\
            'genre, year and titles'
        )
    parser.add_argument(
        '-d', '--base-mp3-dir', dest='base_mp3_dir', type=str,
        help='base directory for mp3s', default='/space/mp3'
        )

    parser.add_argument(
        '-l', '--logging-level', dest='logging_level', type=str,
        help='Logging level (e.g. DEBUG, INFO, WARNING)',
        default='INFO'
        )

    args = parser.parse_args()

    logging.basicConfig(level=eval('logging.{}'.format(args.logging_level)))#,
#                        filename = 'rip_and_encode.log')

    cd_info = cdinfo.CDInfo().get_id()

    if args.cdinfo_file:
        cd_info.from_dict(eval(open(args.cdinfo_file).read()))
    else:
        cd_info.from_musicbrainz()

    encoding_queue = Queue.Queue()
    encoder = encode.Encoder(cd_info, args.base_mp3_dir)

    def encoding_worker():
        while True:
            track_num, wav_file = encoding_queue.get()
            #try except here so that task_done is called regardless (so that
            #queue.join doesn't block)
            try:
                encoder.encode(track_num, wav_file)
            except:
                LOGGER.error('Encoding failed for track %d', track_num)
                LOGGER.error('Traceback: {}'.format(traceback.format_exc()))
            finally:
                encoding_queue.task_done()

    encoding_threads = []
    for i in range(NUM_ENCODING_THREADS):
        encoding_threads.append(threading.Thread(target = encoding_worker))
        encoding_threads[-1].daemon = True
        encoding_threads[-1].start()

    with rip.Ripper() as ripper:
        for track_num in range(1, cd_info.num_tracks + 1):
            wav_file = ripper.rip(track_num)
            encoding_queue.put((track_num, wav_file))
            
        encoding_queue.join()
        ripper.clean()

if __name__ == '__main__':
    main()
