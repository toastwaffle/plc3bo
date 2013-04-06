#!/usr/bin/env python2

import csv
import re
from database import *

lastsectionstr = ''
lastsection = None
lastchemicalstr = ''
lastchemical = None

def get_section(name, parentname=None):
    section = BNFCategory.query.filter(BNFCategory.lowercasename==name.lower()).first()

    if not section:
        if parentname is not None:
            parent = BNFCategory.query.filter(BNFCategory.lowercasename==parentname.lower()).first()

            if not parent:
                parent = BNFCategory(parentname)
                db.session.add(parent)
        else:
            parent = None

        section = BNFCategory(name, parent)
        db.session.add(section)
        db.session.commit()

    return section


def get_chemical(name):
    if name == '':
        return None

    chemical = BNFChemical.query.filter(BNFChemical.lowercasename==name.lower()).first()

    if not chemical:
        chemical = BNFChemical(name)
        db.session.add(chemical)
        db.session.commit()

    return chemical

def get_drug(row):
    global lastsectionstr, lastsection, lastchemicalstr, lastchemical
    drug = BNFDrug.query.filter(BNFDrug.lowercasename==row[0].lower()).first()

    if not drug:
        if lastsectionstr != (row[7] + '||' + row[4]):
            lastsection = get_section(row[7], row[4])
            lastsectionstr = row[7] + '||' + row[4]

        section = lastsection

        if lastchemicalstr != row[1]:
            lastchemical = get_chemical(row[1])
            lastchemicalstr = row[1]

        chemical = lastchemical

        lower = row[0].lower()

        form = 'Unknown'
        if 'cap' in lower:
            form = 'Caplet'
        elif 'tab' in lower:
            form = 'Tablet'
        elif 'susp' in lower:
            form = 'Suspension'
        elif 'liq' in lower:
            form = 'Liquid'
        elif 'soln' in lower:
            form = 'Solution'

        if 'chble' in lower:
            form = 'Chewable ' + form

        match = match = re.search(r'[\d\.]+(mg|g|ml)(/[\d\.]+(mg|g|ml))*', row[0])
        if match:
            dosage = match.group(0)
        else:
            dosage = 'Unknown'

        qty_units = {'1' : 'unit', '3' : 'millilitre', '6' : 'gram', '0' : 'other'}

        qty_unit = qty_units[row[8]]

        prep_class = row[9]

        drug = BNFDrug(row[0],
                       chemical,
                       section,
                       form,
                       dosage,
                       qty_unit,
                       prep_class)

        db.session.add(drug)
        db.session.commit()

    return drug

for year in [2012,2009,2010,2011]:
    filename = 'pres-cost-anal-eng-' + str(year) + '-data.csv'
    csvfile = open(filename, 'r')
    for row in csv.reader(csvfile):
        drug = get_drug(row)

        items = int(float(row[10].replace(',',''))*1000)
        quantity = int(float(row[11].replace(',',''))*1000)
        owc2 = int(float(row[12].replace(',',''))*1000)
        nic = int(float(row[13].replace(',',''))*1000)

        stat = Statistic(drug,
                         year,
                         items,
                         quantity,
                         owc2,
                         nic)

        db.session.add(stat)

        db.session.commit()
