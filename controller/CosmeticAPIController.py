import json
import logging
import sqlalchemy

from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required
from sqlalchemy import exc
from controller import app
from dao import ProductRepo, BrandRepo, CategoryRepo, ColorRepo, ProductTypeRepo, TagRepo
from dao.models import Product, Brand, Category, Color, ProductType, Tag


@app.route("/")
@jwt_required
def home():
    return app.send_static_file('index.html')


"""
API Call to get the product 
Input : product_id
"""


@app.route('/product/<int:product_id>', methods=['GET'])
@jwt_required
def get_product(product_id):
    try:
        logging.info(f'getProduct: User has given input product_id as: {product_id}')
        product = ProductRepo.getProduct(product_id)
        if product is None:
            return make_response(jsonify(response=f'Product with id {product_id} not found'), 404)
        return jsonify(product=Product.serialize(product))
    except exc.SQLAlchemyError as sqlexp:
        return make_response(jsonify(error_message=str(sqlexp)), 400)
    except Exception as excp:
        return make_response(jsonify(error_message=str(excp)), 400)


"""
API Call to search the product 
Input: 
        brand
        product_category
        product_type
        price : greater_than 
                less_than
        rating:greater_than
               less_than
        tag : String or list separated by commas
"""


@app.route('/searchproduct', methods=['GET'])
@jwt_required
def search_product():
    try:
        products = ProductRepo.get_all_products(filters=request.args)
        if len(products) > 0:
            return jsonify(products=Product.serialize_list(products))
        else:
            return make_response(jsonify(response='No Products available for the given search criteria'), 200)
    except exc.SQLAlchemyError as sqlexp:
        return make_response(jsonify(error_message=str(sqlexp)), 400)
    except Exception as excp:
        return make_response(jsonify(error_message=str(excp)), 400)


"""
Rest API : for add product
Input: Allows to pass the new product details as
                    request args or request body
"""


@app.route('/addproduct', methods=['POST'])
@jwt_required
def add_product():
    try:
        if len(request.args) == 0:
            product = request.json
        else:
            product = json.loads(json.dumps(request.args))
        if product is not None:
            product_id = ProductRepo.create_product(product)
        else:
            return make_response(jsonify(response=f'Request data is invalid.'), 400)
        return make_response(jsonify(response=f'Product added successfully and the product_id is {product_id} '), 201)
    except sqlalchemy.exc.InvalidRequestError as reqerr:
        return make_response(jsonify(error_message=str(reqerr)), 400)
    except exc.SQLAlchemyError as sqlexp:
        return make_response(jsonify(error_message=str(sqlexp)), 400)
    except Exception as excp:
        return make_response(jsonify(error_message=str(excp)), 400)


"""
Rest API : for update product
Input: product_id - Id of the product which is to be updated
       PATCH - Updates specific fields
       PUT   - Updates all the product data given in the request body
               Uses default values for empty fields
"""


@app.route('/updateproduct/<int:product_id>', methods=['PUT', 'PATCH'])
@jwt_required
def update_product(product_id):
    try:
        logging.info(f'updateProduct: User has given input product_id as: {product_id}')
        product = ProductRepo.getProduct(product_id)
        if product is not None:
            if request.method == 'PUT':
                ProductRepo.updateallfields(product_id, request.json)
            else:
                fields = request.json
                ProductRepo.update(product_id, fields)
            return jsonify(response=f'Updated product with id {product_id} successfully')
        else:
            return make_response(jsonify(response=f'Request data is invalid.'), 400)
    except sqlalchemy.exc.InvalidRequestError as error:
        return make_response(jsonify(error_message=str(error)), 400)
    except exc.SQLAlchemyError as sqlexp:
        return make_response(jsonify(error_message=str(sqlexp)), 400)
    except Exception as excp:
        return make_response(jsonify(error_message=str(excp)), 400)


"""
Rest API : for delete product
Input: product_id - If of the Product which is to be deleted
"""


@app.route('/delproduct/<int:product_id>', methods=['DELETE'])
@jwt_required
def delete_product(product_id):
    try:
        logging.info(f'deleteProduct:User has given input product_id as: {product_id}')
        product_result = ProductRepo.getProduct(product_id)
        if product_result is None:
            return make_response(jsonify(response=f'Product with id {product_id} not found'), 404)
        if request.method == 'DELETE':
            ProductRepo.delete(product_result)
        return jsonify(response=f'Product with id : {product_id} is deleted successfully')
    except sqlalchemy.exc.InvalidRequestError as error:
        return make_response(jsonify(error_message=str(error)), 400)
    except exc.SQLAlchemyError as sqlexp:
        return make_response(jsonify(error_message=str(sqlexp)), 400)
    except Exception as excp:
        return make_response(jsonify(error_message=str(excp)), 400)


"""
API Call to get the brand 
Input: brand_id 
Output: Returns the Brand details for the given brand_id
"""


@app.route('/brand/<int:brand_id>', methods=['GET'])
@jwt_required
def get_brand_by_id(brand_id):
    logging.info(f'getBrandById: User has given input brand_id as: {brand_id}')
    brand = BrandRepo.get(brand_id)
    if brand is None:
        return make_response(jsonify(response=f'Brand with id {brand_id} not found'), 404)
    return jsonify(brand=Brand.serialize(brand))


"""
API Call to get all brands 
"""


@app.route('/getallbrands', methods=['GET'])
@jwt_required
def get_all_brands():
    """
                @return: Returns the list of JSON Objects i.e product brands
    """
    brand = BrandRepo.get_all_brands()
    if brand is None or len(brand) == 0:
        return make_response(jsonify(response=f'No Brands Available'), 404)
    return jsonify(brands=Brand.serialize_list(brand))


"""
API Call to get all categories
  
"""


@app.route('/getallcategories', methods=['GET'])
@jwt_required
def get_all_categories():
    """
            @return: Returns the list of JSON Objects i.e product categories
    """
    categories = CategoryRepo.get_all_categories()
    if categories is None or len(categories) == 0:
        return make_response(jsonify(response=f'No Categories Available'), 404)
    return jsonify(categories=Category.serialize_list(categories))


"""
API Call to get all colors 
"""


@app.route('/getallcolors', methods=['GET'])
@jwt_required
def get_all_colors():
    """
        @return: Returns the list of JSON Object i.e product colors
    """
    colors = ColorRepo.get_all_colors()
    if colors is None or len(colors) == 0:
        return make_response(jsonify(response=f'No Colors Available'), 404)
    return jsonify(colors=Color.serialize_list(colors))


"""
API Call to get all product types 
"""


@app.route('/getallproducttypes', methods=['GET'])
@jwt_required
def get_all_producttypes():
    """
    @return: Returns the list of JSON Objects i.e product types
    """
    producttypes = ProductTypeRepo.get_all_producttypes()
    if producttypes is None or len(producttypes) == 0:
        return make_response(jsonify(response=f'No ProductTypes Available'), 404)
    return jsonify(product_types=ProductType.serialize_list(producttypes))


"""
API Call to get all product tags 
"""


@app.route("/getallproducttags", methods=['GET'])
@jwt_required
def get_all_tags():
    """
        @return: Returns the list of JSON objects i.e product tags
    """
    tags = TagRepo.get_all_tags()
    if tags is None or len(tags) == 0:
        return make_response(jsonify(response=f'No Tags Available'), 404)
    return jsonify(product_tags=Tag.serialize_list(tags))
