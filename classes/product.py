"""Product Class"""
import pyodbc
import json
from classes.configuration import *

# Database connection string
conn_str = get_connection_string()

# api/products/product.py
class Product:
    def __init__(self, name, price, category, id=None):
        self.id = id
        self.name = name
        self.price = price
        self.category = category

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


def run_query_get(query: str, *params) -> list:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query, *params)
    result = cursor.fetchall()
    conn.close()
    return result

def run_query_post(query: str, *params) -> int:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query, *params)
    conn.commit()
    conn.close()
    return 1

def add_product(product: Product):
    try:
        product_exists = run_query_get('SELECT id FROM Product WHERE id = ?', (product.id,))
        if product_exists:
            return "Product already exists."
        
        run_query_post('''
            INSERT INTO Product (name, price, category)
            VALUES (?, ?, ?)
        ''', (product.name, product.price, product.category))

        id = run_query_get('SELECT TOP 1 id FROM Product ORDER BY id DESC')[0][0]
        return f"""
Adding a product:
Product ID: {id}
Product Name: {product.name}
Product Price: {product.price}
Product Category: {product.category}
"""
    except Exception as e:
        return json.dumps({'status':"Error", 'message':str(e)})

def get_products():
    try:
        products = run_query_get('SELECT * FROM Product')
        return [Product(id=row[0], name=row[1], price=row[2], category=row[3]).__dict__ for row in products]
    except Exception as e:
        return json.dumps({'status':"Error", 'message':str(e)})
    
def get_product_with_args(args):
    try:
        # List of valid column names
        valid_columns = ['id', 'name', 'price', 'category']
        counter = 0
        query = 'SELECT * FROM Product WHERE '
        query_params = []
        
        for arg in args:
            column = arg["name"]
            value = arg["value"]
            
            if column in valid_columns:
                counter += 1
                query += f'{column} = ? AND '
                query_params.append(value)
        
        query = query.rstrip(' AND ')

        if counter == 0:
            raise Exception("Supply at least one valid parameter")
        
        # Assuming run_query_get is a function that executes the query with parameters
        products = run_query_get(query, query_params)
        
        if products:
            return [Product(id=product[0], name=product[1], price=product[2], category=product[3]).__dict__ for product in products]
        return {"error": "Product not found", 'parameters': args}, 404
    except Exception as e:
        return json.dumps({'status': "Error", 'message': str(e)})