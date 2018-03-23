from start import db

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column('id', db.Integer, primary_key=True)
    name_category = db.Column('name_cat', db.String(50), unique=True)


class Item(db.Model):
    __tablename__= 'item'
    id = db.Column('id', db.Integer, primary_key=True)
    name_item = db.Column('name_item', db.String(200), unique=False)
    price_item = db.Column('price_item', db.Integer, unique=False)
    cat_id_choose = db.Column('cat_item', db.Integer, unique=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)