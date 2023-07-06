from flask import Flask, request, jsonify
from flask_cors import CORS
from models.model_products import *
#get_all_products, get_product_by, post_product, put_product, del_product
from models.model_quotations import *
#get_all_quotations, get_quotation_by, post_quotation, put_quotation, del_quotation
from models.model_customers import *
#get_all_customers, get_customer_by, post_customer, put_customer, del_customer
from models.model_users import *
#get_all_users, get_user_by, post_user, put_user, del_user, login(login_email, passw)

app = Flask(__name__)
cors = CORS(app)

#Crea la tabla si no existe
def initialize_tables():
    tables = [Product, Quotation, Customer, Users]

    for table in tables:
        table.create_table()

# Llamar a la función para inicializar las tablas
initialize_tables()

@app.route("/") #Si me pides /
def hello_root():
    return '<h1>Probando el back</h1>'

@app.route("/products", methods=['GET'])#Si me pides /products con GET
def get_products():
    products = Product.get_all_products()
    
    # Aquí debes procesar la lista de productos y devolverla como una respuesta adecuada, por ejemplo:
    return products

@app.route("/products/<product_id>", methods=['GET']) #Si me pides /products/ALGO con GET
def get_product(product_id):
    product = Product.get_product_by_id(product_id)
    if product:        
        return jsonify(product)
    else:
    # Si no se encuentra el producto, puedes devolver un mensaje de error o una respuesta vacía
        return jsonify({'message': 'Producto no encontrado'})


@app.route("/products", methods=["POST"]) #Si me pides /products con POST
def create_product():
    data= request.get_json()
    print ('**createproduct', data)
    Product.post_product(data)
    response = {'message': 'Product created successfully'}
    return jsonify(response), 200

@app.route("/products/<product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json()
    print('**update_product', data['id'])
    result = Product.put_product(data, product_id)
    if isinstance(result, str):
        return jsonify({"message": result})
    else:
        return jsonify({"message": "Product updated successfully"})

@app.route("/products/<product_id>", methods=["PATCH"])
def patch_product(product_id):
    data = request.get_json()
    result = Product.patch_product(data, product_id)
    if isinstance(result, str):
        return jsonify({"message": result})
    else:
        return jsonify({"message": "Product updated successfully"})   

@app.route("/products/<product_id>", methods=['DELETE'])#Si me pides /products/ALGO con DELETE
def delete_product(product_id): 
    Product.delete_product(product_id)
    response = {'message': 'Product deleted successfully'}
    return jsonify(response), 200

@app.route("/quotations", methods=['GET'])#Si me pides /quotations con GET
def get_quotations():
    quotations = Quotation.get_all_quotations()
    
    # Aquí debes procesar la lista de quotationos y devolverla como una respuesta adecuada, por ejemplo:
    return quotations

@app.route("/quotations/<quotation_id>", methods=['GET']) #Si me pides /quotations/ALGO con GET
def get_quotation(quotation_id):
    quotation = Quotation.get_quotation_by_id(quotation_id)
    if quotation:        
        return jsonify(quotation)
    else:
    # Si no se encuentra el quotation, puedes devolver un mensaje de error o una respuesta vacía
        return jsonify({'message': 'quotationo no encontrado'})

@app.route("/quotations", methods=["POST"]) #Si me pides /quotations con POST
def create_quotation():
    data= request.get_json()
    print ('**createquotation', data)
    Quotation.post_quotation(data)
    response = {'message': 'quotation created successfully'}
    return jsonify(response), 200

@app.route("/quotations/<quotation_id>", methods=["PUT"])
def update_quotation(quotation_id):
    data = request.get_json()
    print('**update_quotation', data['id'])
    result = Quotation.put_quotation(data, quotation_id)
    if isinstance(result, str):
        return jsonify({"message": result})
    else:
        return jsonify({"message": "quotation updated successfully"})

@app.route("/quotations/<quotation_id>", methods=["PATCH"])
def patch_quotation(quotation_id):
    data = request.get_json()
    result = Quotation.patch_quotation(data, quotation_id)
    if isinstance(result, str):
        return jsonify({"message": result})
    else:
        return jsonify({"message": "quotation updated successfully"})   

@app.route("/quotations/<quotation_id>", methods=['DELETE'])#Si me pides /quotations/ALGO con DELETE
def delete_quotation(quotation_id): 
    Quotation.delete_quotation(quotation_id)
    response = {'message': 'quotation deleted successfully'}
    return jsonify(response), 200

@app.route("/customers", methods=['GET'])#Si me pides /customers con GET
def get_customers():
    
    customers = Customer.get_all_customers()
    
    # Aquí debes procesar la lista de customers y devolverla como una respuesta adecuada, por ejemplo:
    return customers

@app.route("/customers/<customer_id>", methods=['GET']) #Si me pides /customers/ALGO con GET
def get_customer(customer_id):
    customer = Customer.get_customer_by_id(customer_id)
    if customer:        
        return jsonify(customer)
    else:
    # Si no se encuentra el customer, puedes devolver un mensaje de error o una respuesta vacía
        return jsonify({'message': 'customer no encontrado'})


@app.route("/customers", methods=["POST"]) #Si me pides /customers con POST
def create_customer():
    data= request.get_json()
    print ('**createcustomer', data)
    Customer.post_customer(data)
    response = {'message': 'customer created successfully'}
    return jsonify(response), 200

@app.route("/customers/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    data = request.get_json()
    print('**update_customer', data['id'])
    result = Customer.put_customer(data, customer_id)
    if isinstance(result, str):
        return jsonify({"message": result})
    else:
        return jsonify({"message": "customer updated successfully"})

@app.route("/customers/<customer_id>", methods=["PATCH"])
def patch_customer(customer_id):
    data = request.get_json()
    result = Customer.patch_customer(data, customer_id)
    if isinstance(result, str):
        return jsonify({"message": result})
    else:
        return jsonify({"message": "customer updated successfully"})   

@app.route("/customers/<customer_id>", methods=['DELETE'])#Si me pides /customers/ALGO con DELETE
def delete_customer(customer_id): 
    Customer.delete_customer(customer_id)
    response = {'message': 'customer deleted successfully'}
    return jsonify(response), 200


@app.route("/login", methods=['POST'])
def get_logged_user():
    login_data = request.json
    login_email = login_data.get('login_email')
    passw = login_data.get('passw')
    if login_email and passw:
        print ('@#@#@# get_logged_user',login_data, login_email, passw)
    user, token = Users.login(login_email, passw)
    if user:
        return jsonify({'user': user, 'token': token})
    
    return jsonify({'message': 'Error en el login ROUTER'})
