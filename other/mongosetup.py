from pymongo import MongoClient

connection_string = "mongodb://localhost:27017/"
db_name = "test"

client = MongoClient(connection_string)
database = client[db_name]
users = database["users"]
admin_user = {
        "username": "admin",
        "full_name": "Administrator",
        "email": "admin@idoven.com",
        "hashed_password": "$2b$12$4M2FCTLRZ7ZtrqIfaOHx0uFPSQ7czthVwFvmb14NGOGvBmbz95.xO",  # Password: password
        "is_admin": True
}
users.insert_one(admin_user)

records = database["records"]
dummy_record = {
        "record_id": 0,
        "owner": "admin",
        "result": {
                "id": 0,
                "date": "2023-06-01 19:00:00",
                "lead_results": [],
        }
}
records.insert_one(dummy_record)
