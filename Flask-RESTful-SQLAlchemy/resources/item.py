import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank'
    )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('../code/data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('../code/data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('../code/data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?;"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    def post(self, name):
        if self.find_by_name(name):
            return {'message': f"Item with name {name} already exists."}, 400  # 400 - Bad request

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price'], }

        try:
            self.insert(item)
        except:
            return {"message": "An error occured while inserting item."}, 500

        return item, 201  # 201 - Created

    def delete(self, name):
        connection = sqlite3.connect('../code/data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?;"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': f"Item with name {name} deleted."}, 200

    def put(self, name):
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            self.insert(updated_item)
        else:
            self.update(updated_item)
        return {'message': f"Item with name {name} updated to {data['price']}."}, 200


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('../code/data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.commit()
        connection.close()

        return {'items': items}
