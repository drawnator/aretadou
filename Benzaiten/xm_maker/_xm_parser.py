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
    print(bytes[345:345+1],int.from_bytes(bytes[345:345+1], byteorder='little'),"note")
    print(bytes[346:346+1],int.from_bytes(bytes[346:346+1], byteorder='little'),"instrument")
    print(bytes[347:347+1],int.from_bytes(bytes[347:347+1], byteorder='little'),"volume")
    print(bytes[348:348+1],int.from_bytes(bytes[348:348+1], byteorder='little'),"effect")
    print(bytes[349:349+1],int.from_bytes(bytes[349:349+1], byteorder='little'),"effect parameter")
    #row 2
    print(bytes[350:350+1],int.from_bytes(bytes[350:350+1], byteorder='little'),"note")
    print(bytes[351:351+1],int.from_bytes(bytes[351:351+1], byteorder='little'),"instrument")
    print(bytes[352:352+1],int.from_bytes(bytes[352:352+1], byteorder='little'),"volume")
    print(bytes[353:353+1],int.from_bytes(bytes[353:353+1], byteorder='little'),"effect")
    print(bytes[354:354+1],int.from_bytes(bytes[354:354+1], byteorder='little'),"effect parameter")
    #instrument header
    print(bytes[355:355+4],int.from_bytes(bytes[355:355+4], byteorder='little'),"instrument header length")
    print(bytes[359:359+22],int.from_bytes(bytes[359:359+22], byteorder='little'),"instrument name")
    print(bytes[381:381+1],int.from_bytes(bytes[381:381+1], byteorder='little'),"instrument type")
    print(bytes[382:382+2],int.from_bytes(bytes[382:382+2], byteorder='little'),"number of samples")


class XMParser(object):

    def __init__(self, file):
        self.pattern_start = 336
        self.file = file
        self.bytes = None
        self._parse()

    def _parse(self):
        with open(self.file, "rb") as f:
            self.bytes = f.read()

    def get_pattern(self, pattern_number):
        pattern_index = 0
        local_pattern_start = self.pattern_start
        while pattern_index < pattern_number:
            self.patterns = self.XMpattern(self.bytes, self.pattern_start)
            local_pattern_start += self.patterns.pattern_header_length
            pattern_index += 1
        return self.patterns

    class XMpattern(object):
        def __init__(self, bytes, offset):
            self.bytes = bytes
            self.offset = offset
            self._parse()

        class XMpatternRow(object):
            def __init__(self, note, instrument, volume, effect, effect_parameter):
                self.note = note
                self.instrument = instrument
                self.volume = volume
                self.effect = effect
                self.effect_parameter = effect_parameter

        def _parse(self):
            self.pattern_header_length = int.from_bytes(self.bytes[self.offset:self.offset+4], byteorder='little')
            self.packing_type = 0
            self.number_of_rows = int.from_bytes(self.bytes[self.offset+5:self.offset+5+2], byteorder='little')
            self.packed_pattern_data_size = int.from_bytes(self.bytes[self.offset+7:self.offset+7+2], byteorder='little')
            self.packed_pattern_data = []
            for i in range(self.packed_pattern_data_size+1):
                note = self.bytes[self.offset+9+i]
                instrument = self.bytes[self.offset+9+i+1]
                volume = self.bytes[self.offset+9+i+2]
                effect = self.bytes[self.offset+9+i+3]
                effect_parameter = self.bytes[self.offset+9+i+4]
                self.packed_pattern_data.append(self.XMpatternRow(note, instrument, volume, effect, effect_parameter))

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
