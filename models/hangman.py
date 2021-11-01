from enums.game_state_enum import GameState
from enums.guess_result_enum import GuessResult


class Hangman:
    def __init__(self, word, failed_guesses_limit):
        if failed_guesses_limit <= 0:
            raise ValueError("failed_guesses_limit must be over 0")

        if len(word) <= 0:
            raise ValueError("word must have at least 1 letter")

        self.word = word
        self.state = GameState.IN_PROGRESS
        self.guesses = []
        self.failed_guess_limit = failed_guesses_limit
        self.num_failed_guesses_remaining = failed_guesses_limit
        self.revealed_word = "".join(["_" for i in range(len(word))])
        self.num_revealed_letters = 0

    def get_score(self):
        points_per_letter = 20
        points_per_remaining_guess = 10
        points = self.num_revealed_letters * points_per_letter
        points += (
                self.num_failed_guesses_remaining
                * points_per_remaining_guess
        )
        return points

    def guess(self, input_letter):
        if len(input_letter) > 1:
            return self.__get_response(GuessResult.FAIL_INVALID_INPUT.value, GuessResult.FAIL_INVALID_INPUT.__str__())
        if self.num_failed_guesses_remaining <= 0:
            return self.__get_response(GuessResult.FAIL_ALREADY_GAME_OVER.value, GuessResult.FAIL_ALREADY_GAME_OVER.__str__())
        if input_letter in self.guesses:
            return self.__get_response(GuessResult.FAIL_ALREADY_GUESSED.value, GuessResult.FAIL_ALREADY_GUESSED.__str__())
        if input_letter in self.word:
            self.guesses.append(input_letter)
            self.num_revealed_letters += self.__reveal_word(input_letter)
            self.__check_game_state()
            return self.__get_response(GuessResult.CORRECT.value, "")
        if input_letter not in self.word:
            self.guesses.append(input_letter)
            self.num_failed_guesses_remaining -= 1
            self.__check_game_state()
            return self.__get_response(GuessResult.INCORRECT.value, GuessResult.INCORRECT.__str__())

    def __set_game_state(self, state):
        self.state = state

    def __check_game_state(self):
        if self.num_failed_guesses_remaining == 0:
            self.__set_game_state(GameState.LOST)

        if self.num_revealed_letters == len(self.word):
            self.__set_game_state(GameState.WON)

    def __reveal_word(self, letter):
        letter_index_list = self.__find_occurences(letter)
        self.num_revealed_letters += len(letter_index_list)
        self.__replace_by_index(letter_index_list, letter)
        return len(letter_index_list)

    def __find_occurences(self, letter_to_find):
        return [i for i, letter in enumerate(self.word) if letter == letter_to_find]

    def __replace_by_index(self, index_list, letter):
        char_list = list(self.revealed_word)
        for i in range(0, len(index_list)):
            char_list[index_list[i]] = letter

        self.revealed_word = "".join(char_list)

    def __get_response(self, value, error):
        return {
            "value": value,
            "error": error
        }
