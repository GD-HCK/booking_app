from flask import Flask
from routes.index_controller import app as index_controller
from routes.booking_controller import app as booking_controller

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(index_controller)
app.register_blueprint(booking_controller, url_prefix='/bookings')

if __name__ == '__main__':
    app.run(debug=True)