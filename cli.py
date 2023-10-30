import argparse
import json
from flask import jsonify
import requests

#CLI for the Pizza API

BASE_URL = "http://127.0.0.1:5000"

headers = {
    "Content-type":"application/json",
    "Authorization":""
}

def admin_add_pizza(name, price):
    headers["Authorization"] = str(input("Provide authorization key: "))
    data = {
        "name":name,
        "price":price
    }
    response = requests.post(f"{BASE_URL}/admin/menu", json=data, headers=headers)
    #print(response.status_code)
    if (response.status_code == 401) or (response.status_code == 405):
        print("Auth key non valid - User not authorized")
    else:
        print("Item added to the menu")

def admin_delete_pizza(name):
    headers["Authorization"] = str(input("Provide authorization key: "))
    response = requests.delete(f"{BASE_URL}/admin/menu/{name}", headers=headers)
    #print(response.status_code)
    if response.status_code == 200:
        print("Item removed from menu")
    else:
        print("Item not found")

def admin_cancel_order(id):
    headers["Authorization"] = str(input("Provid authorization key: "))
    response = requests.delete(f"{BASE_URL}/admin/order/cancel/{id}", headers=headers)
    if response.status_code == 201:
        print("Order canceled by administrator")

def list_menu(): #lists the menu
    response = requests.get(f"{BASE_URL}/menu")
    if response.status_code == 200:
        menu = response.json()
        for item in menu:
            print(f"Pizza: {item['name']}, price {item['price']}")
    else:
        print(f"Failed to get menu.")

def create_order(username, email, address, items): #takes in username, email, address and a list of MenuItems you'd like to order
    data = {
        "username": username,
        "email": email,
        "address": address,
        "items": items   
    }
    response=requests.post(f"{BASE_URL}/orders", json=data)
    #print(response.status_code)
    if response.status_code == 200:
        print(f"Order created successfully")
    else:
        print(f"Failed to create order")
        #print(f"{response}")


def check_order_status(id): #checks the order status
    response=requests.get(f"{BASE_URL}/order/{id}")
    #print(response.status_code)
    if response.status_code == 200:
        status_code = response.json()
        print(f"Order status: {status_code['status']}")
    else:
        print("Order not found.")

def cancel_order(id): #deletes pizza
    response=requests.delete(f"{BASE_URL}/order/{id}")
    if response.status_code == 201:
        print("Order canceled.")
    elif response.status_code == 400:
        print("Cannot cancel ready order")
    else:
        print("Order not found.")
    
def register_user(username, address, email): #registers user
    data = {
        "username":username,
        "address": address,
        "email": email
    }
    response=requests.post(f"{BASE_URL}/user/register", json=data)
    if response.status_code == 400:
        print(f"User {username} already exists")
    else:
        print(f"User {username} registered")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pizza API CLI")

    parser.add_argument("--list-menu", action="store_true", help="List the menu")
    parser.add_argument("--create-order", metavar=("username", "email", "address", "items"), nargs="+", help="Create pizza order")
    parser.add_argument("--check-order-status", metavar=("order-id"), nargs=1, help="Check order status")
    parser.add_argument("--cancel-order", metavar=("order-id"), nargs=1 , help="Cancel pizza order")
    parser.add_argument("--create-order", metavar=("username", "email", "address", "items"), nargs="+", help="Create pizza order")
    parser.add_argument("--add-pizza", metavar=("name", "price"), nargs=2, help="Add pizza to the menu *Admin only option*")
    parser.add_argument("--delete-pizza", metavar=("name"), nargs=1, help="Delete pizza from the menu *Admin only option*")
    parser.add_argument("--admin-cancel-order", metavar=("id"), nargs=1, help="Cancel any order *Admin only option*")

    args = parser.parse_args()

    if args.list_menu:
        list_menu()
    elif args.create_order:
        create_order(args.create_order[0], args.create_order[1:])
    elif args.check_order_status:
        check_order_status(args.check_order_status)
    elif args.cancel_order:
        cancel_order(args.cancel_order)
    elif args.add_pizza:
        admin_add_pizza(args.add_pizza[0], float(args.add_pizza[1]))
    elif args.delete_pizza:
        admin_delete_pizza(args.delete_pizza)
    else:
        parser.print_help()

