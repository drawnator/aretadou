def test1():
    with open("one_note_blank.xm","rb") as f:
        bytes = f.read()
        print(bytes[0:17]) #ID text "Extended module"
        print(bytes[17:17+20]) #module name 20*"0"
        print(bytes[37:37+1]) #$ "1A"
        print(bytes[38:38+20]) #Tracker name "MilkyTracker 1.03.00"
        print(bytes[58:58+2]) #version number "04 01"
        #header size
        print(bytes[60:60+4],int.from_bytes(bytes[60:60+4],byteorder='little'),"header")
        #Song length (in patten order table)
        print(bytes[64:64+2],int.from_bytes(bytes[64:64+2], byteorder='little'),"song length")
        #restart position
        print(bytes[66:66+2],int.from_bytes(bytes[66:66+2], byteorder='little'),"restart")
        #number of channels
        print(bytes[68:68+2],int.from_bytes(bytes[68:68+2], byteorder='little'),"chanells")
        #number of patterns
        print(bytes[70:70+2],int.from_bytes(bytes[70:70+2], byteorder='little'),"patterns")
        #number of instruments
        print(bytes[72:72+2],int.from_bytes(bytes[72:72+2], byteorder='little'),"instruments")
        #flags
        print(bytes[74:74+2],int.from_bytes(bytes[74:74+2], byteorder='little'),"flags")
        #default tempo
        print(bytes[76:76+2],int.from_bytes(bytes[76:76+2], byteorder='little'),"tempo")
        #default BPM
        print(bytes[78:78+2],int.from_bytes(bytes[78:78+2], byteorder='little'),"bpm")
        #pattern order table
        print(bytes[80:80+256])
        #pattern header
        print(bytes[336:336+4],int.from_bytes(bytes[336:336+4], byteorder='little'),"pattern header length")
        print(bytes[340:340+1],int.from_bytes(bytes[340:340+1], byteorder='little'),"packing type")
        print(bytes[341:341+2],int.from_bytes(bytes[341:341+2], byteorder='little'),"number of rows")
        print(bytes[343:343+2],int.from_bytes(bytes[343:343+2], byteorder='little'),"packed pattern data size")
        #row 1
        print("row1")
        print(bytes[345:345+1],bin(int.from_bytes(bytes[345:345+1], byteorder='little')),"note value")
        print(bytes[346:346+1],bin(int.from_bytes(bytes[346:346+1], byteorder='little')),"note")
        print(bytes[347:347+1],bin(int.from_bytes(bytes[347:347+1], byteorder='little')),"instrument")
        #row 2
        print("row2")
        print(bytes[355:355+1],bin(int.from_bytes(bytes[355:355+1], byteorder='little')),"note value")
        print(bytes[356:356+1],bin(int.from_bytes(bytes[356:356+1], byteorder='little')),"note")
        print(bytes[357:357+1],bin(int.from_bytes(bytes[357:357+1], byteorder='little')),"instrument")
        #row 3
        print("row3")
        print(bytes[365:365+1],bin(int.from_bytes(bytes[365:365+1], byteorder='little')),"note value")
        print(bytes[366:366+1],bin(int.from_bytes(bytes[366:366+1], byteorder='little')),"note")
        print(bytes[367:367+1],bin(int.from_bytes(bytes[367:367+1], byteorder='little')),"instrument")

        #todo transform all int.from_bytes(bytes[345:345+1] into bytes[345:345+1][0]
        # print(bytes[345:345+1],int.from_bytes(bytes[345:345+1], byteorder='little'),bytes[345:345+1][0],bytes[345:345+1])
        # print(bytes[345:345+1],int.from_bytes(bytes[345:345+1], byteorder='little'),"note")
        # print(bytes[346:346+1],int.from_bytes(bytes[346:346+1], byteorder='little'),"instrument")
        # print(bytes[347:347+1],int.from_bytes(bytes[347:347+1], byteorder='little'),"volume")
        # print(bytes[348:348+1],int.from_bytes(bytes[348:348+1], byteorder='little'),"effect")
        # print(bytes[349:349+1],int.from_bytes(bytes[349:349+1], byteorder='little'),"effect parameter")
        #row 2
        # print(bytes[350:350+1],int.from_bytes(bytes[350:350+1], byteorder='little'),"note")
        # print(bytes[351:351+1],int.from_bytes(bytes[351:351+1], byteorder='little'),"instrument")
        # print(bytes[352:352+1],int.from_bytes(bytes[352:352+1], byteorder='little'),"volume")
        # print(bytes[353:353+1],int.from_bytes(bytes[353:353+1], byteorder='little'),"effect")
        # print(bytes[354:354+1],int.from_bytes(bytes[354:354+1], byteorder='little'),"effect parameter")
        #instrument header
        # print(bytes[350:350+4],int.from_bytes(bytes[350:350+4], byteorder='little'),"instrument header length")
        # print(bytes[354:354+22],int.from_bytes(bytes[354:354+22], byteorder='little'),"instrument name")
        # print(bytes[354+22:354+22+1],int.from_bytes(bytes[354+22:354+22+1], byteorder='little'),"instrument type")
        # print(bytes[354+23:354+23+2],int.from_bytes(bytes[354+23:354+23+2], byteorder='little'),"number of samples")

