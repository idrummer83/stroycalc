from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import relationship

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://calc:calc@localhost/calc'
db = SQLAlchemy(app)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column('id', db.Integer, primary_key=True)
    name_category = db.Column('name_cat', db.String(50), unique=True)
    # items = db.relationship('Item', backref='category', lazy=True,)


class Item(db.Model):
    __tablename__= 'item'
    id = db.Column('id', db.Integer, primary_key=True)
    name_item = db.Column('name_item', db.String(200), unique=False)
    price_item = db.Column('price_item', db.Integer, unique=False)
    cat_id = db.Column('cat_id', db.Integer)



@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/category', methods=['GET', 'POST'])
def create_category():
    cat = ''
    if request.method == 'POST':
        cat = request.form.get('cat', '')
        if cat:
            c = Category(name_category=cat)
            db.session.add(c)
            db.session.commit()
        return redirect('/category')
    return render_template('category.html',all_cat = Category.query.all())


@app.route('/item', methods=['GET', 'POST'])
def create_item():
    cat_id = item = price = ''
    if request.method == 'POST':
        cat = request.form.get('cat_id', '')
        item = request.form.get('item', '')
        price = request.form.get('price', '')
        if cat and item and price:
            c_item = Item(name_item=item,price_item=price,cat_id=cat)
            db.session.add(c_item)
            db.session.commit()
        return redirect('/item')
    return render_template('item.html', all_cat = Category.query.all(), all_item = Item.query.all())


@app.route('/calc', methods=['GET', 'POST'])
def calc_page():
    all_cat = Category.query.all()
    all_item = Item.query.all()
    l=[]
    if request.method == 'POST':
        all = request.form.getlist('price')

        for a in all:
            l.append(a.split('_'))

        from collections import Counter
        from itertools import chain
        z = []
        counts = Counter(chain.from_iterable(l))
        for s, x in counts.items():
            if 'id' in s:
                z.append([s, int(x)])
        w = []
        for i in z:
            k = 0
            for a in l[:i[1]:]:
                k += int(a[0])
                u = a[1]
            del l[:i[1]:]
            w.append([u, k])
        dct = dict((k[0], k[1]) for k in w)

        return render_template('calc.html', all_cat = all_cat, all_item = all_item, n = dct)

    return render_template('calc.html', all_cat = all_cat, all_item = all_item)

if __name__ == '__main__':
    app.debug = True
    app.run()