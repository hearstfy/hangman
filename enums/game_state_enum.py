from enum import Enum


class GameState(Enum):
    IN_PROGRESS = 0
    WON = 1
    LOST = 2

    def __str__(self):
        enum_string = {
            self.IN_PROGRESS: 'IN_PROGESS',
            self.WON: 'WON',
            self.LOST: 'LOST',
        }

        return enum_string[self]