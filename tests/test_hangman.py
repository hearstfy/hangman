import json
import sys
import unittest

from app import app
from enums.guess_result_enum import GuessResult
from services.game_service import GameService


# In my opinion testing every single function in a project is overkill and not needed.
# This test class unit tests, service functions not controllers.
# If I wanted to test the controller functions, I would check if they call relevant service functions
# with correct param values. But for this particular assessment it is not needed because service code
# does the real job and they should be tested


class HangmanTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.game_service = GameService()
        self.game_id, self.game = self.game_service.create_game(words=["3dhubs"], guess_limit=5)

    def test_create_game(self):
        response = self.game_service.to_json(self.game_id, self.game)

        self.assertEqual(response['gameId'], self.game_id)
        self.assertEqual(response['state'], 'IN_PROGESS')
        self.assertEqual(response['revealedWord'], '______')
        self.assertEqual(response['numFailedGuessesRemaining'], 5)
        self.assertEqual(response['score'], 5 * 10)

    def test_get_game(self):
        response = self.game_service.to_json(self.game_id, self.game)

        self.assertEqual(response['gameId'], self.game_id)
        self.assertEqual(response['state'], 'IN_PROGESS')
        self.assertEqual(response['revealedWord'], '______')
        self.assertEqual(response['numFailedGuessesRemaining'], 5)
        self.assertEqual(response['score'], 5 * 10)

    def test_guess_with_guessed_response(self):
        self.game.guesses.append("a")

        response = self.game.guess("a")

        self.assertEqual(response, {"value": GuessResult.FAIL_ALREADY_GUESSED.value,
                                    "error": GuessResult.FAIL_ALREADY_GUESSED.__str__()})

    def test_guess_with_guessed_letter_returns_already__invalid_body_returns_invalid_response(self):
        response = self.game.guess("as")

        self.assertEqual(response, {"value": GuessResult.FAIL_INVALID_INPUT.value,
                                    "error": GuessResult.FAIL_INVALID_INPUT.__str__()})

    def test_guess_with_correct_letter_returns_success_response(self):
        response = self.game.guess("3")

        self.assertEqual(response, {"value": GuessResult.CORRECT.value,
                                    "error": ""})

    def test_guess_with_incorrect_letter_returns_unsuccessful_response(self):
        game_id, game = self.game_service.create_game(words=["3dhubs"], guess_limit=5)

        response = game.guess("l")

        self.assertEqual(response, {"value": GuessResult.INCORRECT.value,
                                    "error": GuessResult.INCORRECT.__str__()})

    def test_guess_with_zero_guess_right_returns_game_over_result(self):
        self.game.num_failed_guesses_remaining = 0

        response = self.game.guess("3")

        self.assertEqual(response, {"value": GuessResult.FAIL_ALREADY_GAME_OVER.value,
                                    "error": GuessResult.FAIL_ALREADY_GAME_OVER.__str__()})
