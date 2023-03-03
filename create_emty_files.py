import math
import pprint

full_tact_sep = "|"
semi_tact_sep = "."
quat_tact_sep = "."
left_tact_bracket = "["
right_line_bracket = "]"
track_sep_padding = 1
track_sep = "="

tracks_line_sep_pad = 2
tracks_line_sep = "&"

part_sep_padding_up = 2
part_sep_padding_down = 1
part_sep = "+"

def with_brackets(s):
    return f"{left_tact_bracket}{s}{right_line_bracket}"

        
def multiple_tacts(tact_count: int, start_from: int, tracks_count: int = 1)->list:
    quater = "----"
    semi_tact = quat_tact_sep.join([quater] * 2)
    single_tact_line = semi_tact_sep.join([semi_tact] * 2) 
    tact_id_line = full_tact_sep.join(
       [
           str(id) + (" " * (len(single_tact_line) - len(str(id)))) 
           for id in range(start_from, start_from + tact_count)
       ] 
    )
    tact_line = full_tact_sep.join([single_tact_line for x in range(tact_count)])
    tracks_separator_line = ([""] * track_sep_padding) + [track_sep * len(tact_line)] + ([""] * track_sep_padding)
    single_track = [tact_line] * 6
    
    result = [tact_id_line]
    for i in range(tracks_count - 1):
        result += single_track
        result += tracks_separator_line
    result += single_track
    return result
    

class SongPart:
    def __init__(self, name: str, size: str) -> None:
       self.name = name
       self.size = size
    
    def _line_sizes(self, line_size:int):
        tacts_left = self.size
        result = []
        while tacts_left > 0:
            current_line_size = min(tacts_left, line_size) 
            tacts_left -= current_line_size
            result += [current_line_size]
        
        return result
           
       
    def to_string(self, starts_from: int, tracks_count: int, tacts_per_line: int):
        result =  \
            [""] * part_sep_padding_up + \
            [part_sep * 10] + \
            [self.name] + \
            [part_sep * 10] + \
            [""] * part_sep_padding_down
            
        initial_tact_id = starts_from
        for tacts_count in self._line_sizes(tacts_per_line):
            current_tacts =  multiple_tacts(tacts_count, initial_tact_id, tracks_count)
            result += \
                current_tacts + \
                [""] * tracks_line_sep_pad + \
                [tracks_line_sep * len(current_tacts[0])] + \
                [""] * tracks_line_sep_pad
        
            initial_tact_id += tacts_count
        
        return result

class Song:
    def __init__(self, name: str, tacts_per_line: int, tracks_number: int, parts: dict[str, int]) -> None:
        self.name = name
        self.tacts_per_line = tacts_per_line
        self.tracks_number = tracks_number
        self.parts: list[SongPart] = list([SongPart(x, parts.get(x)) for x in parts.keys()])
    
    def title_to_strint(self):
        return [self.name.upper()] + ["=+" * 10] + [""]*2

    def to_string(self):
        result = []
        
        result += self.title_to_strint()

        tact_id = 1
        for part in self.parts:
            result += part.to_string(tact_id, self.tracks_number, self.tacts_per_line)
            tact_id += part.size
        
        return result

    def _to_file(self, id: int, name: str, lines: list):
        with open("{:02}".format(id) + "_" + name.lower().replace(" ", "_"), "w") as writer:
            writer.writelines("\n".join(lines))

    def to_files(self):
        self._to_file(0, self.name, self.title_to_strint())
        id = 1
        tact_id = 1
        for part in self.parts:
            self._to_file(id, part.name, part.to_string(tact_id, self.tracks_number, self.tacts_per_line))
            tact_id += part.size
            id += 1
        
        
        
song = Song(
    name = "Head over heels",
    tacts_per_line=3,
    tracks_number=2,
    parts={
        "Intro" : 6,
        "Phrase 1": 8,
        "Chorus 1": 4 
    }
)       

print("\n".join(song.to_string()))
song.to_files()