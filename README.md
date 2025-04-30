## تجهيز الكلاستر (Hadoop + Spark)

### تشغيل الكلاستر (ثلاث حاويات Hadoop):

```sh
docker start hadoop-master hadoop-worker1 hadoop-worker2
```

### الدخول إلى الحاوية master:

```sh
docker exec -it hadoop-master bash
```

### تشغيل خدمات Hadoop (داخل الحاوية master):

```sh
./start-hadoop.sh
```
## اختبار Spark-Shell مع Batch
### داخل الحاوية master، أنشئ ملف file1.txt:
```sh
echo "Hello Spark Wordcount! Hello Hadoop Also :)" > file1.txt
```
### رفع الملف إلى HDFS:
```sh
hdfs dfs -mkdir -p /user/root
hdfs dfs -put file1.txt
```
### تشغيل spark-shell:
```sh
spark-shell
```
![Screenshot 2025-04-30 153123](https://github.com/user-attachments/assets/b1ac459f-82dd-4be6-9700-e1a4d885034f)

### تنفيذ برنامج WordCount بسيط (سطر بسطر داخل spark-shell):
```sh
val lines = sc.textFile("file1.txt")
val words = lines.flatMap(_.split("\\s+"))
val wc = words.map(w => (w, 1)).reduceByKey(_ + _)
wc.saveAsTextFile("file1.count")
```
![Screenshot 2025-04-30 153305](https://github.com/user-attachments/assets/fa8323a9-1ff7-4ace-aa2b-ad2b82d7a86d)

### استرجاع النتائج من HDFS:
```sh
hdfs dfs -get file1.count
```
![Screenshot 2025-04-30 153456](https://github.com/user-attachments/assets/ea0a64c8-6094-4302-8803-99f129f0ff63)

### عرض النتائج:
```sh
hdfs dfs -tail file1.count/part-00001
``` 
![Screenshot 2025-04-30 153743](https://github.com/user-attachments/assets/7dffe07e-a448-4d5c-aadd-fad8ce9f1365)

## مشروع Batch كامل باستخدام Java و Spark
### إنشاء مشروع Maven:
![image](https://github.com/user-attachments/assets/84e23237-232a-471d-aae5-f0ed276d65bd)
### أضف ملف نصي للاختبار مثلاً loremipsum.txt في src/main/resources وتشغيله :
![Screenshot 2025-04-30 143231](https://github.com/user-attachments/assets/bc9e2fec-a0f0-450f-8a79-28954e244011)

### بناء jar:

```sh
mvn clean package
```
![Screenshot 2025-04-30 180126](https://github.com/user-attachments/assets/8d2418f1-a411-4c29-87bd-08db08580e95)

###  نسخ jar إلى hadoop-master:
```sh
docker cp target/wordcount-spark-1.0-SNAPSHOT.jar hadoop-master:/root/wordcount-spark.jar
```
![image](https://github.com/user-attachments/assets/e24d39b5-841c-4d1c-ba99-755202c90dd5)

###  تشغيله محلياً (في الحاوية):
```sh
spark-submit --class spark.batch.tp21.WordCountTask --master local wordcount-spark.jar input/purchases.txt out-spark
```
![Screenshot 2025-04-30 143314](https://github.com/user-attachments/assets/94328a36-27a6-4b51-9749-3b064111097d)
###  تشغيله على YARN Cluster:
```sh
spark-submit --class spark.batch.tp21.WordCountTask --master yarn --deploy-mode cluster wordcount-spark.jar input/purchases.txt out-spark2
```
## مشروع Spark Streaming:
### إنشاء مشروع Maven جديد:
![image](https://github.com/user-attachments/assets/beb5e66c-2fa8-466b-91ac-46b8defcac7a)
### بناء jar:

```sh
mvn package
```
![image](https://github.com/user-attachments/assets/f0a24d52-527b-4935-854f-f1126d509649)

### نسخ JAR إلى الحاوية:
```sh
docker cp target/stream-1.0-SNAPSHOT.jar hadoop-master:/root/stream-1.jar
```
### تثبيت netcat:
```sh
apt update && apt install netcat
```

![Screenshot 2025-04-30 171923](https://github.com/user-attachments/assets/cc3baada-d1d5-453c-b61b-2f687164cb60)

### تشغيل netcat:
```sh
nc -lk 9999
```

![image](https://github.com/user-attachments/assets/7652317b-ac7f-43bd-b5f6-18c3f069a401)

### تشغيل Spark Streaming:
```sh
spark-submit --class spark.streaming.tp22.Stream --master local stream-1.jar > out
```
![image](https://github.com/user-attachments/assets/6118bd97-213f-4057-98fd-9329f1fe04e0)























