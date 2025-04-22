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
![Screenshot 2025-04-22 200825](https://github.com/user-attachments/assets/7a2710bd-4c47-435a-8328-febb598e5b45)

## إنشاء شبكة Docker مخصصة
```sh
docker network create bigdata_network
```
![Screenshot 2025-04-22 201306 - Copy](https://github.com/user-attachments/assets/0b3c019c-f91e-45af-9b2e-0c91d3751b91)

## تشغيل الحاويات وربطها بالشبكة
```sh
docker run -d --name bigdata1 --network bigdata_network -p 8881:8888 ahmedghayout/bigdata:1
docker run -d --name bigdata2 --network bigdata_network -p 8882:8888 ahmedghayout/bigdata:1
docker run -d --name bigdata3 --network bigdata_network -p 8883:8888 ahmedghayout/bigdata:1
```
![Screenshot 2025-04-22 201306 - Copy](https://github.com/user-attachments/assets/76b1924d-fa42-4641-8579-85ec3d78ceb8)
![Screenshot 2025-04-22 202215](https://github.com/user-attachments/assets/ed352a29-dd65-4bd8-b6fc-7120d4fcc104)


##  الدخول إلى الحاوية bigdata1
```sh
docker exec -it bigdata1 /bin/bash
```
## تحديث النظام وتثبيت أمر ping داخل الحاوية
```sh
apt update && apt install -y iputils-ping
```
![Screenshot 2025-04-22 202014](https://github.com/user-attachments/assets/6fc33728-181b-415e-a3c9-dbeb821d5fa4)

وتطبيق الامر على باقي الحاويات

## اختبار الاتصال بين الحاويتين
```sh
ping bigdata2
```
![Screenshot 2025-04-22 202141](https://github.com/user-attachments/assets/dc34a1f5-cfd5-4f17-b42e-ddc58fa77e21)








