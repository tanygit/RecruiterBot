
from flask import Flask

from .database import init_app as init_database


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        DATABASE="instance/recruiter_bot.sqlite3",
        TESTING=False,
    )

    if test_config:
        app.config.update(test_config)

    init_database(app)

    # Routes will be registered here after routes.py is created.
    from .routes import api
    app.register_blueprint(api)

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "service": "recruiter-bot"
        }

    return app
