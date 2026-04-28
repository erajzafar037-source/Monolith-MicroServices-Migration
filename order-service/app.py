from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    product_name = db.Column(db.String(120))

with app.app_context():
    db.create_all()

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    new_order = Order(username=data['user'], product_name=data['product'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"status": "Order Created in Microservice!"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
