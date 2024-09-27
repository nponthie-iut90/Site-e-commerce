from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors

import os                                 # à ajouter
from dotenv import load_dotenv            # à ajouter
load_dotenv()                             # à ajouter


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        #
        db = g._database = pymysql.connect(
            host=os.environ.get("HOST"),
            # host="serveurmysql", # à modifier
            user=os.environ.get("LOGIN"),  # à modifier
            password=os.environ.get("PASSWORD"),  # à modifier
            database=os.environ.get("DATABASE"),  # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return db
