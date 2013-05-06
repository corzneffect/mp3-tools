import unittest
import difflib

from mp3tools import encode, cdinfo

class TestEncoder(unittest.TestCase):
    def test_get_encoder_cmd(self):
        cd_info = cdinfo.CDInfo()
        cd_info.num_tracks = 7
        cd_info.from_dict(
            {'artist':'The Phoenix Foundation',
             'album':'Fandango - disk A',
             'genre':'Alternative',
             'year':'2013',
             'titles':['Black Mould',
                       'Modern Rock',
                       'The Captain',
                       'Thames Soup',
                       'Evolution Did',
                       'Inside Me Dead',
                       'Corale']}
            )
        encoder = encode.Encoder(cd_info,'/who/cares')
        expected = 'lame -h -b 320 --quiet --tt \"Black Mould\" '+\
            '--ta \"The Phoenix Foundation\" --tl \"Fandango - disk A\" ' +\
            '--ty \"2013\" --tn \"1\" --tg \"Alternative\" '+\
            '\"a_file.wav\"' +\
            ' \"/who/cares/the_phoenix_foundation/fandango_-_disk_a/'+\
            '01_black_mould.mp3\"'
        returned = encoder.get_encoder_cmd(1,'a_file.wav')
        self.assertEqual(
            returned, expected,            
            "Commands differ.\nReturned:\n{}\nExpected:\n{}\nOpcodes = {}".format(
                returned,
                expected,
                difflib.SequenceMatcher(a = returned, 
                                        b = expected).get_opcodes()
                )
            )

if __name__ == '__main__':
    unittest.main()
