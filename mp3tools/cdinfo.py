import DiscID, CDDB
import logging
import os

LOGGER = logging.getLogger(__name__)

class CDInfoError(Exception):
    pass

class CDInfo(object):
    def __init__(self):
        self.id = ''
        self.num_tracks = 0
        self.genre = ''
        self.titles = []
        self.artist = ''
        self.album = ''
        self.year = ''

    def get_id(self):
        cdrom = DiscID.open('/dev/cdrom')
        self.id,self.num_tracks = DiscID.disc_id(cdrom)[:2]
        return self
        
    def from_dict(self, cdinfo_dict):
        self.genre = cdinfo_dict['genre']
        self.titles = cdinfo_dict['titles']
        self.artist = cdinfo_dict['artist']
        self.album = cdinfo_dict['album']
        self.year = cdinfo_dict['year']
        if not len(self.titles) == self.num_tracks:
            raise CDInfoError('title list not xconsistent to num_tracks')

    def from_cddb(self):
        (query_stat, query_info) = CDDB.query((self.id, self.num_tracks))
        
        if query_stat == 200:
            LOGGER.info("success!\nQuerying CDDB for track info of `%s'... " % 
                        query_info['title'])

            (read_stat, read_info) = CDDB.read(query_info['category'], 
                                               query_info['disc_id'])
            if read_stat == 210:
                LOGGER.info("success!")
                for i in range(0, self.num_tracks):
                    LOGGER.info("Track %.02d: %s",i+1, 
                                read_info['TTITLE%s' + `i`])
            else:
                msg = "failure getting track info, status: %i" % read_stat
                LOGGER.error(msg)
                raise Exception(msg)

        elif query_stat == 210 or query_stat == 211:
            print "multiple matches found! Matches are:"
            for i in range(len(query_info)):
                print "%d -ID: %s Category: %s Title: %s" % \
                    (i,query_info[i]['disc_id'],
                     query_info[i]['category'],
                     query_info[i]['title'])
            index=int(raw_input("choose index (type index and return)"))
            (read_stat, read_info) = CDDB.read(query_info[index]['category'], 
                                               query_info[index]['disc_id'])
        else:
            msg = "failure getting disc info, status %i" % query_stat
            LOGGER.error(msg)
            raise Exception(msg)
        
        #Make sure the genre is OK
        genrelist=os.popen('lame --genre-list').readlines()
        genredict={}
        for l in genrelist:
            genredict[l[1].strip()]=l[0].strip()

        if read_info['DGENRE']=='Indie Rock':
            read_info['DGENRE'] = 'Indie'

        #default genre is Alternative
        self.genre = genredict.get(read_info['DGENRE'],'20') 
        self.titles = [read_info['TTITLE%d' %(i+1)] for i in range(
                self.num_tracks)] 
        artist,album = os.path.split(read_info['DTITLE'])
        self.artist = artist.strip()
        self.album = album.strip()
        self.year = read_info['DYEAR']
        return self
