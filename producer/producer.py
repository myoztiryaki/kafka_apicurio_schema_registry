import requests
import pandas as pd
from confluent_kafka import Producer
from avro.schema import Parse
from avro.io import DatumWriter, BinaryEncoder
from io import BytesIO
import json
import time

# Apicurio Registry ve Kafka bağlantı ayarları
REGISTRY_URL = 'http://localhost:8080/apis/registry/v2/groups/default/artifacts/33e4eff9-b9d6-47f4-9814-c1383d043625'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

producer_config = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'client.id': 'my-producer',
    'linger.ms': 10,
    'acks': 'all'
}

# Producer'ı oluşturma
producer = Producer(producer_config)

# Veri setini yükleme
df = pd.read_csv("https://raw.githubusercontent.com/erkansirin78/datasets/refs/heads/master/Churn_Modelling.csv")

# Apicurio Registry'den şema alma
response = requests.get(REGISTRY_URL)
if response.status_code == 200:
    schema_content = response.json()
    if schema_content:
        print("Şema başarıyla alındı.")
        schema = Parse(json.dumps(schema_content))  # JSON string'e dönüştürdük
    else:
        print("Şema içeriği bulunamadı. Yanıt:", response.json())
        exit(1)
else:
    print(f"Şema alınamadı: {response.status_code}, {response.text}")
    exit(1)

# Veriyi Avro formatında Kafka’ya gönderen fonksiyon
def send_avro_message(row):
    writer = DatumWriter(schema)
    bytes_writer = BytesIO()
    encoder = BinaryEncoder(bytes_writer)
    writer.write(row, encoder)
    return bytes_writer.getvalue()

# Mesajları Kafka’ya Avro formatında gönderme
for _, row in df.iterrows():
    avro_message = send_avro_message(row.to_dict())
    time.sleep(2)
    producer.produce("churn-topic", avro_message)
    print(f"Sent message: {row.to_dict()}")
    producer.flush()