def test2():
    file = XMParser("one_note_blank.xm")
    # print(file.bytes[336:336+4])
    print(file.get_number_of_patterns())
    print(file.patterns[0].number_of_rows)
    print(file.get_number_of_channels())
    for note in file.patterns[0].row_data:
        print(note[0].note)
    # print(file.patterns[0].row_data[0][0].note)

class XMParser(object):

    def __init__(self, file):
        self._pattern_start = 336
        self.file = file
        self.bytes = None
        self._parse()
        self.header_size = self.bytes[60:60+4][0]
        self.song_length = self.bytes[64:64+2][0]
        self.restart_position = self.bytes[66:66+2][0]
        self.number_of_channels = self.bytes[68:68+2][0]
        self.number_of_patterns = self.bytes[70:70+2][0]
        self.number_of_instruments = self.bytes[72:72+2][0]
        self.flags = self.bytes[74:74+2][0]
        self.default_tempo = self.bytes[76:76+2][0]
        self.default_bpm = self.bytes[78:78+2][0]

    def _parse(self):
        with open(self.file, "rb") as f:
            self.bytes = f.read()
        self.patterns = []
        for i in range(self.get_number_of_patterns()):
            self.patterns.append(self.XMpattern(self.bytes, self._pattern_start))
            self._pattern_start = self.patterns[-1].get_offset() + 1
        

    def get_patterns(self,pattern_number):
        return self.patterns[pattern_number]

    class XMpattern(object):
        def __init__(self, bytes, offset, number_of_channels=8):
            self.bytes = bytes
            self._offset = offset
            self.number_of_channels = number_of_channels
            self._parse()

        class XMpatternNote(object):
            def __init__(self, note=b'\x00', instrument=b'\x00', volume=b'\x00', effect=b'\x00', effect_parameter=b'\x00'):
                self.note = note
                self.instrument = instrument
                self.volume = volume
                self.effect = effect
                self.effect_parameter = effect_parameter

        def _parse(self):
            self.pattern_header_length = int.from_bytes(self.bytes[self._offset:self._offset+4], byteorder='little')
            self.packing_type = 0
            self.number_of_rows = int.from_bytes(self.bytes[self._offset+5:self._offset+5+2], byteorder='little')
            self.packed_pattern_data_size = int.from_bytes(self.bytes[self._offset+7:self._offset+7+2], byteorder='little')
            self._offset += 9
            self.row_data = [[] for i in range(self.number_of_rows)]
            for row in range(self.number_of_rows):
                for channel in range(self.number_of_channels):
                    self.row_data[row].append(self._get_channel_data())
                    self._offset += 1
        
        def _get_channel_data(self):
            pattern = self.bytes[self._offset:self._offset+1]
            note = pattern[0] & 1
            instrument = pattern[0] & 2
            volume = pattern[0] & 4
            effect = pattern[0] & 8
            effect_parameter = pattern[0] & 16
            if note:
                self._offset += 1
                note = self.bytes[self._offset:self._offset+1]
            if instrument:
                self._offset += 1
                instrument = self.bytes[self._offset:self._offset+1]
            if volume:
                self._offset += 1
                volume = self.bytes[self._offset:self._offset+1]
            if effect:
                self._offset += 1
                effect = self.bytes[self._offset:self._offset+1]
            if effect_parameter:
                self._offset += 1
                effect_parameter = self.bytes[self._offset:self._offset+1]
            return self.XMpatternNote(note, instrument, volume, effect, effect_parameter)
        
        def get_row_data(self):
            return self.row_data
        
        def get_number_of_rows(self):
            return self.number_of_rows
        
        def get_packed_pattern_data_size(self):
            return self.packed_pattern_data_size
        
        def get_offset(self):
            return self._offset
            

    def get_header_size(self):
        return int.from_bytes(self.bytes[60:60+4], byteorder='little')

    def get_song_length(self):
        return int.from_bytes(self.bytes[64:64+2], byteorder='little')

    def get_restart_position(self):
        return int.from_bytes(self.bytes[66:66+2], byteorder='little')

    def get_number_of_channels(self):
        return int.from_bytes(self.bytes[68:68+2], byteorder='little')

    def get_number_of_patterns(self):
        return int.from_bytes(self.bytes[70:70+2], byteorder='little')

    def get_number_of_instruments(self):
        return int.from_bytes(self.bytes[72:72+2], byteorder='little')

    def get_flags(self):
        return int.from_bytes(self.bytes[74:74+2], byteorder='little')

    def get_default_tempo(self):
        return int.from_bytes(self.bytes[76:76+2], byteorder='little')

    def get_default_bpm(self):
        return int.from_bytes(self.bytes[78:78+2], byteorder='little')


# def _analize():

# if __name__ == "__main__":
#     import sys
#     dir = sys.argv[1]
#     print(dir)

if __name__ == "__main__":
    test2()
