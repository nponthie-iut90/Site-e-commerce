#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                           template_folder='templates')


@client_article.route('/client/index')
@client_article.route('/client/article/show')  # remplace /client
def client_article_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # Construction de la requête SQL de base
    sql = '''SELECT * FROM ski'''

    # Liste des paramètres pour la requête SQL
    list_param = []
    condition_and = ""

    # Filtrage par mot-clé
    filter_word = session.get('filter_word')
    if filter_word:
        condition_and += " AND nom_ski LIKE %s"
        list_param.append(f"%{filter_word}%")

    # Filtrage par prix minimum
    filter_prix_min = session.get('filter_prix_min')
    if filter_prix_min:
        condition_and += " AND prix_ski >= %s"
        list_param.append(filter_prix_min)

    # Filtrage par prix maximum
    filter_prix_max = session.get('filter_prix_max')
    if filter_prix_max:
        condition_and += " AND prix_ski <= %s"
        list_param.append(filter_prix_max)

    # Filtrage par types d'articles
    filter_types = session.get('filter_types')
    if filter_types:
        condition_and += " AND type_ski_id IN %s"
        list_param.append(tuple(filter_types))

    # Intégration des conditions dans la requête SQL
    if condition_and:
        sql += " WHERE " + condition_and.lstrip(" AND")

    articles = []
    mycursor.execute(sql, tuple(list_param))
    articles = mycursor.fetchall()

    # Récupération des types d'articles pour affichage dans le filtre
    types_article = []
    sql = '''SELECT * FROM type_ski'''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    # Calcul du prix total du panier s'il existe
    articles_panier = []
    prix_total = None
    sql_panier = '''SELECT * FROM ligne_panier WHERE utilisateur_id = %s'''
    mycursor.execute(sql_panier, (id_client,))
    articles_panier = mycursor.fetchall()
    if len(articles_panier) >= 1:
        sql_prix_total = '''SELECT SUM(prix * quantite) AS prix_total FROM ligne_panier WHERE utilisateur_id = %s'''
        mycursor.execute(sql_prix_total, (id_client,))
        result = mycursor.fetchone()
        prix_total = result['prix_total']

    return render_template('client/boutique/panier_article.html',
                           articles=articles,
                           articles_panier=articles_panier,
                           prix_total=prix_total,
                           items_filtre=types_article)
