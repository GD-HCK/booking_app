# app.py
from classes.product import *
from flask import Blueprint, request, jsonify, render_template
app = Blueprint('product', __name__)

# prefix = "/products"

@app.route('/')
def index():
    return render_template('products.html', products=get_products())

@app.route("/product/filter", methods=["GET"])
def filter_product():
    args = []
    for request_arg in request.args:
        args.append({'name': request_arg, 'value': request.args.get(request_arg)})
    return get_product_with_args(args)

@app.get("/product/<id>")
def get_product(id):
    return get_product_with_args({'name': 'id', 'value': id})

@app.post("/product")
def add_product_list():
    if request.is_json:
        product_data = request.get_json()
        product = Product.from_dict(product_data)
        return add_product(product)
    return {"error": "Request must be JSON"}, 415

if __name__ == "__main__":
    app.run(debug=True)