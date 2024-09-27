#! /usr/bin/python
# -*- coding:utf-8 -*-
from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                          template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite = int(request.form.get('quantite'))
    mycursor = get_db().cursor()
    # Récupérer le nom et le prix associés à l'id_ski
    sql = '''SELECT nom_ski, prix_ski, stock FROM ski WHERE id_ski = %s'''
    mycursor.execute(sql, (id_article,))
    article_info = mycursor.fetchone()
    nom_ski = article_info['nom_ski']
    prix_ski = article_info['prix_ski']
    stock_ski = article_info['stock']

    sql_check = '''SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND id_ski = %s'''
    mycursor.execute(sql_check, (id_client, id_article,))
    existing_item = mycursor.fetchone()

    if existing_item:
        # Si l'article est déjà dans le panier, mettre à jour la quantité
        new_quantite = existing_item['quantite'] + quantite
        sql = '''UPDATE ligne_panier SET quantite = %s WHERE utilisateur_id = %s AND id_ski = %s'''
        mycursor.execute(sql, (new_quantite, id_client, id_article,))
        sql2 = '''UPDATE ski SET stock = stock - %s WHERE id_ski = %s'''
        mycursor.execute(sql2, (quantite, id_article))
        get_db().commit()
    else:
        sql = '''INSERT INTO ligne_panier(utilisateur_id, id_ski, nom_ski, quantite, prix, date_ajout)
                 VALUES (%s, %s, %s, %s, %s, NOW())'''
        mycursor.execute(sql, (id_client, id_article, nom_ski, quantite, prix_ski))
        sql2 = '''UPDATE ski SET stock = stock - %s WHERE id_ski = %s'''
        mycursor.execute(sql2, (quantite, id_article))
        get_db().commit()

    # ---------
    #id_declinaison_article=request.form.get('id_declinaison_article',None)
    id_declinaison_article = 1

# ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_article))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_article = declinaisons[0]['id_declinaison_article']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_article))
    #     article = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_article.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , article=article)

# ajout dans le panier d'un article

    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article',)
    # quantite = 1
    sql = '''SELECT * FROM ligne_panier WHERE id_ski = %s AND utilisateur_id = %s'''
    mycursor.execute(sql, (id_article, id_client,))
    ski_info = mycursor.fetchone()
    quantite = ski_info['quantite']
    new_quantite = quantite - 1
    if new_quantite > 0:
        sql = '''UPDATE ligne_panier SET quantite = %s WHERE id_ski = %s AND utilisateur_id = %s'''
        mycursor.execute(sql, (new_quantite, id_article, id_client,))
        sql2 = '''UPDATE ski SET stock = stock + 1 WHERE id_ski = %s'''
        mycursor.execute(sql2, (id_article,))
        get_db().commit()
    else:
        sql = '''DELETE FROM ligne_panier WHERE id_ski = %s AND utilisateur_id = %s'''
        mycursor.execute(sql, (id_article, id_client,))
        sql2 = '''UPDATE ski SET stock = stock + 1 WHERE id_ski = %s'''
        mycursor.execute(sql2, (id_article,))
        get_db().commit()


    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    # id_declinaison_article = request.form.get('id_declinaison_article', None)

    # sql = ''' selection de la ligne du panier pour l'article et l'utilisateur connecté'''
    article_panier = []

    # if not (article_panier is None) and article_panier['quantite'] > 1:
    #     sql = ''' mise à jour de la quantité dans le panier => -1 article '''
    # else:
    #     sql = ''' suppression de la ligne de panier'''

    # mise à jour du stock de l'article disponible
    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = '''SELECT * FROM ligne_panier WHERE utilisateur_id = %s'''
    mycursor.execute(sql, (client_id,))
    items_panier = []
    items_panier = mycursor.fetchall()

    for item in items_panier:
        quantite_article = item['quantite']

        # Mettre à jour le stock de l'article dans la table des articles
        sql_update_stock = '''UPDATE ski SET stock = stock + %s WHERE id_ski = %s'''
        mycursor.execute(sql_update_stock, (quantite_article, item['id_ski']))

        sql_delete = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND id_ski = %s'''
        mycursor.execute(sql_delete, (client_id, item['id_ski']))
        # sql2 = ''' mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article'''
        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article',)
    # id_declinaison_article = request.form.get('id_declinaison_article')
    mycursor = get_db().cursor()
    sql = '''SELECT quantite FROM ligne_panier WHERE utilisateur_id = %s AND id_ski = %s'''
    mycursor.execute(sql, (id_client, id_article))
    result = mycursor.fetchone()
    quantite = result['quantite']
    print(quantite)
    sql2 = '''DELETE FROM ligne_panier
    WHERE (utilisateur_id = %s AND id_ski = %s)'''
    mycursor.execute(sql2, (id_client, id_article))
    sql3 = '''UPDATE ski SET stock = stock + %s WHERE id_ski = %s'''
    mycursor.execute(sql3, (quantite, id_article,))
    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    # test des variables puis
    # mise en session des variables
    session['filter_word'] = filter_word
    session['filter_prix_min'] = filter_prix_min
    session['filter_prix_max'] = filter_prix_max
    session['filter_types'] = filter_types
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/article/show')
