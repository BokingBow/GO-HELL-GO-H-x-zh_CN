import os
import csv

INPUT_ROOT = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo\Fixed_Padded"      # 编辑好的 CSV 目录
OUTPUT_ROOT = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo\Endnd"     # 转换回 .txt 的输出目录

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def convert_csv_to_txt(csv_path, txt_path):
    rows = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)  # 跳过表头 Key, Value
        for row in reader:
            if len(row) >= 2:
                key = row[0]
                value = row[1]
                rows.append(f"{key}={value}")
    
    if not rows:
        return False
    
    with open(txt_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(rows))
    
    return True

def process_directory(input_dir, output_dir):
    csv_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))
    
    for csv_path in csv_files:
        rel_path = os.path.relpath(csv_path, input_dir)
        txt_path = os.path.join(output_dir, rel_path).replace(".csv", ".txt")
        ensure_dir(os.path.dirname(txt_path))
        
        if convert_csv_to_txt(csv_path, txt_path):
            print(f"[转换] {csv_path} -> {txt_path}")

if __name__ == "__main__":
    ensure_dir(OUTPUT_ROOT)
    process_directory(INPUT_ROOT, OUTPUT_ROOT)
    print("===== 转换完成 =====")