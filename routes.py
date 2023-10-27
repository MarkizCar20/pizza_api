from flask import Flask, request, jsonify
from models import MenuItem, Order, User

app = Flask(__name__)

menu = [
    MenuItem("Margherita", 10.99),
    MenuItem("Pepperoni", 15.00),
    #Add more items - Or add a method to add more items I guesss?
]

orders = []

@app.route("/menu", methods=["GET"])
def get_menu():
    menu_data = [{"name":item.name, "price":item.price} for item in menu]
    return jsonify(menu_data)

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    username = data["username"]
    user_address = data["address"]
    user_email = data["email"]
    selected_items = data["items"]

    user = User(username, user_address, user_email)
    items = [item for item in menu if item.name in selected_items]
    new_order = Order(user, items)
    orders.append(new_order)

    return jsonify({"message": "Order created successfully"})

@app.route("/order/<int:order_id>", methods=["GET"])
def check_order_status(order_id):
    if 0 <= order_id < len(orders):
        return jsonify({"status": orders[order_id].status})
    return jsonify({"error":"Order not found"}), 404

@app.route("/order/<int:order_id>", methods=["DELETE"])
def cancel_order(order_id):
    if 0 <= order_id < len(orders):
        if orders[order_id].status != "Ready to be delivered":
            orders.pop(order_id)
            return jsonify({"message": "Order canceled!"})
        return jsonify({"message": "Cannot cancel ready order!"}), 400
    return jsonify({"message": "Order not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)