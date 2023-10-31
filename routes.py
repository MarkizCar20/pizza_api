from flask import Flask, request, jsonify
from models import MenuItem, Order, User

ADMIN_TOKEN = "1234567812345678"

app = Flask(__name__)

menu = [
    MenuItem("Margherita", 10.99),
    MenuItem("Pepperoni", 15.00),
    #Add more items - Or add a method to add more items I guesss?
]

users = []

orders = []

def check_user_exists(target_user):
    return any(
        user.username == target_user.username and
        user.email == target_user.email and
        user.address == target_user.address
        for user in users
    )


@app.route("/admin/menu", methods=["POST"])
def add_menu_item():
    token = request.headers.get("Authorization")

    if token != ADMIN_TOKEN:
        return jsonify({"message": "Not Authorized"}), 401
    
    data = request.get_json()
    item_name = data["name"]
    item_price = data["price"]
    new_item = MenuItem(item_name, item_price)
    menu.append(new_item)

    return jsonify({"message": "Added new menu item"}), 200

@app.route("/admin/menu/<item_name>", methods=["DELETE"])
def delete_item(item_name):
    token = request.headers.get("Authorization")

    if token != ADMIN_TOKEN:
        return jsonify({"message": "Not Authorized"}), 401
    
    item_to_delete = next((item for item in menu if item.name == item_name), None)

    if item_to_delete:
        menu.remove(item_to_delete)
        return jsonify({"message": f"Menu item {item_name} removed from menu"}), 200
    return jsonify({"message": f"Menu item {item_name} not found!"}), 404

@app.route("/admin/order/cancel/<int:order_id>", methods=["DELETE"])
def cancel_order_admin(order_id):
    if 0 <= order_id < len(orders):
        orders.pop(order_id)
        return jsonify({"message":"Order canceled"}), 201

@app.route("/menu", methods=["GET"])
def get_menu():
    menu_data = [{"name":item.name, "price":item.price} for item in menu]
    return jsonify(menu_data), 200

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    username = data["username"]
    user_email = data["email"]
    user_address = data["address"]
    selected_items = data["items"]
    if (user_address == "") and (any(
        user.username == username and
        user.email == user_email
        for user in users
    ) == False):
        return jsonify({"message":f"User {username} isn't registered. Register or provide user address"}), 404       
    items = [item for item in menu if item.name in selected_items]
    if (items == None):
        return jsonify({"message": "Pizza doesn't exist in menu"}), 404
    for user_to_find in users:
        if user_to_find.username == username and user_to_find.email == user_email:
            user_address = user_to_find.address
    user = User(username, user_email, user_address)
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
            return jsonify({"message": "Order canceled!"}), 201
        return jsonify({"message": "Cannot cancel ready order!"}), 400
    return jsonify({"message": "Order not found"}), 404

@app.route("/user/register", methods=["POST"])
def user_register():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    address = data["address"]
    user = User(username, email, address)
    if check_user_exists(user): #this should check if the user already exists and won't add a new one
        return jsonify({"message":f"User {username} already exists"}), 400
    users.append(user)
    return jsonify({"message":f"User {username} registered"}), 200

if __name__ == "__main__":
    app.run(debug=True)