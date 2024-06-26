from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import os

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/RESTFUL'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init db
db = SQLAlchemy(app)
#Init marshmallow (ma)
ma = Marshmallow(app)

#Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

#product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

#Init schema
product_schema = ProductSchema ()
products_schema = ProductSchema (many=True)

@app.route('/product', methods= ['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name,description,price,qty)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

#Get All Products
@app.route('/product', methods = ['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)



#@app.route("/")
#def create_tables():
#    with app.app_context():
#        db.create_all()
#    return "Tables created!"

#Run server
if __name__ == '__main__':
    app.run(debug=True)
