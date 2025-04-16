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

## 3. التبديل إلى قاعدة البيانات "info"
```sh
use info
```

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

## 5. استعلامات البحث
### 5.1 جلب جميع المنتجات
```sh
db.produits.find()
```
### 5.2 جلب أول منتج
```sh
db.produits.findOne()
```
### 5.3 البحث عن منتج باستخدام معرفه
```sh
db.produits.findOne({_id: ObjectId("ID_du_produit")})
```
### 5.4 البحث عن المنتجات بسعر أعلى من 13723
```sh
db.produits.find({prix: {$gt: 13723}})
```
### 5.5 البحث عن أول منتج يحتوي على "ultrabook"
```sh
db.produits.findOne({ultrabook: true})
```
### 5.6 البحث عن منتج يحتوي اسمه على "Macbook"
```sh
db.produits.findOne({nom: /Macbook/})
```
### 5.7 البحث عن المنتجات التي يبدأ اسمها بـ "Macbook"
```sh
db.produits.find({nom: /^Macbook/})
```

## 6. حذف المنتجات
### 6.1 حذف جميع منتجات "Apple"
```sh
db.produits.remove({fabriquant: "Apple"})
```
### 6.2 حذف منتج واحد فقط من "Apple"
```sh
db.produits.remove({fabriquant: "Apple"}, true)
```
