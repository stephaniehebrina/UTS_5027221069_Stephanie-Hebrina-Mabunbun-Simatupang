import grpc
import sys
sys.path.append('../')
import apotekz_pb2
import apotekz_pb2_grpc

def create_medicine(stub):
    medicine_id = input("Enter medicine ID: ")
    name = input("Enter medicine name: ")
    type = input("Enter medicine type: ")
    quantity = int(input("Enter medicine quantity: "))
    delivery_type = input("Enter medicine delivery type (pick up/delivery): ")

    medicine = apotekz_pb2.Medicine(id=medicine_id, name=name, type=type, quantity=quantity, delivery_type=delivery_type)
    response = stub.AddMedicine(medicine)
    print("AddMedicine Response:", response)

def get_all_medicines(stub):
    all_medicines = stub.GetAllMedicines(apotekz_pb2.Empty())
    print("GetAll Response:", all_medicines)

def get_medicine(stub):
    medicine_id = input("Enter medicine ID: ")
    medicine = stub.GetMedicine(apotekz_pb2.MedicineId(id=medicine_id))
    print("GetMedicine Response:", medicine)

def update_medicine(stub):
    medicine_id = input("Enter medicine ID to update: ")
    name = input("Enter updated medicine name: ")
    type = input("Enter updated medicine type: ")
    quantity = int(input("Enter updated medicine quantity: "))
    delivery_type = input("Enter updated medicine delivery type (pick up/delivery): ")

    medicine = apotekz_pb2.Medicine(id=medicine_id, name=name, type=type, quantity=quantity, delivery_type=delivery_type)
    response = stub.UpdateMedicine(medicine)
    print("UpdateMedicine Response:", response)

def delete_medicine(stub):
    medicine_id = input("Enter medicine ID to delete: ")
    response = stub.DeleteMedicine(apotekz_pb2.MedicineId(id=medicine_id))
    print("DeleteMedicine Response:", response)

def run():
    channel = grpc.insecure_channel('localhost:5002')
    stub = apotekz_pb2_grpc.MedicineServiceStub(channel)

    while True:
        print("\n1. Add Medicine\n2. Get All Medicines\n3. Get Medicine\n4. Update Medicine\n5. Delete Medicine\n6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_medicine(stub)
        elif choice == '2':
            get_all_medicines(stub)
        elif choice == '3':
            get_medicine(stub)
        elif choice == '4':
            update_medicine(stub)
        elif choice == '5':
            delete_medicine(stub)
        elif choice == '6':
            break
        else:
            print("Invalid choice! Please enter a valid option.")


if __name__ == '__main__':
    run()
