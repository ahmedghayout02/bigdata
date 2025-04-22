## تسجيل الدخول إلى Docker Hub 
```sh
docker login
```
![Screenshot 2025-04-22 200634](https://github.com/user-attachments/assets/63615e13-f5d7-4574-a9e8-54c1e6ae93fd)

##  بناء صورة Docker من ملف Dockerfile
```sh
docker build -t bigdata .
```
## إضافة وسم جديد للصورة لربطها بحسابك على Docker Hub
```sh
docker tag bigdata ahmedghayout/bigdata:1
```
## رفع الصورة إلى Docker Hub
```sh
docker push ahmedghayout/bigdata:1
```
## تحميل الصورة من Docker Hub
```sh
docker pull ahmedghayout/bigdata:1
```
## إنشاء شبكة Docker مخصصة
```sh
docker network create bigdata_network
```
## تشغيل الحاويات وربطها بالشبكة
```sh
docker run -d --name bigdata1 --network bigdata_network -p 8881:8888 ahmedghayout/bigdata:1
docker run -d --name bigdata2 --network bigdata_network -p 8882:8888 ahmedghayout/bigdata:1
docker run -d --name bigdata3 --network bigdata_network -p 8883:8888 ahmedghayout/bigdata:1
```
##  الدخول إلى الحاوية bigdata1
```sh
docker exec -it bigdata1 /bin/bash
```
## تحديث النظام وتثبيت أمر ping داخل الحاوية
```sh
apt update && apt install -y iputils-ping
```
وتطبيق الامر على باقي الحاويات

## اختبار الاتصال بين الحاويتين
```sh
ping bigdata2
```







