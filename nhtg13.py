#!/usr/bin/env python2

from flask import Flask, session, redirect, url_for, escape, request, render_template, send_from_directory

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://nhtg13:sq8NyLaAmuANVeR6@localhost/nhtg13'
app.config['WHOOSH_BASE'] = '/home/samuel/code/NHTG13/search.db'
app.secret_key = '<%\xd9\xfb\xbc )\xf6\xb1\xb9~:{g\x04Cp\xf7X\xca\xf5\xc0)\xee'

from database import *

@app.route('/')
def index():
    categories = BNFCategory.query.filter(BNFCategory.parent_id==None).order_by(BNFCategory.name).all()

    return render_template('index.html', categories=categories)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/search/')
def search():
    try:
        term = request.args['query']
    except KeyError:
        flash('Please enter a search term', 'error')
        return redirect(url_for('index'))

    drugs = BNFDrug.query.whoosh_search(term).all()
    categories = BNFCategory.query.whoosh_search(term).all()
    chemicals = BNFChemical.query.whoosh_search(term).all()

    return render_template('searchresults.html',
                           categories=categories,
                           drugs=drugs,
                           chemicals=chemicals)

@app.route('/category/<int:id>')
def category(id):
    pass
