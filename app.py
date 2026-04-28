from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monolith.db'
db = SQLAlchemy(app)

# THE TANGLED DATABASE MODEL
class Monolith(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # User info
    username = db.Column(db.String(80))
    # Product info
    product_name = db.Column(db.String(120))
    # Order info
    order_status = db.Column(db.String(20))

with app.app_context():
    db.create_all()

@app.route('/process', methods=['POST'])
def process_everything():
    data = request.json
    # Garbage Logic: Everything is mixed in one function
    new_entry = Monolith(
        username=data['user'], 
        product_name=data['product'], 
        order_status='Pending'
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Order processed in the messy monolith!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
