import pandas as pd

# โหลดข้อมูล
file_path = "jil.csv"  # เปลี่ยนเป็นพาธไฟล์ที่ถูกต้อง
df = pd.read_csv(file_path)

# ตรวจหาค่า Missing Values และเติมค่าที่เหมาะสม
df.fillna(method='ffill', inplace=True)  # ใช้วิธี forward fill แทนค่าที่หายไป

# ลบค่าที่ซ้ำกัน
df.drop_duplicates(inplace=True)

# ตรวจหาค่าผิดพลาด (เช่น ค่าเป็นลบในคอลัมน์ที่ควรเป็นค่าบวก)
for col in df.select_dtypes(include=['number']).columns:
    df = df[df[col] >= 0]

# แปลงค่าคอลัมน์ CAEC และ CALC
mapping = {"no": 0, "Sometimes": 1, "Frequently": 2, "Always": 3}
if "CAEC" in df.columns:
    df["CAEC"] = df["CAEC"].map(mapping)
if "CALC" in df.columns:
    df["CALC"] = df["CALC"].map(mapping)

# แปลงค่าคอลัมน์ family_history_with_overweight
family_mapping = {"no": 0, "yes": 1}
if "family_history_with_overweight" in df.columns:
    df["family_history_with_overweight"] = df["family_history_with_overweight"].map(family_mapping)

# ปัดค่าเฉพาะคอลัมน์ Height เป็นทศนิยม 2 ตำแหน่ง
if "Height" in df.columns:
    df["Height"] = df["Height"].round(2)

# ปัดค่าคอลัมน์ตัวเลขอื่น ๆ เป็นจำนวนเต็ม (ปัดแบบคณิตศาสตร์)
num_cols = df.select_dtypes(include=['number']).columns.difference(["Height"])
df[num_cols] = df[num_cols].round().astype(int)

# บันทึกไฟล์ที่ทำความสะอาดแล้วเป็น Excel
output_path = "cleaned_data_rounded.xlsx"
df.to_excel(output_path, index=False)

# แสดงผลข้อมูลที่ถูกทำความสะอาดแล้ว
print(df.head())
print(f"\nข้อมูลมีทั้งหมด {df.shape[0]} แถว และ {df.shape[1]} คอลัมน์")
print(f"บันทึกไฟล์ที่: {output_path}")