# 🔐 تسجيل الدخول إلى Docker Hub
docker login
# هذا الأمر يسمح لك بتسجيل الدخول إلى حساب Docker الخاص بك حتى تتمكن من رفع الصور (images).

# 🛠️ بناء الصورة (image) من ملف Dockerfile الحالي
docker build -t bigdata .
# ينشئ صورة جديدة باسم "bigdata" من محتوى المجلد الحالي (يجب أن يحتوي على Dockerfile).

# 🏷️ عمل tag للصورة باسم المستخدم ونسخة محددة
docker tag bigdata ahmedghayout/bigdata:1
# يُعطي اسمًا جديدًا للصورة يتضمن اسم المستخدم على Docker Hub والنسخة (tag 1).

# 🚀 رفع الصورة إلى Docker Hub
docker push ahmedghayout/bigdata:1
# يرفع الصورة إلى مستودع Docker Hub الخاص بك (ahmedghayout).

# 🌐 إنشاء شبكة Docker مخصصة
docker network create bigdata_network
# ينشئ شبكة Docker مخصصة تُستخدم لربط الحاويات معًا.

# 🐳 تشغيل أول حاوية وربطها بالشبكة على منفذ 8881
docker run -d --name bigdata1 --network bigdata_network -p 8881:8888 ahmedghayout/bigdata:1

# 🐳 تشغيل ثاني حاوية وربطها بالشبكة على منفذ 8882
docker run -d --name bigdata2 --network bigdata_network -p 8882:8888 ahmedghayout/bigdata:1

# 🐳 تشغيل ثالث حاوية وربطها بالشبكة على منفذ 8883
docker run -d --name bigdata3 --network bigdata_network -p 8883:8888 ahmedghayout/bigdata:1

# 🖥️ الدخول إلى الحاوية الأولى bigdata1
docker exec -it bigdata1 /bin/bash

# 🔄 تحديث الحزم وتثبيت أداة ping داخل الحاوية
apt update && apt install -y iputils-ping

# 📡 اختبار الاتصال بين الحاويات داخل الشبكة
ping bigdata2
# يفحص إذا كانت الحاوية "bigdata1" قادرة على التواصل مع الحاوية "bigdata2".
