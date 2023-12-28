from dataclasses import dataclass


@dataclass
class Rarity:
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"
    MYTHIC = "Mythic"
    SPECIAL = "Special"
    X = "No one knows about it."
