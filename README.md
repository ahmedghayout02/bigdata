<h2 align="center">
دليل عملي لتثبيت وتشغيل مشروع معالجة بيانات باستخدام Hadoop وMapReduce عبر Docker، بالإضافة إلى تنفيذ مثال عملي يسمى WordCount.
</h2>


## أولاً: إعداد بيئة العمل
### 1. المتطلبات الأساسية:
Docker

Visual Studio Code

Java JDK 8

Maven



## ثانياً: تشغيل Hadoop Cluster باستخدام Docke
### 2. إنشاء شبكة Docker خاصة بـ Hadoop
```sh 
docker network create hadoop
```
![Screenshot 2025-04-23 001732](https://github.com/user-attachments/assets/e8a5d8c3-8812-4a9f-bb5d-b099046bd70c)

هذه الشبكة ستربط بين الـ Master والـ Workers.

### 2.2. تشغيل الـ Master (Namenode)
```sh
docker run -itd --net=hadoop -p 9870:9870 -p 8088:8088 -p 7077:7077 -p 16010:16010 --name hadoop-master --hostname hadoop-master liliasfaxi/hadoop-cluster:latest
```
![Screenshot 2025-04-23 001732](https://github.com/user-attachments/assets/371e71b3-0fc9-4f11-bb08-fe2d3a2dd08e)

هذا الحاوية ستكون مسؤولة عن إدارة الـ Namenode و ResourceManager.

``` sh
docker run -itd -p 8040:8042 --net=hadoop --name hadoop-worker1 --hostname hadoop-worker1 liliasfaxi/hadoop-cluster:latest

docker run -itd -p 8041:8042 --net=hadoop --name hadoop-worker2 --hostname hadoop-worker2 liliasfaxi/hadoop-cluster:latest
```
كل Worker سيكون بمثابة Datanode و NodeManager.
![Screenshot 2025-04-23 003749](https://github.com/user-attachments/assets/679055ee-3347-4e7e-bb2f-4c1b4babefd0)


## ثالثاً: تشغيل Hadoop داخل الـ Containers
### الدخول إلى الـ Master:
```sh
docker exec -it hadoop-master bash
```
ثم تشغيل Hadoop:
```sh
./start-hadoop.sh
```
هذا الأمر يقوم بتشغيل كل مكونات HDFS و YARN داخل الحاويات.
![Screenshot 2025-04-26 190754](https://github.com/user-attachments/assets/df47010b-fb69-42bc-9fa4-7fa8be1c8202)

## رابعاً: رفع بيانات إلى HDFS
### 4.1. إنشاء مجلد input داخل HDFS:
```sh
hdfs dfs -mkdir -p /user/root/input
```
### 4.2. رفع ملف البيانات (مثلاً purchases.txt):
```sh
hdfs dfs -put purchases.txt /user/root/input
```
![437691109-e1a36270-ff00-4654-a51a-5c69bd74d9ab](https://github.com/user-attachments/assets/b5a47e1a-966b-4dba-81a3-bfce070feea1)

## خامساً: تنفيذ MapReduce - مثال WordCount
### 5.1. إنشاء مشروع Maven في VS Code
![Screenshot 2025-04-23 005254](https://github.com/user-attachments/assets/a8ce83ea-33b1-4c04-b294-7ef28d9f767b)
### 5.2. تعديل ملف pom.xml لإضافة مكتبات Hadoop
```sh
<dependencies>
  <dependency>
    <groupId>org.apache.hadoop</groupId>
    <artifactId>hadoop-common</artifactId>
    <version>3.3.6</version>
  </dependency>
  <dependency>
    <groupId>org.apache.hadoop</groupId>
    <artifactId>hadoop-mapreduce-client-core</artifactId>
    <version>3.3.6</version>
  </dependency>
  <dependency>
    <groupId>org.apache.hadoop</groupId>
    <artifactId>hadoop-hdfs</artifactId>
    <version>3.3.6</version>
  </dependency>
  <dependency>
    <groupId>org.apache.hadoop</groupId>
    <artifactId>hadoop-mapreduce-client-jobclient</artifactId>
    <version>3.3.6</version>
  </dependency>
</dependencies>
```
### 5.3. إنشاء كلاس Mapper (TokenizerMapper)
```sh
public class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable> {
    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();

    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
        StringTokenizer itr = new StringTokenizer(value.toString());
        while (itr.hasMoreTokens()) {
            word.set(itr.nextToken());
            context.write(word, one);
        }
    }
}
```
### 5.4. إنشاء كلاس Reducer (IntSumReducer)
```sh
public class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
        int sum = 0;
        for (IntWritable val : values) {
            sum += val.get();
        }
        result.set(sum);
        context.write(key, result);
    }
}
```
### 5.5. كلاس التشغيل الرئيسي (WordCount)
```sh
public class WordCount {
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(WordCount.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```
![image](https://github.com/user-attachments/assets/b165af35-106c-4e57-a703-209b2a5d6280)

## سادساً: إنشاء ملف JAR
### 6.1. إضافة Plugin في pom.xml لتجميع كل التبعيات
```sh
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-assembly-plugin</artifactId>
    <version>3.6.0</version>
    <configuration>
        <archive>
            <manifest>
                <mainClass>hadoop.mapreduce.tp1.WordCount</mainClass>
            </manifest>
        </archive>
        <descriptorRefs>
            <descriptorRef>jar-with-dependencies</descriptorRef>
        </descriptorRefs>
    </configuration>
    <executions>
        <execution>
            <id>make-assembly</id>
            <phase>package</phase>
            <goals>
                <goal>single</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```
### 6.2. بناء المشروع:
```sh
mvn clean compile assembly:single
```
سينتج لك ملف JAR جاهز مع كل التبعيات.
![Screenshot 2025-04-23 115727](https://github.com/user-attachments/assets/1bd59be8-ddb6-4178-8ea5-8dccf9cdacc7)
![Screenshot 2025-04-23 120122](https://github.com/user-attachments/assets/5f019d98-8901-48b3-b160-2f8abdd2967b)



## سابعاً: تشغيل Job MapReduce في الـ Cluster
```sh
docker cp target/wordcount-1.0-SNAPSHOT-jar-with-dependencies.jar hadoop-master:/root/wordcount.jar
```
![image](https://github.com/user-attachments/assets/19a4edf4-b060-4cf7-aade-91e3ce3fb200)

### 7.2. تشغيل البرنامج داخل الحاوية:
```sh
docker exec -it hadoop-master bash
hadoop jar /root/wordcount.jar /user/root/input /user/root/output
```
## ثامناً: عرض نتائج المعالجة
### 8.1. عرض نتائج WordCount:
```sh
hdfs dfs -cat /user/root/output/part-r-00000
```
![image](https://github.com/user-attachments/assets/5b8b11a6-d661-4d74-a854-093769d712e3)











