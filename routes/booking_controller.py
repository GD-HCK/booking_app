# booking_form_blueprint.py
from ..classes.booking_class import *
from flask import Blueprint, request, jsonify, render_template, redirect
from flask_login import login_required
app = Blueprint('booking_controller', __name__)

# prefix = "/bookings"

# route '/'
# [GET]
@app.route('/', methods=['GET'])
@login_required
def index():
    """Return the booking form."""
    return redirect('/mybookings/form')

# route '/mybookings'
# [GET]
@app.route('/mybookings', methods=['GET'])
@login_required
def get_all_bookings():
    """Return all user's bookings."""
    return get_all_bookings()

# route '/mybookings/form'
@app.route('/mybookings/form', methods=['GET'])
@login_required
def get_booking_form():
    return render_template('booking_form.html', title='Booking Form')

# [POST]
@app.route("/mybookings/form", methods=["POST"])
@login_required
def add_booking():
    if request.is_json:
        booking_data = request.get_json()
        booking = booking.from_dict(booking_data)
        return add_booking(booking)
    return {"error": "Request must be JSON"}, 415

# route '/mybookings/filter'
# [GET]
@app.route("/mybookings/filter", methods=["GET"])
@login_required
def filter_bookings():
    args = []
    for request_arg in request.args:
        args.append({'name': request_arg, 'value': request.args.get(request_arg)})
    return get_booking_with_args(args)


# route '/mybookings/<booking_id>'
# [GET]
@app.route("/mybookings/<booking_id>", methods=["GET"])
@login_required
def get_booking(booking_id):
    return get_booking_with_args({'name': 'id', 'value': booking_id})

if __name__ == "__main__":
    app.run(debug=True)