from flask import Flask, request, jsonify
from sqlalchemy import Column, Integer, String, Date, Boolean
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

# Obtener valores de las variables de entorno
pg_host = os.getenv("PGSQL_HOST")
pg_user = os.getenv("PGSQL_USER")
pg_password = os.getenv("PGSQL_PASSWORD")
pg_database = os.getenv("PGSQL_DATABASE")

# Construir la cadena de conexión
connectionString = f"postgresql://{pg_user}:{pg_password}@{pg_host}:5432/{pg_database}"
#database
app.config["SQLALCHEMY_DATABASE_URI"] = connectionString
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

class STORE(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

class EMPLOYEE(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

class INVENTORY(db.Model):
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, nullable=False)
    employee_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    flavor = Column(String(255), nullable=False)
    is_season_flavor = Column(Boolean, nullable=False)
    quantity = Column(Integer, nullable=False)

    def __init__(self, id, store_id, employee_id, date, flavor, is_season_flavor, quantity):
        self.id = id
        self.store_id = store_id
        self.employee_id = employee_id
        self.date = date
        self.flavor = flavor
        self.is_season_flavor = is_season_flavor
        self.quantity = quantity

#schemas =========================================================================================

class StoreSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

store_schema = StoreSchema()
stores_schema = StoreSchema(many=True)

class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

class InventorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'store_id', 'employee_id', 'date', 'flavor', 'is_season_flavor', 'quantity')

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)

#===================================================================================================

@app.route('/stores/get', methods=['GET'])
def get_stores():
    all_stores = STORE.query.all()
    result = stores_schema.dump(all_stores)
    return jsonify(result)

@app.route('/stores/post', methods=['POST'])
def add_store():
    name = request.json['name']
    new_store = STORE(name=name)
    db.session.add(new_store)
    db.session.commit()
    return store_schema.jsonify(new_store)

@app.route('/stores/get/<int:id>', methods=['GET'])
def get_store(id):
    store_obj = STORE.query.get(id)
    return store_schema.jsonify(store_obj)

@app.route('/stores/put/<int:id>', methods=['PUT'])
def update_store(id):
    store_obj = STORE.query.get(id)
    name = request.json['name']
    store_obj.name = name
    db.session.commit()
    return store_schema.jsonify(store_obj)

@app.route('/stores/delete/<int:id>', methods=['DELETE'])
def delete_store(id):
    store_obj = STORE.query.get(id)
    db.session.delete(store_obj)
    db.session.commit()
    return store_schema.jsonify(store_obj)

#===================================================================================================
@app.route('/employees', methods=['GET'])
def get_employees():
    all_employees = EMPLOYEE.query.all()
    result = employees_schema.dump(all_employees)
    return jsonify(result)

@app.route('/employees', methods=['POST'])
def add_employee():
    name = request.json['name']
    new_employee = EMPLOYEE(name=name)
    db.session.add(new_employee)
    db.session.commit()
    return employee_schema.jsonify(new_employee)

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee_obj = EMPLOYEE.query.get(id)
    return employee_schema.jsonify(employee_obj)

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee_obj = EMPLOYEE.query.get(id)
    name = request.json['name']
    employee_obj.name = name
    db.session.commit()
    return employee_schema.jsonify(employee_obj)

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee_obj = EMPLOYEE.query.get(id)
    db.session.delete(employee_obj)
    db.session.commit()
    return employee_schema.jsonify(employee_obj)

# Rutas para la clase Inventory #===================================================================================================
@app.route('/inventories', methods=['GET'])
def get_inventories():
    all_inventories = INVENTORY.query.all()
    result = inventories_schema.dump(all_inventories)
    return jsonify(result)

@app.route('/inventories', methods=['POST'])
def add_inventory():
    store_id = request.json['store_id']
    employee_id = request.json['employee_id']
    date = request.json['date']
    flavor = request.json['flavor']
    is_season_flavor = request.json['is_season_flavor']
    quantity = request.json['quantity']
    
    new_inventory = INVENTORY(
        store_id=store_id,
        employee_id=employee_id,
        date=date,
        flavor=flavor,
        is_season_flavor=is_season_flavor,
        quantity=quantity
    )

    db.session.add(new_inventory)
    db.session.commit()
    return inventory_schema.jsonify(new_inventory)

@app.route('/inventories/<int:id>', methods=['GET'])
def get_inventory(id):
    inventory_obj = INVENTORY.query.get(id)
    return inventory_schema.jsonify(inventory_obj)

@app.route('/inventories/<int:id>', methods=['PUT'])
def update_inventory(id):
    inventory_obj = INVENTORY.query.get(id)
    store_id = request.json['store_id']
    employee_id = request.json['employee_id']
    date = request.json['date']
    flavor = request.json['flavor']
    is_season_flavor = request.json['is_season_flavor']
    quantity = request.json['quantity']

    inventory_obj.store_id = store_id
    inventory_obj.employee_id = employee_id
    inventory_obj.date = date
    inventory_obj.flavor = flavor
    inventory_obj.is_season_flavor = is_season_flavor
    inventory_obj.quantity = quantity

    db.session.commit()
    return inventory_schema.jsonify(inventory_obj)

@app.route('/inventories/<int:id>', methods=['DELETE'])
def delete_inventory(id):
    inventory_obj = INVENTORY.query.get(id)
    db.session.delete(inventory_obj)
    db.session.commit()
    return inventory_schema.jsonify(inventory_obj)

#===================================================================================================

if __name__ == '__main__':
    app.run(debug=True)