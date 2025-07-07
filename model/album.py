from dataclasses import dataclass


@dataclass
class Album:
    albumId : int
    titolo : str
    artistaId :int
    durata :str


    def __hash__(self):
        return self.albumId
    def __eq__(self, other):
        return self.albumId == other.albumId
    def __str__(self):
        return (f"album: {self.albumId}, artista : "
                f"{self.artistaId}, titolo : {self.titolo}, durata : {self.durata}")