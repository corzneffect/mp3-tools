import datetime
import DiscID, CDDB
import logging
import os
import musicbrainz2.disc as mbdisc
import musicbrainz2.webservice as mbws

LOGGER = logging.getLogger(__name__)

class CDInfoError(Exception):
    pass

class CDDBError(Exception):
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

    def from_musicbrainz(self):
        disc = mbdisc.readDisc()
        filter_ = mbws.ReleaseFilter(discId=disc.getId())
        service = mbws.WebService()
        query = mbws.Query(service)
        results = query.getReleases(filter_)
        self.genre = '' #musicbrainz does not support genres
        self.artist = results[0].release.artist.name
        self.album = results[0].release.getTitle()
        try:
            self.year = results[0].release.getEarliestReleaseDate(
            ).split('-')[0]
        except AttributeError:
            LOGGER.warning(
                "Couldn't' get year from MusicBrainz - using current year")
            self.year = str(datetime.datetime.now().year)
        self.titles = [
            track.getTitle() for track in results[0].release.getTracks()]
        return self
