import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("MONOLITH_DATABASE_URI", "sqlite:///monolith.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Monolith(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    order_status = db.Column(db.String(20), nullable=False, default="Pending")


with app.app_context():
    db.create_all()


@app.get("/health/live")
def health_live():
    return jsonify({"status": "ok"}), 200


@app.route("/process", methods=["POST"])
def process_everything():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400
    username = data.get("user")
    product = data.get("product")
    if not isinstance(username, str) or not username.strip() or not isinstance(product, str) or not product.strip():
        return jsonify({"error": "user and product are required"}), 400
    entry = Monolith(username=username.strip(), product_name=product.strip(), order_status="Pending")
    try:
        db.session.add(entry)
        db.session.commit()
    except Exception:
        db.session.rollback()
        app.logger.exception("Failed to persist order in monolith")
        return jsonify({"error": "Unable to process order"}), 500
    return jsonify({"message": "Order accepted by monolith", "order_id": entry.id, "status": entry.order_status}), 201
