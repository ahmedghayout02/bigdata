import pandas as pd
import dask.dataframe as dd
import time
import os
import psutil
import pyarrow as pa
import pyarrow.parquet as pq
from dask.distributed import Client
import sys
import gc


sys.stdout.reconfigure(encoding='utf-8')

# 📌 قياس استهلاك الذاكرة

def measure_memory(repeats=10, delay=0.5):  # زيادة التكرارات والتأخير
    """قياس الذاكرة بدقة بأخذ متوسط عدة قراءات"""
    readings = []
    process = psutil.Process(os.getpid())
    for _ in range(repeats):
        mem = process.memory_info().rss / (1024 ** 2)  # بالميجابايت
        readings.append(mem)
        time.sleep(delay)
    return max(readings)  # حساب المتوسط


# 🔄 تحويل CSV إلى Parquet مع الضغط
def convert_to_parquet(input_file: str, output_file: str, chunk_size: int = 5000) -> bool:
    """يحوّل الملف CSV إلى Parquet مع معالجة الأخطاء"""
    if not os.path.exists(output_file):
        print(f"🔄 جاري تحويل {os.path.basename(input_file)} إلى Parquet...")
        writer = None
        try:
            for i, chunk in enumerate(pd.read_csv(input_file, chunksize=chunk_size, low_memory=False)):
                chunk = chunk.apply(lambda x: x.astype(str) if x.dtype == object else x)
                
                table = pa.Table.from_pandas(chunk)
                
                if not writer:
                    writer = pq.ParquetWriter(output_file, schema=table.schema, compression='snappy', use_dictionary=True)
                
                writer.write_table(table)
                print(f"✅ تم تحويل الجزء {i+1}")
            
            print(f"🎉 التحويل إلى Parquet اكتمل بنجاح! الملف: {output_file}")
            return True
        except Exception as e:
            print(f"❌ فشل التحويل: {str(e)}")
            if writer:
                writer.close()
                os.remove(output_file)
            return False
        finally:
            if writer:
                writer.close()
    else:
        print(f"⚠️ الملف {output_file} موجود مسبقًا")
        return True

# 📊 التحليل باستخدام Pandas (تجزئة)
def pandas_chunking(file_name, chunk_size=10000):
    start_mem = measure_memory()
    start_time = time.time()

    total_sum = {}
    total_count = {}

    try:
        for chunk in pd.read_csv(file_name, chunksize=chunk_size, low_memory=False):
            grouped = chunk.groupby("event_type")["price"]
            for name, group in grouped:
                total_sum[name] = total_sum.get(name, 0) + group.sum()
                total_count[name] = total_count.get(name, 0) + group.count()

        final_result = {name: total_sum[name] / total_count[name] for name in total_sum}
        
        return {
            'Method': 'Pandas Chunking',
            'Time (Seconds)': round(time.time() - start_time, 2),
            'Memory (MB)': round(measure_memory() - start_mem, 2)
        }
    except Exception as e:
        print(f"❌ فشل في Pandas Chunking: {e}")
        return {'Method': 'Pandas Chunking', 'Time (Seconds)': None, 'Memory (MB)': None}

# 🏎️ التحليل باستخدام Dask

def dask_processing(file_name):
    client = None
    try:
        # ⚙️ ضبط إعدادات العمال لتحميل أكبر للذاكرة
        client = Client(n_workers=1,threads_per_worker=1, memory_target_fraction=0.9,memory_spill_fraction=0.9)
        
        # 📦 تحميل البيانات مع الإبقاء عليها في الذاكرة
        start_mem = measure_memory(repeats=10, delay=0.5)
        start_time = time.time()
        
        df = dd.read_csv(file_name,low_memory=False,blocksize='8MB').persist()  # إجبار التحميل في الذاكرة
        
        # 🔄 عمليات متكررة على البيانات
        for _ in range(3):  # تكرار العمليات لزيادة الحمل
            df['price'] = df['price'].astype(float)
            df['discounted_price'] = df['price'] * 0.8  # عمليات حسابية إضافية
            
        # 📊 عمليات تجميع معقدة
        grouped = df.groupby("event_type").agg(avg_price=('price', 'mean'),max_price=('price', 'max'),min_price=('price', 'min')).persist()  # الإبقاء على النتائج في الذاكرة
        
        # ⏳ تأخير قياس الذاكرة النهائي
        time.sleep(10)  # الانتظار لضمان استقرار القياس
        end_mem = measure_memory(repeats=20, delay=1)
        
        return {
            'Method': 'Dask Processing','Time (Seconds)': round(time.time() - start_time, 2),'Memory (MB)': round(end_mem - start_mem, 2)}
    except Exception as e:
        print(f"❌ فشل في Dask Processing: {e}")
        return {'Method': 'Dask Processing', 'Time (Seconds)': None, 'Memory (MB)': None}
    finally:
        if client:
            client.close()

# 📉 التحليل باستخدام Parquet
def parquet_compression(file_name):
    start_mem = measure_memory()
    start_time = time.time()

    try:
        # قراءة البيانات على دفعات
        parquet_file = pq.ParquetFile(file_name)
        total_sum = {}
        total_count = {}
        
        for batch in parquet_file.iter_batches(columns=['event_type', 'price'], batch_size=100000):
            df_batch = batch.to_pandas()
            grouped = df_batch.groupby("event_type")["price"]
            for name, group in grouped:
                total_sum[name] = total_sum.get(name, 0) + group.sum()
                total_count[name] = total_count.get(name, 0) + group.count()
        
        avg_price = {k: total_sum[k]/total_count[k] for k in total_sum}
        
        return {
            'Method': 'Parquet Compression',
            'Time (Seconds)': round(time.time() - start_time, 2),
            'Memory (MB)': round(measure_memory() - start_mem, 2)
        }
    except Exception as e:
        print(f"❌ فشل قراءة Parquet: {e}")
        return {'Method': 'Parquet Compression', 'Time (Seconds)': None, 'Memory (MB)': None}

# 🔬 مقارنة النتائج وحفظها
def compare_results(results, output_file="comparison_results.csv"):
    df = pd.DataFrame(results).dropna()
    
    print("\n🔍 **نتائج المقارنة:**")
    if not df.empty:
        print(f"🚀 الأسرع: {df.loc[df['Time (Seconds)'].idxmin(), 'Method']}")
        print(f"💾 الأقل استهلاكًا للذاكرة: {df.loc[df['Memory (MB)'].idxmin(), 'Method']}")
    else:
        print("⚠️ لا توجد نتائج صالحة للمقارنة!")
    
    print("\n📊 **جدول النتائج:**")
    print(df.to_string(index=False))
    
    df.to_csv(output_file, index=False)
    print(f"\n✅ تم حفظ النتائج في: {output_file}")

# 🏁 التنفيذ الرئيسي
if __name__ == "__main__":
    base_path = r"G:\tpS2\big data\tp2"
    input_csv = os.path.join(base_path, "2019-Nov.csv")
    output_parquet = os.path.join(base_path, "2019-Nov.parquet")
    
    # ✅ تحويل CSV إلى Parquet
    success = convert_to_parquet(input_csv, output_parquet)
    
    if success:
        # 🏎️ تشغيل التحليلات
        results = [
            pandas_chunking(input_csv),
            dask_processing(input_csv),
            parquet_compression(output_parquet)
        ]
        # 📊 عرض النتائج
        compare_results(results)
    else:
        print("❌ فشل في تحويل الملف، يرجى التحقق من البيانات!")
