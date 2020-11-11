from flask import request
from controller import app


@app.route('/hello1', methods=['GET'])
def hello():
    name = request.args.get('name') or 'Stranger'
    return {'dataString': 'Hello {name} from Flask!!'.format(name=name)}
