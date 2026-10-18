import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("ORDER_DATABASE_URI", "sqlite:///orders.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    product_name = db.Column(db.String(120), nullable=False)


with app.app_context():
    db.create_all()


@app.get("/health/live")
def health_live():
    return jsonify({"status": "ok"}), 200


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400
    username = data.get("user")
    product = data.get("product")
    if not isinstance(username, str) or not username.strip() or not isinstance(product, str) or not product.strip():
        return jsonify({"error": "user and product are required"}), 400
    order = Order(username=username.strip(), product_name=product.strip())
    try:
        db.session.add(order)
        db.session.commit()
    except Exception:
        db.session.rollback()
        app.logger.exception("Failed to persist order")
        return jsonify({"error": "Unable to create order"}), 500
    return jsonify({"status": "created", "order_id": order.id}), 201
