"""Booking Class"""
import json
from .sql_class import *

class Booking:
    def __init__(self, id, user_id, start_date, end_date, status):
        self.id = id
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


def add_booking(booking: Booking):
    try:
        booking_exists = run_query_get('SELECT id FROM Booking WHERE id = ?', (booking.id,))
        if booking_exists:
            return "Booking already exists."
        
        run_query_post('''
            INSERT INTO Booking (name, price, category)
            VALUES (?, ?, ?)
        ''', (booking.name, booking.price, booking.category))

        id = run_query_get('SELECT TOP 1 id FROM Booking ORDER BY id DESC')[0][0]
        return f"""
Adding a booking:
Booking ID: {id}
Booking Name: {booking.name}
Booking Price: {booking.price}
Booking Category: {booking.category}
"""
    except Exception as e:
        return json.dumps({'status':"Error", 'message':str(e)})

def get_bookings():
    try:
        bookings = run_query_get('SELECT * FROM Booking')
        return [Booking(id=row[0], name=row[1], price=row[2], category=row[3]).__dict__ for row in bookings]
    except Exception as e:
        return json.dumps({'status':"Error", 'message':str(e)})
    
def get_booking_with_args(args):
    try:
        # List of valid column names
        valid_columns = ['id', 'name', 'price', 'category']
        counter = 0
        query = 'SELECT * FROM Booking WHERE '
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
        bookings = run_query_get(query, query_params)
        
        if bookings:
            return [Booking(id=booking[0], name=booking[1], price=booking[2], category=booking[3]).__dict__ for booking in bookings]
        return {"error": "Booking not found", 'parameters': args}, 404
    except Exception as e:
        return json.dumps({'status': "Error", 'message': str(e)})