# تحميل Apache Kafka
## اذهب إلى الموقع الرسمي: https://kafka.apache.org/downloads

# تشغيل Zookeeper و Kafka

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
# إنشاء Topic
## افتح نافذة جديدة لـ Command Prompt.

```sh
kafka-topics.bat --create --topic test --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
# تشغيل منتج (Producer) ومستهلك (Consumer)
## ✅ Producer 
### افتح نافذة جديدة، واكتب:
```sh
kafka-console-producer.bat --broker-list localhost:9092 --topic test
```
## ✅  Consumer
```sh
kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic test --from-beginning
```
### الآن، سترى كل الرسائل التي أرسلها المنتج.


# 🔧 محاكاة جهاز IoT باستخدام Apache Kafka وPython

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

---

### 2. تشغيل Zookeeper وKafka

فتح نافذتين من الطرفية و تشغيل:

**Zookeeper:**

```bash
cd G:\kafka_2.13-3.7.2\bin\windows
.\zookeeper-server-start.bat ..\..\config\zookeeper.properties
```

**خادم Kafka:**

```bash
cd G:\kafka_2.13-3.7.2\bin\windows
.\kafka-server-start.bat ..\..\config\server.properties
```

---

### 3. إنشاء Topic في Kafka

```bash
cd G:\kafka_2.13-3.7.2\bin\windows
.\kafka-topics.bat --create --topic test --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

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

    producer.send('test', message.encode('utf-8'))
    time.sleep(5)
```

```bash
python iot_sensor.py
```

---

### 5. استهلاك الرسائل باستخدام Kafka Consumer

فتح نافذة طرفية جديدة:

```bash
cd G:\kafka_2.13-3.7.2\bin\windows
.\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic test --from-beginning
```

---

## ✅ مثال على المخرجات

**نافذة المنتج (Producer):**



**نافذة المستهلك (Consumer):**



---





















