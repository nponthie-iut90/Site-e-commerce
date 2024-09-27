#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = '''
        SELECT commande.*, utilisateur.login, etat.libelle
        FROM commande
        JOIN utilisateur ON commande.utilisateur_id = utilisateur.id_utilisateur
        JOIN etat ON commande.etat_id = etat.id_etat
    '''
    mycursor.execute(sql)
    commandes = []
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    print(id_commande)
    if id_commande is not None:
        print(id_commande)
        sql = '''SELECT * , (quantite * prix) AS prix_ligne FROM ligne_commande WHERE commande_id = %s'''
        mycursor.execute(sql, (id_commande,))
        articles_commande = mycursor.fetchall()

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql_commande_adresses = '''
        SELECT 
        *,
        a1.nom AS nom_livraison, 
        a1.rue AS rue_livraison, 
        a1.code_postal AS code_postal_livraison, 
        a1.ville AS ville_livraison, 
        a2.nom AS nom_facturation, 
        a2.rue AS rue_facturation, 
        a2.code_postal AS code_postal_facturation, 
        a2.ville AS ville_facturation
    FROM 
        commande
    LEFT JOIN 
        adresse a1 ON commande.adresse = a1.id_adresse
    LEFT JOIN 
        adresse a2 ON commande.adresse_1 = a2.id_adresse
    WHERE 
        commande.id_commande = %s 
        '''
        mycursor.execute(sql_commande_adresses, (id_commande,))
        commande_adresses = mycursor.fetchone()
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = '''UPDATE commande SET etat_id = 2 WHERE id_commande = %s'''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')
