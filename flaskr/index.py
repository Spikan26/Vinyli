from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    db = get_db()
    produits = db.execute(
        'SELECT p.idProduit, p.titre, p.annee_sortie, p.prix, p.quantite, p.image, p.description'
        ' FROM Produit p '
    ).fetchall()
    return render_template('index.html', produits=produits)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        titre = request.form['titre']
        annee_sortie = request.form['annee_sortie']
        prix = request.form['prix']
        quantite = request.form['quantite']
        image = request.form['image']
        description = request.form['description']
        error = None

        if not titre:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO Produit (titre, annee_sortie, prix, quantite, image, description)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (titre, annee_sortie, prix, quantite, image, description)
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.idProduit, p.titre, p.annee_sortie, p.prix, p.quantite, p.image, p.description'
        ' FROM Produit p '
        ' WHERE p.idProduit = ?',
        (id,)
    ).fetchone()

    if produit is None:
        abort(404, "Le produit d'id {0} n'existe pas.".format(id))

    return post


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM Produit WHERE idProduit = ?', (id,))
    db.commit()
    return redirect(url_for('index'))
