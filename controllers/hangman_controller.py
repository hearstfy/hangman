from flask import Blueprint, request

from services.game_service import GameService

hangman_controller = Blueprint('hangman_controller', __name__, url_prefix='/api')
game_service = GameService()


@hangman_controller.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@hangman_controller.route('/hangman', methods=['POST'])
def create_game():
    game_id, game = game_service.create_game()
    return game_service.to_json(game_id, game)


@hangman_controller.route('/hangman/<int:game_id>', methods=['GET'])
def get_hangman(game_id):
    game = game_service.get_game(game_id)

    if game is None:
        return {'error': 'Game not found'}, 404

    return game_service.to_json(game_id, game), 200


@hangman_controller.route('/hangman/<int:game_id>/guess', methods=['POST'])
def guess(game_id):
    game = game_service.get_game(game_id)
    letter = request.json.get("letter")
    return game.guess(letter)
