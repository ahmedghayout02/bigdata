import time
import random
from kafka import KafkaProducer

# الاتصال بـ Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# إرسال بيانات كل 5 ثواني
while True:
    temperature = round(random.uniform(20, 40), 2)
    humidity = round(random.uniform(30, 70), 2)

    message = f"Temp: {temperature}°C, Humidity: {humidity}%"
    print(f"Sending: {message}")

    producer.send('test', message.encode('utf-8'))
    time.sleep(5)
