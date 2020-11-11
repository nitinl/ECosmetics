import requests
import json
from flask import request, jsonify, make_response
from sqlalchemy import null

from controller import app
from dao import ProductRepo, BrandRepo
from dao.models import Product, Brand, ProductType, Category, Serializer
from service.CosmeticsService import CosmeticsService


@app.route('/getdatafromexternalapi', methods=['GET'])
def getcosmeticsdata_from_externalapi():
    params = {"brand": "covergirl"}
    response = requests.get(f"http://makeup-api.herokuapp.com/api/v1/products.json?", params=params)
    # response = requests.get(f"http://makeup-api.herokuapp.com/api/v1/products.json?")
    print(type(response.json()))
    data = response.json()

    if data != null and len(data) > 0:
        CosmeticsService.processcosmeticsdata(data)
    else:
        print("No data to process")
    return jsonify(data=Product.serialize_list(data))


@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route('/hello', methods=['GET'])
def hello():
    name = request.args.get('name') or 'Stranger'
    return {'dataString': 'Hello {name} from Flask!!'.format(name=name)}


@app.route('/product/<int:product_id>', methods=['GET'])
def getProduct(product_id):
    product = ProductRepo.get(product_id)
    print(type(product))
    if product is None:
        return make_response(jsonify(response=f'Product with id {product_id} not found'), 404)

    if request.method == 'GET':
        return product.__str__()


@app.route('/product', methods=['GET'])
def getProductById():
    productid = request.args.get('product_id')
    print(type(productid))
    product = Product.query.join(Brand, Product.brandid == Brand.brandid).join(ProductType,
                                                                               Product.producttypeid == ProductType.typeid).join(
        Category, Product.categoryid == Category.categoryid) \
        .filter(Product.productid == productid)
    if product is None:
        return make_response(jsonify(response=f'Product with id {productid} not found'), 404)

    if request.method == 'GET':
        return jsonify(Serializer.serialize_list(product))


@app.route('/brand', methods=['GET'])
def getBrandById():
    brandid = request.args.get('brand_id')
    brand = BrandRepo.get(brandid)
    if brand is None:
        return make_response(jsonify(response=f'Brand with id {brandid} not found'), 404)

    if request.method == 'GET':
        return json.dumps(brand)


if __name__ == "__main__":
    app.run()
