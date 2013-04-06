"""
database.py

Contains classes for database table objects
"""

from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.whooshalchemy as whooshalchemy
from nhtg13 import app

db = SQLAlchemy(app)


class BNFCategory(db.Model):
    __tablename__ = 'bnf_category'
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    lowercasename = db.Column(db.String(255), primary_key=True)

    parent_id = db.Column(db.Integer, db.ForeignKey('bnf_category.id'))
    parent = db.relationship('BNFCategory',
                             remote_side=[id],
                             backref=db.backref('children',
                                                lazy='dynamic',
                                                order_by=name
                                                )
                             )

    def __init__(self, name, parent=None):
        self.name = name
        self.lowercasename = name.lower()

        if isinstance(parent, BNFCategory):
            self.parent = parent
        else:
            self.parent_id = parent

    def __repr__(self):
        return "<BNFCategory %s>" % self.name


class BNFChemical(db.Model):
    __tablename__ = 'bnf_chemical'
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    lowercasename = db.Column(db.String(255), primary_key=True)

    def __init__(self, name):
        self.name = name
        self.lowercasename = name.lower()

    def __repr__(self):
        return "<BNFChemical %s>" % self.name


class BNFDrug(db.Model):
    __tablename__ = 'bnf_drug'
    __searchable__ = ['name']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    lowercasename = db.Column(db.String(255), primary_key=True)

    form = db.Column(db.String(50))
    dosage = db.Column(db.String(50))
    qty_unit = db.Column(db.Enum('unit', 'millilitre', 'gram', 'other'))
    prep_class = db.Column(db.Integer)

    chemical_id = db.Column(db.Integer, db.ForeignKey('bnf_chemical.id'))
    chemical = db.relationship('BNFChemical',
                               backref=db.backref('drugs',
                                                  lazy='dynamic'
                                                  )
                               )

    category_id = db.Column(db.Integer, db.ForeignKey('bnf_category.id'))
    category = db.relationship('BNFCategory',
                               backref=db.backref('drugs',
                                                  lazy='dynamic'
                                                  )
                               )

    def __init__(self,
                 name,
                 chemical,
                 category,
                 form=None,
                 dosage=None,
                 qty_unit=None,
                 prep_class=None):
        self.name = name
        self.lowercasename = name.lower()
        self.form = form
        self.dosage = dosage
        self.qty_unit = qty_unit
        self.prep_class = prep_class

        if isinstance(category, BNFCategory):
            self.category = category
        else:
            self.category_id = category

        if isinstance(chemical, BNFChemical):
            self.chemical = chemical
        else:
            self.chemical_id = chemical


class Statistic(db.Model):
    __tablename__ = 'statistic'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)

    drug_id = db.Column(db.Integer, db.ForeignKey('bnf_drug.id'))
    drug = db.relationship('BNFDrug',
                               backref=db.backref('statistics',
                                                  lazy='dynamic'
                                                  )
                               )

    items = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    owc2 = db.Column(db.Integer)
    nic = db.Column(db.Integer)

    def __init__(self,
                 drug,
                 year,
                 items=None,
                 quantity=None,
                 owc2=None,
                 nic=None):
        self.items = items
        self.quantity = quantity
        self.owc2 = owc2
        self.nic = nic
        self.year = year

        if isinstance(drug, BNFDrug):
            self.drug = drug
        else:
            self.drug_id = drug

    def __repr__(self):
        return "<BNFStatistic %s>" % self.id

    def todict(self):
        return {"items": self.items,
                "quantity": self.quantity,
                "owc2": self.owc2,
                "nic": self.nic,
                "year": str(self.year),
                "costp": float(self.nic) / float(self.items),
                "costi": float(self.nic) / float(self.quantity),
                "iperp": float(self.quantity) / float(self.items)}


whooshalchemy.whoosh_index(app, BNFDrug)
whooshalchemy.whoosh_index(app, BNFCategory)
whooshalchemy.whoosh_index(app, BNFChemical)
