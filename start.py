from flask import Flask, render_template, request, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://calc:calc@localhost/calc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

from collections import Counter
from itertools import chain
from models.models import *

@app.route('/')
def welcome():
    return render_template('menu.html')


@app.route('/category', methods=['GET', 'POST'])
def create_category():
    cat = ''
    if request.method == 'POST':
        cat = request.form.get('cat', '')
        if cat:
            category = Category(name_category=cat)
            db.session.add(category)
            db.session.commit()
        return redirect('/category')
    return render_template('category.html',all_cat = Category.query.all())


@app.route('/item', methods=['GET', 'POST'])
def create_item():
    cat_id = item = price = ''
    if request.method == 'POST':
        cat_id = request.form.get('id_select', '')
        item = request.form.get('item', '')
        price = request.form.get('price', '')
        if item and price:
            category_item = Item(name_item=item,price_item=price,category_id=cat_id)
            db.session.add(category_item)
            db.session.commit()
        return redirect('/item')
    return render_template('item.html', all_cat = Category.query.all(), all_item = Item.query.all())


@app.route('/calc', methods=['GET', 'POST'])
def calc_page():
    all_cat = Category.query.all()
    all_item = Item.query.all()
    list_all_checked=[]
    if request.method == 'POST':
        all_checked = request.form.getlist('price')

        # creating all checked inputs's
        for a in all_checked:
            list_all_checked.append(a.split('_'))

        # creating list of id's and price
        list_id_counter = []
        counts = Counter(chain.from_iterable(list_all_checked))
        for s, x in counts.items():
            if 'id' in s:
                list_id_counter.append([s, int(x)])

        # calculating dict with id and calculated price
        list_calculate = []
        for i in list_id_counter:
            k = 0
            for a in list_all_checked[:i[1]:]:
                k += int(a[0])
                u = a[1]
            del list_all_checked[:i[1]:]
            list_calculate.append([u, k])
        dict_list_calculate = [dict((k[0], k[1]) for k in list_calculate)]

        # calculating full price
        f=0
        for fp in list_calculate:
            f += fp[1]

        return render_template('calc.html', all_cat = all_cat, all_item = all_item, dct=dict_list_calculate, full = f)

    return render_template('calc.html', all_cat = all_cat, all_item = all_item)

if __name__ == '__main__':
    app.debug = True
    app.run()