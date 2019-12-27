from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Gallery(Resource):
    def get(self):
        return {'Hello':'world'}

api.add_resource(Gallery, '/')

if __name__ == '__main__':
    app.run(debug=True)