from flask import Flask
from routes.index import app as index_blueprint
from routes.product import app as product_blueprint

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(index_blueprint)
app.register_blueprint(product_blueprint, url_prefix='/products')

if __name__ == '__main__':
    app.run(debug=True)