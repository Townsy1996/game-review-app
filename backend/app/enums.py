from enum import Enum


class AgeRating(str, Enum):
    pegi_3 = "PEGI 3"
    pegi_7 = "PEGI 7"
    pegi_12 = "PEGI 12"
    pegi_16 = "PEGI 16"
    pegi_18 = "PEGI 18"


class Genre(str, Enum):
    ADVENTURE = "Adventure"
    ACTION = "Action"
    RPG = "RPG"
    SHOOTER = "Shooter"
    STRATEGY = "Strategy"
    SIMULATION = "Simulation"
    SPORTS = "Sports"
    RACING = "Racing"
    PUZZLE = "Puzzle"
    PLATFORMER = "Platformer"
    FIGHTING = "Fighting"
    INDIE = "Indie"
    HORROR = "Horror"
    SURVIVAL = "Survival"
    MOBA = "MOBA"
    MMORPG = "MMORPG"
    SANDBOX = "Sandbox"
    ROGUELIKE = "Roguelike"


class Platform(str, Enum):
    PC = "PC"
    PLAYSTATION_5 = "PlayStation 5"
    PLAYSTATION_4 = "PlayStation 4"
    XBOX_SERIES = "Xbox Series S/X"
    XBOX_ONE = "Xbox One"
    NINTENDO_SWITCH = "Nintendo Switch"
    NINTENDO_SWITCH_2 = "Nintendo Switch 2"
