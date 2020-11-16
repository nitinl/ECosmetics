import json

from sqlalchemy import null

from dao.models import Product, Tag, Color, Brand, Category, ProductType, db


def handlenull(paramvalue):
    return None if paramvalue == null or paramvalue == "null" else paramvalue


def process_data(product):
    brandname = handlenull(product.get('brand'))
    b1 = Brand.query.filter_by(brandname=brandname).first()
    if (b1 is None) and (brandname is not None):
        b1 = Brand(brandname=brandname)

    categoryname = handlenull(product.get('category'))
    category_rec = Category.query.filter_by(categoryname=categoryname).first()
    if (category_rec is None) and (categoryname is not None):
        category_rec = Category(categoryname=categoryname)

    prodtypename = handlenull(product.get('product_type'))
    product_type_rec = ProductType.query.filter_by(typename=prodtypename).first()
    if (product_type_rec is None) and (prodtypename is not None):
        product_type_rec = ProductType(typename=product.get('product_type'))

    prod = Product(productname=product.get('name'), price=product.get('price'),
                   productlink=product.get('product_link'), rating=handlenull(product.get('rating')),
                   description=product.get('description'),
                   brand=b1, category=category_rec, producttype=product_type_rec)

    existing_colors = Color.query.all()
    existing_colors_names = [col.colorname for col in existing_colors]
    color_entries = []
    prodcolors = product.get('product_colors')
    if type(prodcolors) == str:  # if the input is given as request arguments
        prodcolors = json.loads(prodcolors)
    for color in prodcolors:

        if (color.get('colour_name') not in existing_colors_names) and (color.get('colour_name') is not None):
            color_entry = Color(colorhexval=color.get('hex_value'), colorname=color.get('colour_name'))
        else:
            color_entry = Color.query.filter_by(colorhexval=color.get('hex_value')).first()
        if color_entry is not None:
            color_entries.append(color_entry)
    prod.colors.extend(color_entries)

    existing_tags = Tag.query.all()
    existing_tags_names = [tag.tagname for tag in existing_tags]
    tag_entries = []
    prodtags = product.get('tag_list')
    if type(prodtags) == str:  # if the input is given as request arguments
        prodtags = json.loads(prodtags)
    for tag in prodtags:
        if tag not in existing_tags_names:
            tag_entry = Tag(tagname=tag)
        else:
            tag_entry = Tag.query.filter_by(tagname=tag).first()
        tag_entries.append(tag_entry)
    prod.tags.extend(tag_entries)
    return prod


def create_product(product):
    product = process_data(product)
    db.session.add(product)
    db.session.commit()


def get_all_products():
    products = Product.query.all()
    return products


def get(prodid):
    return Product.query.filter_by(productid=prodid).first()


def update(prodid, fields):
    result = Product.query.filter_by(productid=prodid).update(fields)
    db.session.commit()
    return result


def delete(product):
    db.session.delete(product)
    db.session.commit()


