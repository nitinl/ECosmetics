import json
import logging

import null
import sqlalchemy
from flask import request, jsonify, make_response

from controller import app
from dao import ProductRepo, BrandRepo, TagRepo
from dao.models import Product, Tag, db


@app.route("/")
def index():
    return app.send_static_file('index.html')


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
    if len(products) > 0:
        return jsonify(products=Product.serialize_list(products))
    else:
        return make_response(jsonify(response='No Products available for the given search criteria'), 200)


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


@app.route('/updateproduct/<int:product_id>', methods=['PUT'])
def updateProduct(product_id):
    try:
        product = ProductRepo.get(product_id)
        if product is not None:
            ProductRepo.updateallfields(product_id, request.json)
            return jsonify(response='OK')
        else:
            return make_response(jsonify(response=f'Request data is invalid.'), 400)

    except (sqlalchemy.exc.InvalidRequestError, KeyError):
        return make_response(jsonify(error='Bad request'), 400)


@app.route('/updateproduct/<int:product_id>', methods=['PATCH'])
def updateProduct_all_values(product_id):
    try:
        product = ProductRepo.get(product_id)
        if product is not None:
            fields = request.json
            ProductRepo.update(product_id, fields)
            return jsonify(response='OK')
        else:
            return make_response(jsonify(response=f'Request data is invalid.'), 400)

    except (sqlalchemy.exc.InvalidRequestError, KeyError):
        return make_response(jsonify(error='Bad request'), 400)


@app.route('/delproduct', methods=['DELETE'])
def delProduct():
    try:
        product_id = request.args.get('product_id')
        logging.info(f'User has given input author_id as: {product_id}')
        product_result = ProductRepo.get(product_id)
        if product_result is None:
            return make_response(jsonify(response=f'Product with id {product_id} not found'), 404)
        if request.method == 'DELETE':
            ProductRepo.delete(product_result)
        return jsonify(response='OK')

    except (sqlalchemy.exc.InvalidRequestError, KeyError):
        return make_response(jsonify(error='Bad request'), 400)