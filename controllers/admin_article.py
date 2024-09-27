#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
# from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')


@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = '''  
    SELECT * FROM ski
    '''
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    return render_template('admin/article/show_article.html', articles=articles)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()
    sql = '''
    SELECT * FROM type_ski
    '''
    mycursor.execute(sql)
    type_article = mycursor.fetchall()
    return render_template('admin/article/add_article.html'
                           , types_article=type_article
                           # ,couleurs=colors
                           # ,tailles=tailles
                           )


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()

    nom_ski = request.form.get('nom', '')
    type_ski_id = request.form.get('type_article_id', '')
    largeur = request.form.get('largeur', '')
    prix_ski = request.form.get('prix', '')
    fournisseur = request.form.get('fournisseur', '')
    marque = request.form.get('marque', '')
    conseil_utilisation = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload' + str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename = None

    tuple_test = (nom_ski, type_ski_id, largeur, prix_ski, fournisseur, marque, conseil_utilisation, filename)

    sql = '''
    INSERT INTO ski (nom_ski, type_ski_id, largeur, prix_ski, fournisseur, marque, conseil_utilisation, image)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''

    tuple_add = (nom_ski, filename, prix_ski, type_ski_id, conseil_utilisation)
    print(tuple_add)
    mycursor.execute(sql, tuple_test)
    get_db().commit()

    print(u'article ajouté , nom: ', nom_ski, ' - type_article:', type_ski_id, ' - prix:', prix_ski,
          ' - description:', conseil_utilisation, ' - image:', image)
    message = u'article ajouté , nom:' + nom_ski + '- type_article:' + type_ski_id + ' - prix:' + prix_ski + ' - description:' + conseil_utilisation + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    id_article = request.args.get('id_article')
    print(id_article)
    mycursor = get_db().cursor()
    # sql = ''' SELECT nb_declinaison
    # FROM ski
    # WHERE id_ski = %s'''
    # mycursor.execute(sql, id_article)
    # nb_declinaison = mycursor.fetchone()
    # print(nb_declinaison)
    # if nb_declinaison['nb_declinaison'] > 0:
    #     message = u'il y a des declinaisons dans cet article : vous ne pouvez pas le supprimer'
    #     flash(message, 'alert-warning')
    # else:
    sql = '''
        SELECT *
        FROM ski
        WHERE id_ski = %s
    '''
    mycursor.execute(sql, id_article)
    article = mycursor.fetchone()
    print(article)
    image = article['image']
    print(image)
    sql = '''
            DELETE FROM ski
            WHERE id_ski = %s
            '''
    mycursor.execute(sql, id_article)
    get_db().commit()
    if image != None:
        os.remove('static/images/' + image)

    print("un article supprimé, id :", id_article)
    message = u'un article supprimé, id : ' + id_article
    flash(message, 'alert-success')

    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET'])
def edit_article():
    id_article = request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = '''
        SELECT *
        FROM ski
        WHERE id_ski = %s;
    '''
    tuple_id = (id_article,)
    mycursor.execute(sql, tuple_id)
    article = mycursor.fetchone()
    print(article)
    sql = '''
        SELECT *
        FROM type_ski
    '''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    # sql = '''
    # requête admin_article_6
    # '''
    # mycursor.execute(sql, id_article)
    # declinaisons_article = mycursor.fetchall()

    return render_template('admin/article/edit_article.html'
                           , article=article
                           , types_article=types_article
                           #  ,declinaisons_article=declinaisons_article
                           )


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    nom = request.form.get('nom', '')
    id_article = request.form.get('id_article', '')
    largeur = request.form.get('largeur', '')
    image = request.files.get('image', '')
    type_article_id = request.form.get('type_article_id', '')
    prix = request.form.get('prix', '')
    fournisseur = request.form.get('fournisseur', '')
    marque = request.form.get('marque', '')
    description = request.form.get('conseil_utilisation', '')
    stock = request.form.get('stock', '')
    print("test", id_article)
    sql = '''
       SELECT image
       FROM ski
       WHERE id_ski = %s;
       '''
    mycursor.execute(sql, id_article)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    print(image_nom)
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename

    sql = '''
    UPDATE ski
    SET nom_ski = %s, largeur = %s, prix_ski = %s, type_ski_id = %s, fournisseur = %s, marque = %s,
    conseil_utilisation = %s, image = %s, stock = %s
    WHERE id_ski = %s
    '''
    mycursor.execute(sql, (nom, largeur, prix, type_article_id, fournisseur, marque, description, image_nom, stock,
                           id_article,))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'article modifié , nom:' + nom + '- type_article :' + type_article_id + ' - prix:' + prix + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    article = []
    commentaires = {}
    return render_template('admin/article/show_avis.html'
                           , article=article
                           , commentaires=commentaires
                           )


@admin_article.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    return admin_avis(article_id)
