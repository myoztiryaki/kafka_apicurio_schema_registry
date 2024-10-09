import requests
import json

# Avro Şeması Tanımı
schema = {
    "type": "record",
    "name": "Customer",
    "fields": [
        {"name": "RowNumber", "type": "int"},
        {"name": "CustomerId", "type": "int"},
        {"name": "Surname", "type": "string"},
        {"name": "CreditScore", "type": "int"},
        {"name": "Geography", "type": "string"},
        {"name": "Gender", "type": "string"},
        {"name": "Age", "type": "int"},
        {"name": "Tenure", "type": "int"},
        {"name": "Balance", "type": "float"},
        {"name": "NumOfProducts", "type": "int"},
        {"name": "HasCrCard", "type": "int"},
        {"name": "IsActiveMember", "type": "int"},
        {"name": "EstimatedSalary", "type": "float"},
        {"name": "Exited", "type": "int"}
    ]
}

# Şemayı Apicurio Registry'ye kaydet
url = "http://localhost:8080/apis/registry/v2/groups/default/artifacts"
headers = {"Content-Type": "application/json"}

response = requests.post(url, headers=headers, data=json.dumps(schema))

if response.status_code == 200 or response.status_code == 201:
    print("Şema başarıyla kaydedildi.")
else:
    print("Şema kaydedilemedi:", response.status_code, response.text)
