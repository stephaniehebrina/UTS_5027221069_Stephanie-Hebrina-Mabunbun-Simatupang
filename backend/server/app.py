from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sys
sys.path.append('../')
import grpc
import apotekz_pb2
import apotekz_pb2_grpc
import os

app = Flask(__name__)
CORS(app)

grpc_channel = grpc.insecure_channel('localhost:5002')
grpc_stub = apotekz_pb2_grpc.MedicineServiceStub(grpc_channel)

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/src/'))
app.template_folder = template_dir

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/addMedicine", methods=['POST'])
def add_medicine():
    data = request.json
    medicine_request = apotekz_pb2.Medicine(
        id=data['id'],
        name=data['name'],
        type=data['type'],
        quantity=data['quantity'],
        delivery_type=data['delivery_type']
    )
    response = grpc_stub.AddMedicine(medicine_request)
    return jsonify({"message": "Medicine added successfully"})


@app.route("/allMedicines")
def get_all_medicines():
    response = grpc_stub.GetAllMedicines(apotekz_pb2.Empty())
    medicine_list = [{"id": medicine.id, "name": medicine.name, "type": medicine.type, "quantity": medicine.quantity, "delivery_type": medicine.delivery_type} for medicine in response.medicines]
    return jsonify({"medicines": medicine_list})

@app.route("/medicine/<medicine_id>")
def get_medicine(medicine_id):
    response = grpc_stub.GetMedicine(apotekz_pb2.MedicineId(id=medicine_id))
    if response.id:
        medicine_data = {"id": response.id, "name": response.name, "type": response.type, "quantity": response.quantity, "delivery_type": response.delivery_type}
        return jsonify(medicine_data)
    else:
        return jsonify({"message": "Medicine not found"}), 404
    
@app.route("/updateMedicine/<medicine_id>", methods=['PUT'])
def update_medicine(medicine_id):
    data = request.json
    medicine_request = apotekz_pb2.Medicine(
        id=medicine_id,
        name=data['name'],
        type=data['type'],
        quantity=data['quantity'],
        delivery_type=data['delivery_type']
    )
    response = grpc_stub.UpdateMedicine(medicine_request)
    return jsonify({"message": "Medicine updated successfully"})


@app.route("/deleteMedicine/<medicine_id>", methods=['DELETE'])
def delete_medicine(medicine_id):
    response = grpc_stub.DeleteMedicine(apotekz_pb2.MedicineId(id=medicine_id))
    return jsonify({"message": "Medicine deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
