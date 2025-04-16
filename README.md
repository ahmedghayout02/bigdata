# MongoDB Commands Guide

## 1. تشغيل MongoDB Server
```sh
C:\MongoDB\bin\mongod.exe
```
![image](https://github.com/user-attachments/assets/f8bae73a-0fc3-4db3-9175-89bf7077aab3)


## 2. تشغيل Mongo Shell
```sh
C:\MongoDB\bin\mongo.exe
```
![image](https://github.com/user-attachments/assets/8bbea0f0-dcde-467c-8a7b-0d5233a06d4c)


## 3. التبديل إلى قاعدة البيانات "info"
```sh
use info
```
![image](https://github.com/user-attachments/assets/20bcf00f-2ae3-4e6c-801e-b1e9538aec6b)


## 4. إدراج مستندات في مجموعة "produits"
```sh
db.produits.insert({
    nom: "Macbook Pro",
    fabriquant: "Apple",
    options: ["Intel Core i5", "Retina Display", "Long life battery"]
})

db.produits.insert({
    nom: "Macbook Air",
    fabriquant: "Apple",
    prix: 125794.73,
    ultrabook: true,
    options: ["Intel Core i7", "SSD", "Long life battery"]
})

db.produits.insert({
    nom: "Thinkpad X230",
    fabriquant: "Lenovo",
    prix: 114358.74,
    ultrabook: true,
    options: ["Intel Core i5", "SSD", "Long life battery"]
})
```
![image](https://github.com/user-attachments/assets/6e050ddd-7ac8-44b7-943e-c6b460386856)


## 5. استعلامات البحث
### 5.1 جلب جميع المنتجات
```sh
db.produits.find()
```
![image](https://github.com/user-attachments/assets/a50895c0-3242-4356-9791-8f6736ce271e)

### 5.2 جلب أول منتج
```sh
db.produits.findOne()
```
![image](https://github.com/user-attachments/assets/938944a7-b117-42e1-a744-b911510c8926)

### 5.3 البحث عن منتج باستخدام معرفه
```sh
db.produits.findOne({_id: ObjectId("ID_du_produit")})
```
![image](https://github.com/user-attachments/assets/9b66e2ff-c97c-4773-9e68-15d3ac8addb3)

### 5.4 البحث عن المنتجات بسعر أعلى من 13723
```sh
db.produits.find({prix: {$gt: 13723}})
```
![image](https://github.com/user-attachments/assets/e89756b9-faae-4378-b9ee-2eca57030f43)

### 5.5 البحث عن أول منتج يحتوي على "ultrabook"
```sh
db.produits.findOne({ultrabook: true})
```
![image](https://github.com/user-attachments/assets/2a8b82d1-be51-4523-99cc-04d63e3c7a13)

### 5.6 البحث عن منتج يحتوي اسمه على "Macbook"
```sh
db.produits.findOne({nom: /Macbook/})
```
![image](https://github.com/user-attachments/assets/5bb4ef96-914b-45db-a41b-c27bcb770729)

## 6. حذف المنتجات
### 6.1 حذف جميع منتجات "Apple"
```sh
db.produits.remove({fabriquant: "Apple"})
```
![image](https://github.com/user-attachments/assets/5a2b53ee-25dd-4a5d-93ab-8773f8907922)

### 6.2 حذف منتج واحد فقط من "Apple"
```sh
db.produits.remove({fabriquant: "Apple"}, true)
```
![image](https://github.com/user-attachments/assets/62ea2855-581f-4b7a-9b17-cef6ec69f58b)

