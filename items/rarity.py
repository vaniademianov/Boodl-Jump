from dataclasses import dataclass
from other.cons import BLUE, DARK_RED, GREEN, ORANGE, PURPLE, WHITE, YELLOW

@dataclass
class RarityBase:
    name: str
    level: int
    color: tuple

    def __eq__(self, other):
        return self.level == other.level if isinstance(other, RarityBase) else NotImplemented

    def __lt__(self, other):
        return self.level < other.level if isinstance(other, RarityBase) else NotImplemented

    def __str__(self):
        return f"{self.name}"
    def __int__(self):
        return self.level
@dataclass
class Common(RarityBase):
    name: str = "Common"
    level: int = 0
    color: tuple = WHITE

@dataclass
class Uncommon(RarityBase):
    name: str = "Uncommon"
    level: int = 1
    color: tuple = GREEN

@dataclass
class Rare(RarityBase):
    name: str = "Rare"
    level: int = 2
    color: tuple = BLUE

@dataclass
class Epic(RarityBase):
    name: str = "Epic"
    level: int = 3
    color: tuple = PURPLE

@dataclass
class Legendary(RarityBase):
    name: str = "Legendary"
    level: int = 4
    color: tuple = YELLOW

@dataclass
class Mythic(RarityBase):
    name: str = "Mythic"
    level: int = 5
    color: tuple = ORANGE

@dataclass
class Special(RarityBase):
    name: str = "Special"
    level: int = 6
    color: tuple = DARK_RED

@dataclass
class X(RarityBase):
    name: str = "No one knows about it."
    level: int = 7
    color: tuple = WHITE
@dataclass
class Rarity:
    COMMON = Common
    UNCOMMMON = Uncommon
    RARE = Rare 
    EPIC = Epic 
    LEGENDARY = Legendary
    MYTHIC = Mythic
    SPECIAL = Special
    X = X 