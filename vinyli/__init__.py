import os

from flask import Flask


def create_app(test_config=None):
    # Configuration de l'application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "vinyli.sqlite"),
    )

    if test_config is None:
        # Configure l'application a partir du fichier config.py lorsque l'application n'est pas en mode dev
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Configure l'application avec les configuration par defaut de test
        app.config.from_mapping(test_config)

    # Verifie si le dossier de l'instance existe
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # import du fichier db.py
    from . import db

    db.init_app(app)

    # import du fichier auth.py
    from . import auth

    app.register_blueprint(auth.bp)

    # import du fichier index.py
    from . import index

    app.register_blueprint(index.bp)
    app.add_url_rule("/", endpoint="index")

    return app
