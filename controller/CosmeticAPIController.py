import json
import logging

import sqlalchemy
from flask import request, jsonify, make_response

from controller import app
from dao import ProductRepo, BrandRepo
from dao.models import Product


@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route('/hello', methods=['GET'])
def hello():
    dat = jsonify(request.args).data
    name = request.get_json(force=True).get("name")
    # name = request.args.get('name') or 'Stranger'
    return {'dataString': 'Hello {name} from Flask!!'.format(name=name)}


@app.route('/product/<int:product_id>', methods=['GET'])
def getProduct(product_id):
    product = ProductRepo.get(product_id)
    # productid = request.args.get('product_id')
    print(type(product))
    if product is None:
        return make_response(jsonify(response=f'Product with id {product_id} not found'), 404)

    if request.method == 'GET':
        return jsonify(product=Product.serialize(product))


@app.route('/searchproduct', methods=['GET'])
def searchProduct():
    products = ProductRepo.get_all_products(filters=request.args)
    return jsonify(data=Product.serialize_list(products))


@app.route('/brand', methods=['GET'])
def getBrandById():
    brandid = request.args.get('brand_id')
    brand = BrandRepo.get(brandid)
    if brand is None:
        return make_response(jsonify(response=f'Brand with id {brandid} not found'), 404)

    if request.method == 'GET':
        return json.dumps(brand)


@app.route('/addproduct', methods=['POST'])
def addProduct():
    if len(request.args) == 0:
        product = request.json
    else:
        product = json.loads(json.dumps(request.args))
    if product is not None:
        ProductRepo.create_product(product)
    else:
        return make_response(jsonify(response=f'Request data is invalid.'), 400)

    return make_response(jsonify(response='OK'), 201)


@app.route('/updateproduct/<int:product_id>', methods=['PATCH', 'PUT'])
def updateProduct(product_id):
    try:
        product = ProductRepo.get(product_id)
        if product is not None:
            if request.method == 'PATCH':
                fields = request.json
            else:
                fields = {'productname': request.json.get('productname'),
                          'brand': {"brandname": request.json.get('brand')},
                          'price': request.json.get('price'),
                          'productlink': request.json.get('productlink'),
                          'description': request.json.get('description'),
                          'rating': request.json.get('rating'),
                          'category': {'categoryname': request.json.get('category')},
                          'producttype': {"typename": request.json.get('producttype')},
                          'colors': request.json.get('colors'),
                          'tags': request.json.get('tags')}
                # update with base table fields alone working fine
                # fields = {'productname': request.json.get('productname'),
                #           'price': request.json.get('price'),
                #           'productlink': request.json.get('productlink'),
                #           'description': request.json.get('description'),
                #           'rating': request.json.get('rating')}

            ProductRepo.update(product_id, fields)
            return jsonify(response='OK')
        else:
            return make_response(jsonify(response=f'Request data is invalid.'), 400)

    except (sqlalchemy.exc.InvalidRequestError, KeyError):
        return make_response(jsonify(error='Bad request'), 400)


@app.route('/delproduct', methods=['DELETE'])
def delProduct():
    product_id = request.args.get('product_id')
    logging.info(f'User has given input author_id as: {product_id}')
    productres = ProductRepo.get(product_id)
    if productres is None:
        return make_response(jsonify(response=f'Product with id {product_id} not found'), 404)

    if request.method == 'DELETE':
        ProductRepo.delete(productres)

    return jsonify(response='OK')
