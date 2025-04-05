# استخدم صورة بايثون الأساسية
FROM python:3.9

# تعيين دليل العمل داخل الحاوية
WORKDIR /app

# نسخ ملفات المشروع إلى الحاوية
COPY requirements.txt .  

# تحديث pip (لضمان التوافق مع المكتبات)
RUN pip install --upgrade pip  

# تثبيت التبعيات
RUN pip install -r requirements.txt  

# نسخ جميع الملفات داخل الحاوية
COPY . .  

# فتح المنفذ 8888 لاستخدام Jupyter
EXPOSE 8888  

# تشغيل Jupyter Notebook عند تشغيل الحاوية
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
