# تحميل Apache Kafka
##اذهب إلى الموقع الرسمي: https://kafka.apache.org/downloads

# تشغيل Zookeeper و Kafka
## Kafka يحتاج Zookeeper ليشتغل (للتنسيق بين الخوادم).

### افتح نافذتين لـ Command Prompt (نافذتين مختلفتين):

### في الأولى، اكتب لتشغيل Zookeeper:
cd C:\kafka\kafka_3.x.x\bin\windows
zookeeper-server-start.bat ..\..\config\zookeeper.properties

### في الثانية، لتشغيل Kafka:
cd C:\kafka\kafka_3.x.x\bin\windows
kafka-server-start.bat ..\..\config\server.properties

# إنشاء Topic
### افتح نافذة جديدة لـ Command Prompt.
### أنشئ Topic باسم test:
kafka-topics.bat --create --topic test --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

# تشغيل منتج (Producer) ومستهلك (Consumer)
## ✅ Producer 
### افتح نافذة جديدة، واكتب:
kafka-console-producer.bat --broker-list localhost:9092 --topic test
## ✅  Consumer
kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic test --from-beginning
### الآن، سترى كل الرسائل التي أرسلها المنتج.

# مشروع IoT بسيط باستخدام Kafka
# 🔧 محاكاة جهاز IoT باستخدام Apache Kafka وPython

## 📌 وصف المشروع

هذا المشروع يُحاكي جهاز IoT (مثل مستشعر درجة الحرارة والرطوبة) يرسل بيانات إلى **Apache Kafka** باستخدام Python. يتم إرسال البيانات من خلال سكريبت Python (`iot_sensor.py`) ويتم استهلاكها بواسطة مستهلك Kafka.

---

## ✅ المتطلبات

- **Apache Kafka** (مثبت ويعمل بشكل صحيح)
- **Python 3.x**
- مكتبة `kafka-python`

---

## 📦 تثبيت المتطلبات

### 1. تثبيت Python  

### 2. تثبيت مكتبة `kafka-python`

```bash
pip install kafka-python

# خطوات التشغيل 
## تشغيل Zookeeper

























