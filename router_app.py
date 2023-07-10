from flask import Flask, request, jsonify
from flask_cors import CORS
from models.model_workers import *
#get_all_workers, get_worker_by, post_worker, put_worker, del_worker
from models.model_calendars import *
#get_all_calendars, get_calendar_by, post_calendar, put_calendar, del_calendar
from models.model_vacations import *
#get_all_vacations, get_vacation_by, post_vacation, put_vacation, del_vacation


app = Flask(__name__)
cors = CORS(app)

#Crea la tabla si no existe
def initialize_tables():
    tables = [Workers, Calendars, Vacations]

    for table in tables:
        table.create_table()

# Llamar a la función para inicializar las tablas
initialize_tables()

@app.route("/") #Si me pides /
def hello_root():
    return '<h1>Probando el back</h1>'

@app.route("/workers", methods=['GET'])#Si me pides /workers con GET
def get_workers():
    workers = Workers.get_all_workers()
    print ("WORKERS", workers)
    # Aquí debes procesar la lista de workeros y devolverla como una respuesta adecuada, por ejemplo:
    return workers

@app.route("/workers/<worker_id>", methods=['GET']) #Si me pides /workers/ALGO con GET
def get_worker(worker_id):
    worker = Workers.get_worker_by_id(worker_id)
    if worker:        
        return jsonify(worker)
    else:
    # Si no se encuentra el workero, puedes devolver un mensaje de error o una respuesta vacía
        return jsonify({'message': 'Workero no encontrado'})


@app.route("/workers", methods=["POST"]) #Si me pides /workers con POST
def create_worker():
    data= request.get_json()
    print ('**createworker', data)
    Workers.post_worker(data)
    response = {'message': 'Worker created successfully'}
    return jsonify(response), 200

@app.route("/workers/<worker_id>", methods=["PUT"])
def update_worker(worker_id):
    data = request.get_json()
    print('**update_worker', data)
    result = Workers.put_worker(data, worker_id)
    if isinstance(result, str):
        return jsonify({"message": result})
    else:
        return jsonify({"message": "Worker updated successfully"})

@app.route("/workers/<worker_id>", methods=["PATCH"])
def patch_worker(worker_id):
    data = request.get_json()
    result = Workers.patch_worker(data, worker_id)
    if isinstance(result, str):
        return jsonify({"message": result})
    else:
        return jsonify({"message": "Worker updated successfully"})   

@app.route("/workers/<worker_id>", methods=['DELETE'])#Si me pides /workers/ALGO con DELETE
def delete_worker(worker_id): 
    Workers.delete_worker(worker_id)
    response = {'message': 'Worker deleted successfully'}
    return jsonify(response), 200

@app.route("/calendars", methods=['GET'])#Si me pides /calendars con GET
def get_calendars():
    calendars = Calendars.get_all_calendars()
    
    # Aquí debes procesar la lista de calendaros y devolverla como una respuesta adecuada, por ejemplo:
    return calendars

@app.route("/calendars/<calendar_id>", methods=['GET']) #Si me pides /calendars/ALGO con GET
def get_calendar(calendar_id):
    calendar = Calendars.get_calendar_by_id(calendar_id)
    if calendar:        
        return jsonify(calendar)
    else:
    # Si no se encuentra el calendar, puedes devolver un mensaje de error o una respuesta vacía
        return jsonify({'message': 'calendaro no encontrado'})

@app.route("/calendars", methods=["POST"]) #Si me pides /calendars con POST
def create_calendar():
    data= request.get_json()
    print ('**createcalendar', data)
    Calendars.post_calendar(data)
    response = {'message': 'calendar created successfully'}
    return jsonify(response), 200

@app.route("/calendars/<calendar_id>", methods=["PUT"])
def update_calendar(calendar_id):
    data = request.get_json()
    print('**update_calendar', data['id'])
    result = Calendars.put_calendar(data, calendar_id)
    if isinstance(result, str):
        return jsonify({"message": result})
    else:
        return jsonify({"message": "calendar updated successfully"})

@app.route("/calendars/<calendar_id>", methods=["PATCH"])
def patch_calendar(calendar_id):
    data = request.get_json()
    result = Calendars.patch_calendar(data, calendar_id)
    if isinstance(result, str):
        return jsonify({"message": result})
    else:
        return jsonify({"message": "calendar updated successfully"})   

@app.route("/calendars/<calendar_id>", methods=['DELETE'])#Si me pides /calendars/ALGO con DELETE
def delete_calendar(calendar_id): 
    Calendars.delete_calendar(calendar_id)
    response = {'message': 'calendar deleted successfully'}
    return jsonify(response), 200

@app.route("/vacations", methods=['GET'])#Si me pides /vacations con GET
def get_vacations():
    
    vacations = Vacations.get_all_vacations()
    
    # Aquí debes procesar la lista de vacations y devolverla como una respuesta adecuada, por ejemplo:
    return vacations

@app.route("/vacations/<vacation_id>", methods=['GET']) #Si me pides /vacations/ALGO con GET
def get_vacation(vacation_id):
    vacation = Vacations.get_vacation_by_id(vacation_id)
    if vacation:        
        return jsonify(vacation)
    else:
    # Si no se encuentra el vacation, puedes devolver un mensaje de error o una respuesta vacía
        return jsonify({'message': 'vacation no encontrado'})


@app.route("/vacations", methods=["POST"]) #Si me pides /vacations con POST
def create_vacation():
    data= request.get_json()
    print ('**createvacation', data)
    Vacations.post_vacation(data)
    response = {'message': 'vacation created successfully'}
    return jsonify(response), 200

@app.route("/vacations/<vacation_id>", methods=["PUT"])
def update_vacation(vacation_id):
    data = request.get_json()
    print('**update_vacation', data['id'])
    result = Vacations.put_vacation(data, vacation_id)
    if isinstance(result, str):
        return jsonify({"message": result})
    else:
        return jsonify({"message": "vacation updated successfully"})

@app.route("/vacations/<vacation_id>", methods=["PATCH"])
def patch_vacation(vacation_id):
    data = request.get_json()
    result = Vacations.patch_vacation(data, vacation_id)
    if isinstance(result, str):
        return jsonify({"message": result})
    else:
        return jsonify({"message": "vacation updated successfully"})   

@app.route("/vacations/<vacation_id>", methods=['DELETE'])#Si me pides /vacations/ALGO con DELETE
def delete_vacation(vacation_id): 
    Vacations.delete_vacation(vacation_id)
    response = {'message': 'vacation deleted successfully'}
    return jsonify(response), 200


@app.route("/login", methods=['POST'])
def get_logged_worker():
    login_data = request.json
    login_email = login_data.get('email')
    passw = login_data.get('passw')
    if login_email and passw:
        print ('@#@#@# get_logged_worker',login_data, login_email, passw)
    worker, token, secret = Workers.login(login_email, passw)
    if worker:
        return jsonify({'worker': worker, 'token': token, 'secret': secret})
    
    return jsonify({'message': 'Error en el login ROUTER'})
