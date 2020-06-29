import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        mdp = request.form['mdp']
        nom = request.form['nom']
        prenom = request.form['prenom']
        db = get_db()
        error = None

        if not email:
            error = 'Email requis.'
        elif not mdp:
            error = 'Mot de passe requis.'
        elif db.execute(
            'SELECT idClient FROM Client WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = 'Email {} déjà renseigné.'.format(email)

        if error is None:
            db.execute(
                'INSERT INTO Client (email, mdp, nom, prenom) VALUES (?, ?, ?, ?)',
                (email, generate_password_hash(mdp), nom, prenom)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        mdp = request.form['mdp']
        db = get_db()
        error = None
        client = db.execute(
            'SELECT * FROM Client WHERE email = ?', (email,)
        ).fetchone()

        if client is None:
            error = 'Email incorrect.'
        elif not check_password_hash(client['mdp'], mdp):
            error = 'Mot de passe incorrect.'

        if error is None:
            session.clear()
            session['user_id'] = client['idClient']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM Client WHERE idClient = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

