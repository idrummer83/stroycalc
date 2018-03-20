from start import db

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