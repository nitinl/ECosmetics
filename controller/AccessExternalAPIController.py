import requests
from flask import jsonify, make_response
from sqlalchemy import null

from controller import app
from service.CosmeticsService import CosmeticsService


@app.route('/getdatafromexternalapi', methods=['GET'])
def getcosmeticsdata_from_externalapi():
    params = {"product_category":"lipstick","product_type":"lipstick"}
    response = requests.get(f"http://makeup-api.herokuapp.com/api/v1/products.json?", params=params)
    # response = requests.get(f"http://makeup-api.herokuapp.com/api/v1/products.json?")
    print(type(response.json()))
    data = response.json()

    if data != null and len(data) > 0:
        CosmeticsService.processcosmeticsdata(data)
    else:
        print("No data to process")
        return make_response(jsonify(response=f'No data to process'), 400)

    # return jsonify(data=Product.serialize_list(data))

    return make_response(jsonify(response='OK'), 201)


