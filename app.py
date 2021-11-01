from flask import Flask
from controllers.hangman_controller import hangman_controller

app = Flask(__name__)
app.register_blueprint(hangman_controller)

if __name__ == '__main__':
    app.run()
