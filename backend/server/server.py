import grpc
import sys
import logging
sys.path.append('../')
import pymongo
from concurrent import futures
import apotekz_pb2
import apotekz_pb2_grpc

class MedicineService(apotekz_pb2_grpc.MedicineServiceServicer):
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["ApotekDatabase"]
        self.collection = self.db["MedicineList"]
        logging.info("Connected to MongoDB")

    def AddMedicine(self, request, context):
        logging.info("Received AddMedicine request: %s", request)
        medicine_data = {
            "id": request.id,
            "name": request.name,
            "type": request.type,
            "quantity": request.quantity,
            "delivery_type": request.delivery_type
        }
        self.collection.insert_one(medicine_data)
        return request

    def GetAllMedicines(self, request, context):
        logging.info("Received GetAllMedicines request")
        medicine_list = []
        for medicine_data in self.collection.find():
            medicine = apotekz_pb2.Medicine(
                id=medicine_data["id"],
                name=medicine_data["name"],
                type=medicine_data["type"],
                quantity=medicine_data["quantity"],
                delivery_type=medicine_data["delivery_type"]
            )
            medicine_list.append(medicine)
        return apotekz_pb2.MedicineList(medicines=medicine_list)
    
    def GetMedicine(self, request, context):
        logging.info("Received GetMedicine request for medicine ID: %s", request.id)
        medicine_data = self.collection.find_one({"id": request.id})
        if medicine_data:
            medicine = apotekz_pb2.Medicine(
                id=medicine_data["id"],
                name=medicine_data["name"],
                type=medicine_data["type"],
                quantity=medicine_data["quantity"],
                delivery_type=medicine_data["delivery_type"]
            )
            return medicine
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Medicine not found")
            return apotekz_pb2.Medicine()
        
    def UpdateMedicine(self, request, context):
        logging.info("Received UpdateMedicine request for medicine ID: %s", request.id)
        medicine_data = self.collection.find_one({"id": request.id})
        if medicine_data:
            updated_medicine_data = {
                "id": request.id,
                "name": request.name,
                "type": request.type,
                "quantity": request.quantity,
                "delivery_type": request.delivery_type
            }
            self.collection.update_one({"id": request.id}, {"$set": updated_medicine_data})
            return apotekz_pb2.Empty() 
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Medicine not found")
            return apotekz_pb2.Empty()

    def DeleteMedicine(self, request, context):
        logging.info("Received DeleteMedicine request for medicine ID: %s", request.id)
        result = self.collection.delete_one({"id": request.id})
        if result.deleted_count > 0:
            return apotekz_pb2.Empty()
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Medicine not found")
            return apotekz_pb2.Empty()

def serve():
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    apotekz_pb2_grpc.add_MedicineServiceServicer_to_server(MedicineService(), server)
    server.add_insecure_port('[::]:5002') 
    server.start()
    logging.info("Listening on port 5002")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
