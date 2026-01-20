from dataclasses import dataclass

@dataclass
class Artist:
    id : int
    name : str
    numero_album : None

    def __str__(self):
        return f"{self.id}, {self.name}"

    def __hash__(self):
        return hash(self.id)