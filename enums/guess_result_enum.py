from enum import Enum


class GuessResult(Enum):
    CORRECT = 0
    INCORRECT = 1
    FAIL_INVALID_INPUT = 2
    FAIL_ALREADY_GAME_OVER = 3
    FAIL_ALREADY_GUESSED = 4

    def __str__(self):
        enum_string = {
            self.CORRECT: 'Correct',
            self.INCORRECT: 'Incorrect',
            self.FAIL_INVALID_INPUT: 'Invalid Input',
            self.FAIL_ALREADY_GAME_OVER: 'Game is already over',
            self.FAIL_ALREADY_GUESSED: 'Already guessed this letter',
        }

        return enum_string[self]
