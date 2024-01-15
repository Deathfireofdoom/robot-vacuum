from flask import Flask
from src.api import api_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(
        api_blueprint, url_prefix=""
    )  # NOTE: adding it to prefix '' and not '/api' according to instructions.

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
