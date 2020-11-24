"""
Description: Models: Classes representing DB tables.
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from flask_bcrypt import generate_password_hash, check_password_hash

"""
Description: Setup the flask application.
"""

db = SQLAlchemy()


class Serializer(object):
    """Class for serializing SQLAlchemy objects into dicts."""

    @staticmethod
    def is_primitive(obj):
        return type(obj) in (int, float, str, bool)

    def serialize(self):
        fields = inspect(self).attrs.keys()
        return {c: getattr(self, c) for c in fields if Serializer.is_primitive(getattr(self, c))}

    @staticmethod
    def serialize_list(list_obj):
        return [m.serialize() for m in list_obj]


class Category(db.Model, Serializer):
    __tablename__ = 'Category'
    categoryid = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(120), nullable=False)
    products = db.relationship("Product", backref="Category", uselist=False)

    def __repr__(self):
        return f'Category Id: {self.categoryid}, Category name:{self.categoryname}'


class ProductType(db.Model, Serializer):
    __tablename__ = 'ProductType'
    typeid = db.Column(db.Integer, primary_key=True)
    typename = db.Column(db.String(120), nullable=False)
    products = db.relationship("Product", backref="ProductType", uselist=False)

    def __repr__(self):
        return f'Type Id: {self.typeid}, Type name:{self.typename}'


class Brand(db.Model, Serializer):
    __tablename__ = 'Brand'
    brandid = db.Column(db.Integer, primary_key=True)
    brandname = db.Column(db.String(120), nullable=False)
    products = db.relationship("Product", backref="Brand", uselist=False)

    def __repr__(self):
        return f'Brand Id : {self.brandid}, Brand name:{self.brandname}'


class Color(db.Model, Serializer):
    __tablename__ = 'Color'
    colorid = db.Column(db.Integer, primary_key=True)
    colorhexval = db.Column(db.String(120), nullable=False)
    colorname = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'Color Id: {self.colorid}, Color HexValue : {self.colorhexval}, Color name:{self.colorname}'


class Tag(db.Model, Serializer):
    __tablename__ = 'Tag'
    tagid = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'Tag Id: {self.tagid}, Tag name:{self.typename}'


producttags = db.Table('ProductTagMap',
                       db.Column('productid', db.Integer, db.ForeignKey('Product.productid')),
                       db.Column('tagid', db.Integer, db.ForeignKey('Tag.tagid')))

productcolors = db.Table('ProductColorMap',
                         db.Column('productid', db.Integer, db.ForeignKey('Product.productid')),
                         db.Column('colorid', db.Integer, db.ForeignKey('Color.colorid'))
                         )


class Product(db.Model, Serializer):
    __tablename__ = 'Product'
    productid = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String, nullable=False)
    price = db.Column(db.Float)
    productlink = db.Column(db.String)
    rating = db.Column(db.Float)
    description = db.Column(db.String)
    categoryid = db.Column(db.Integer, db.ForeignKey('Category.categoryid'))
    producttypeid = db.Column(db.Integer, db.ForeignKey('ProductType.typeid'))
    brandid = db.Column(db.Integer, db.ForeignKey('Brand.brandid'))
    category = db.relationship('Category')
    producttype = db.relationship('ProductType')
    brand = db.relationship('Brand')
    tags = db.relationship("Tag", secondary=producttags, backref=db.backref('products', lazy='joined'))
    colors = db.relationship('Color', secondary=productcolors, backref=db.backref('products', lazy='joined'))

    def __repr__(self):
        return f'Product Details: productid: {self.productid} productname: {self.productname}  price ={self.price} ' \
               f' description= {self.description}' \
               f' productlink = {self.productlink} rating= {self.rating}'

    def serialize(self):
        return {
            "productid": self.productid,
            "name": self.productname,
            "brandid": self.brandid,
            "brand": self.brand.brandname,
            "price": self.price,
            "product_link": self.productlink,
            "description": self.description,
            "rating": self.rating,
            "categoryid": self.categoryid,
            "category": self.category.categoryname,
            "producttypeid": self.producttypeid,
            "product_type": self.producttype.typename,
            "product_colors": [{'hex_value': color.colorhexval, 'colour_name': color.colorname} for color in
                               self.colors],
            "tag_list": [tag.tagname for tag in self.tags]}


class User(db.Model, Serializer):
    __tablename__ = 'User'
    email = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(200), nullable=False)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'email : {self.email}, password: {self.password}'

