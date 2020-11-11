from sqlalchemy import null

from controller import db
from dao.models import Product, Tag, Color, Brand, Category, ProductType


def handlenull(paramvalue):
    return None if paramvalue == null else paramvalue


def create_product(product):
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
    for color in product.get('product_colors'):
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
    for tag in product.get('tag_list'):
        if tag not in existing_tags_names:
            tag_entry = Tag(tagname=tag)
        else:
            tag_entry = Tag.query.filter_by(tagname=tag).first()
        tag_entries.append(tag_entry)
    prod.tags.extend(tag_entries)

    db.session.add(prod)
    db.session.commit()


def get_all_products():
    products = Product.query.all()
    return products


def get(prodid):
    return Product.query.filter_by(productid=prodid).first()


if __name__ == '__main__':
    data = [
        {"id": 641, "brand": "benefit", "name": "dallas dusty rose face powder", "price": "36.0", "price_sign": null,
         "currency": null,
         "image_link": "https://www.benefitcosmetics.com/ca/sites/ca/files/styles/category_page_lg/public/dallas-component2.png?itok=faVNQISZ",
         "product_link": "https://www.benefitcosmetics.com/ca/en-gb/product/dallas",
         "website_link": "https://www.benefitcosmetics.com",
         "description": "an outdoor glow for an indoor gal face powder", "rating": null, "category": null,
         "product_type": "bronzer", "tag_list": [], "created_at": "2016-10-02T11:37:26.889Z",
         "updated_at": "2017-12-23T20:42:44.364Z",
         "product_api_url": "https://makeup-api.herokuapp.com/api/v1/products/641.json",
         "api_featured_image": "//s3.amazonaws.com/donovanbailey/products/api_featured_images/000/000/641/original/open-uri20171223-4-1yca462?1514061764",
         "product_colors": [{"hex_value": "#CE9990", "colour_name": null}]}]
    for p in data:
        print(type(p))
        create_product(p)
