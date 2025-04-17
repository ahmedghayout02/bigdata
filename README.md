# 1- تحميل Apache Kafka
 اذهب إلى الموقع الرسمي: https://kafka.apache.org/downloads

# 2- تشغيل Zookeeper و Kafka

##  لتشغيل Zookeeper:
```bash
cd C:\kafka\kafka_3.x.x\bin\windows
zookeeper-server-start.bat ..\..\config\zookeeper.properties
```
##   لتشغيل Kafka:
```sh
cd C:\kafka\kafka_3.x.x\bin\windows
kafka-server-start.bat ..\..\config\server.properties
```
# 3- إنشاء Topic
```sh
kafka-topics.bat --create --topic test --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
# 4- تشغيل منتج (Producer) ومستهلك (Consumer)
## ✅ Producer 
```sh
kafka-console-producer.bat --broker-list localhost:9092 --topic test
```
## ✅  Consumer
```sh
kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic test --from-beginning
```


# 5- محاكاة جهاز IoT باستخدام Apache Kafka وPython

## 📌 وصف المشروع

هذا المشروع يُحاكي جهاز IoT (مثل مستشعر درجة الحرارة والرطوبة) يرسل بيانات إلى **Apache Kafka**. يتم إرسال البيانات بواسطة سكريبت Python ويتم استهلاكها بواسطة مستهلك Kafka المدمج.

---

## ✅ المتطلبات

- Apache Kafka (مثبت ويعمل)
- Python 3.x
- مكتبة `kafka-python`

---

## 🚀 خطوات التشغيل

### 1. تثبيت المتطلبات

**تثبيت Python:**  

**تثبيت مكتبة kafka-python:**

```bash
pip install kafka-python
```
![image](https://github.com/user-attachments/assets/6cf0a356-2ad8-4eb8-bb9f-806466a0893f)


---

### 2. تشغيل Zookeeper وKafka

فتح نافذتين من الطرفية و تشغيل:

**Zookeeper:**

```bash
cd G:\kafka_2.13-3.7.2\bin\windows
.\zookeeper-server-start.bat ..\..\config\zookeeper.properties
```
![image](https://github.com/user-attachments/assets/bf7945ae-1950-46f1-85f7-0e40f9967bdc)


**خادم Kafka:**

```bash
cd G:\kafka_2.13-3.7.2\bin\windows
.\kafka-server-start.bat ..\..\config\server.properties
```
![image](https://github.com/user-attachments/assets/f086f507-cf2b-42ea-ae81-cc6f431774f5)


---

### 3. إنشاء Topic في Kafka

```bash
cd G:\kafka_2.13-3.7.2\bin\windows
.\kafka-topics.bat --create --topic ahmed --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
![image](https://github.com/user-attachments/assets/eaecfafc-7016-446b-beb8-e77bef21fc53)


---

### 4. تشغيل سكريبت محاكاة المستشعر

```python
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

while True:
    temperature = round(random.uniform(20, 40), 2)
    humidity = round(random.uniform(30, 70), 2)

    message = f"Temp: {temperature}°C, Humidity: {humidity}%"
    print(f"Sending: {message}")

    producer.send('ahmed', message.encode('utf-8'))
    time.sleep(5)
```

```bash
python iot_sensor.py
```
![image](https://github.com/user-attachments/assets/0a453918-189e-49c1-b292-830764d7867c)


---

### 5. استهلاك الرسائل باستخدام Kafka Consumer


```bash
cd G:\kafka_2.13-3.7.2\bin\windows
.\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic ahmed --from-beginning
```
![image](https://github.com/user-attachments/assets/81a8ee51-1a0e-4402-abaa-41cc11658958)





















