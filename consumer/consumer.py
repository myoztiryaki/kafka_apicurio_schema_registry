from sqlmodel import Field, SQLModel, create_engine, Session
import requests
from confluent_kafka import Consumer
from avro.io import DatumReader, BinaryDecoder
from io import BytesIO
from avro.schema import parse
import json

# Apicurio Registry URL ve Şema Bilgisi
REGISTRY_URL = "http://localhost:8080/apis/registry/v2/groups/default"
schema_id = "33e4eff9-b9d6-47f4-9814-c1383d043625"  

# Şema çekme ve ayrıştırma
schema_response = requests.get(f"{REGISTRY_URL}/artifacts/{schema_id}")
schema = parse(json.dumps(schema_response.json()))  # JSON'u string formatına dönüştürdük

# SQLModel Tablo Tanımı
class ChurnTable(SQLModel, table=True):
    RowNumber: int = Field(primary_key=True)
    CustomerId: int
    Surname: str
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float
    Exited: int

# PostgreSQL bağlantısı
DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/mydatabase"
engine = create_engine(DATABASE_URL)

# Tabloyu oluştur
SQLModel.metadata.create_all(engine)

# Kafka Consumer ayarları
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(consumer_config)
consumer.subscribe(['churn-topic'])

# Mesajları tüketme ve PostgreSQL'e ekleme
with Session(engine) as session:
    while True:
        message = consumer.poll(1.0)
        if message is None:
            continue
        if message.error():
            print(f"Consumer error: {message.error()}")
            continue

        # Avro verisini çözümleme
        avro_bytes = BytesIO(message.value())
        decoder = BinaryDecoder(avro_bytes)
        reader = DatumReader(schema)
        record = reader.read(decoder)

        # SQLModel nesnesi oluştur ve veritabanına ekle

        # Mevcut kaydı kontrol et
        existing_record = session.get(ChurnTable, record['RowNumber'])
        if existing_record is None:  # Kayıt yoksa ekle
            churn_record = ChurnTable(
                RowNumber=record['RowNumber'],
                CustomerId=record['CustomerId'],
                Surname=record['Surname'],
                CreditScore=record['CreditScore'],
                Geography=record['Geography'],
                Gender=record['Gender'],
                Age=record['Age'],
                Tenure=record['Tenure'],
                Balance=record['Balance'],
                NumOfProducts=record['NumOfProducts'],
                HasCrCard=record['HasCrCard'],
                IsActiveMember=record['IsActiveMember'],
                EstimatedSalary=record['EstimatedSalary'],
                Exited=record['Exited']
            )
            session.add(churn_record)
            session.commit()
        else:
            print(f"Record with RowNumber {record['RowNumber']} already exists. Skipping.")

        # Eklenen kaydı ekrana yazdır
        print(f"Consumed Record: {record}")
        
# PostgreSQL ve Kafka Consumer bağlantılarını kapatma
consumer.close()