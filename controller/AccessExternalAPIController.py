import requests
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
from sqlalchemy import null, exc

from controller import app
from dao import ProductRepo

"""
Call to external API to fetch the data i.e Cosmetic Products and store in local DB 
"""


@app.route('/getdatafromexternalapi', methods=['GET'])
@jwt_required
def getcosmeticsdata_from_externalapi():
    try:
        # params = {"product_category": "lipstick", "product_type": "lipstick"}
        # response = requests.get(f"http://makeup-api.herokuapp.com/api/v1/products.json?", params=params)
        response = requests.get(f"http://makeup-api.herokuapp.com/api/v1/products.json")
        data = response.json()
        if data != null and len(data) > 0:
            for product in data:
                ProductRepo.create_product(product)
            return make_response(jsonify(response='Data Loaded Successfully'), 201)
        else:
            return make_response(jsonify(response=f'No data to process'), 400)
    except exc.SQLAlchemyError as sqlexp:
        return make_response(jsonify(error_message=str(sqlexp)), 400)
    except Exception as excp:
        return make_response(jsonify(error_message=str(excp)), 400)
