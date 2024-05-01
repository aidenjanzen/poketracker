import requests
import webbrowser

FLASK_URL = "http://localhost:8888"


def http(method, path, data=None):
    print(f"Making {method} request to {FLASK_URL + path}...")
    if method not in ["GET", "POST", "PUT", "DELETE"]:
        raise RuntimeWarning("Invalid method")
    
    if method == "GET":
        response = requests.get(FLASK_URL + path)
    elif method == "POST":
        response = requests.post(FLASK_URL + path, json=data)
    elif method == "PUT":
        response = requests.put(FLASK_URL + path, json=data)
    elif method == "DELETE":
        response = requests.delete(FLASK_URL + path)
    
    badcodes = [400, 404, 500] #should make this a range
    print("Received status code:", response.status_code)
    if response.status_code in badcodes:
        print(response.content)

    return response

def get(path):
    return http("GET", path)


def post(path, data=None):
    return http("POST", path, data)


def put(path, data=None):
    return http("PUT", path, data)


def delete(path):
    return http("DELETE", path)


def demo():
    # updates customer balance 
    print("updating customer balance for: id 1")
    put("/api/customers/1", {"balance": 1000})
    input("Check for balance in webpage. Enter when ready.")
    webbrowser.open(FLASK_URL + "/customers/1")
    input("Press Enter to continue.")

    #creates three new products
    print("Adding a new product: 'salty nuts' (6.99)")
    post("/api/products/", {"name": "salty nuts", "price": 6.99})
    input("Check for salty nuts in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")

    print("Adding a new product: 'popcorn' (7.99)")
    post("/api/products/", {"name": "popcorn", "price": 7.99})    
    input("Check for popcorn in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")

    print("Adding a new product: 'monster' (4.99)")
    post("/api/products/", {"name": "monster", "price": 4.99, "available": 200}) #you can also specify the amount default is one
    input("Check for monster in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")

    # creates 3 new orders
    print("Adding a new order: NOK 1") #id 10
    post("/api/orders", {
        "customer_id": 1,
        "items": [
            {
            "name": "salty nuts",
            "quantity": 100
            },
        ]
    })
    input("Check for order in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders/10")
    input("Press Enter to continue.")

    print("Adding a new order: NOK 2") #id 11
    post("/api/orders", {
        "customer_id": 1,
        "items": [
            {
            "name": "salty nuts",
            "quantity": 100
            },
            {
            "name": "popcorn",
            "quantity": 100
            },
            {
            "name": "monster",
            "quantity": 5
            },
        ]
    })
    input("Check for order in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders/11")
    input("Press Enter to continue.")

    print("Adding a new order: OK") #12
    post("/api/orders", {
        "customer_id": 1,
        "items": [
            {
            "name": "monster",
            "quantity": 10
            },
        ]
    })
    input("Check for order in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders/12")
    input("Press Enter to continue.")
    #process ok order
    print("Processing a order: OK")
    put("/api/orders/12", {
        "process": True, #this will use default strategy adjust 
    })
    input("Check for order in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders/12")
    input("Press Enter to continue.")


    #process not ok order 2
    print("Processing a order: NOK 2 with reject")
    put("/api/orders/11", {
        "process": True,
        "strategy": "reject",
    })
    input("Check for change in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders/11")
    #process not ok with ignore
    input("Press Enter to continue.")
    print("Processing same order NOK 2 with ignore.")
    put("/api/orders/11", {
        "process": True,
        "strategy": "ignore",
    })
    input("Check for change in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders/11")
    input("Press Enter to continue.")

    #process not ok order 1
    print("Processing a order: NOK 1 with adjust")
    put("/api/orders/10", {
        "process": True,
    })
    input("Check for order in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders/10")
    input("Press Enter to continue.")

    # error checking
    # create order with not existing product
    print("Adding a new order with bad product")
    post("/api/orders", {
        "customer_id": 1,
        "items": [
            {
            "name": "monkey",
            "quantity": 10
            },
        ]
    })
    input("Check for order in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders")
    input("Press Enter to continue.")

    # create an order with invalid value \
    print("Adding a new order with invalid value")
    post("/api/orders", {
        "customer_id": 1,
        "items": [
            { 
            "name": "monster",
            "quantity": "hwlloe randome",
            },
        ]
    })
    input("Check for order in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/orders")
    input("Press Enter to continue.")

    # add product with invalid price 
    print("Adding a new product: 'cow feed' (string value)")
    post("/api/products/", {"name": "cow feed", "price": "123"}) #if you put a bad value in the name it also returns an error
    input("Check for cow feed in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")

if __name__ == "__main__":
    demo()
