from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from ..models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank'
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='Every item needs a store id'
    )

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f"Store with name {name} already exists."}, 400  # 400 - Bad request

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error occured while creating store."}, 500

        return store.json(), 201  # 201 - Created

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': f"Store with name {name} deleted."}, 200


class StoreList(Resource):
    def get(self):
       return {'items': [store.json() for store in StoreModel.query.all()]}
