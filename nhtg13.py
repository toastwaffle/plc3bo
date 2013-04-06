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

@app.route('/search/')
def search():
    try:
        term = request.args['query']
    except KeyError:
        flash('Please enter a search term', 'error')
        return redirect(url_for('index'))

    categories = BNFCategory.query.whoosh_search(term).all()
    chemicals = BNFChemical.query.whoosh_search(term).all()
    drugs = BNFDrug.query.whoosh_search(term).all()

    return render_template('searchresults.html',
                           categories=categories,
                           drugs=drugs,
                           chemicals=chemicals,
                           term=term)

@app.route('/category/<int:id>')
def category(id):
    category = BNFCategory.query.filter(BNFCategory.id==id).first()

    if not category:
        flash('Category not found', 'error')
        return redirect(url_for('index'))

    children = category.children.order_by(BNFCategory.name).all()
    drugs = category.drugs.order_by(BNFDrug.name).all()

    return render_template('category.html', category=category, children=children, drugs=drugs)


@app.route('/drug/<int:id>')
def drug(id):
    pass

@app.route('/chemical/<int:id>')
def chemical(id):
    chemical = BNFChemical.query.filter(BNFChemical.id==id).first()

    if not chemical:
        flash('Category not found', 'error')
        return redirect(url_for('index'))

    drugs = chemical.drugs.order_by(BNFDrug.name).all()

    return render_template('chemical.html', chemical=chemical, drugs=drugs)

@app.context_processor
def utility_processor():
    def get_all(query):
        return query.all()
    return dict(get_all=get_all)


if __name__ == '__main__':
    app.run(debug=True)
