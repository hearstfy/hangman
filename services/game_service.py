import random

from models.hangman import Hangman


class GameService:
    def __init__(self):
        self.games = {}
        self.next_game_id = 1

    def create_game(self, words=None, guess_limit=5):
        if words is None:
            words = ["3dhubs", "marvin", "print", "filament", "order", "layer"]

        if len(words) <= 0:
            raise ValueError("words must have at least 1 word")

        if guess_limit <= 0:
            raise ValueError("guess_limit must be greater than 0")

        rand_word = words[random.randint(0, len(words) - 1)]
        game = Hangman(rand_word, guess_limit)
        game_id = self.next_game_id
        self.games[game_id] = game
        self.next_game_id += 1
        return game_id, Hangman(rand_word, guess_limit)

    def get_game(self, game_id):
        return self.games.get(game_id)

    def to_json(self, game_id, game: Hangman):
        return {
            'gameId': game_id,
            'state': game.state.__str__(),
            'revealedWord': game.revealed_word,
            'numFailedGuessesRemaining': game.num_failed_guesses_remaining,
            'score': game.get_score()
        }
