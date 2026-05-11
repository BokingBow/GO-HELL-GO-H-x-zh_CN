import os
import csv
import sys

# ========== 配置参数 ==========
INPUT_ROOT = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo\Extract"      # 存放 .txt 文件的上层目录（由之前的脚本生成）
OUTPUT_ROOT = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo\Batch"       # CSV 文件输出目录
# =============================

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"[创建目录] {path}")

def convert_txt_to_csv(txt_path, csv_path):
    """
    将单个 .txt 文件（键=值格式）转换为 .csv 文件
    支持：
      - 空行跳过
      - 注释行跳过（行首为 # 或 ;）
      - 等号分隔
    """
    rows = []
    
    with open(txt_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.rstrip("\n\r")
            
            # 跳过空行
            if not line.strip():
                continue
            
            # 跳过注释行（如果以 # 或 ; 开头）
            if line.strip().startswith("#") or line.strip().startswith(";"):
                continue
            
            # 查找第一个等号的位置
            eq_pos = line.find("=")
            if eq_pos == -1:
                # 没有等号的行，整行作为键，值为空
                key = line
                value = ""
                print(f"  [警告] 无等号行 {txt_path}:{line_num} -> 整行作为键")
            else:
                key = line[:eq_pos]
                value = line[eq_pos + 1:] if eq_pos + 1 < len(line) else ""
            
            rows.append([key, value])
    
    if not rows:
        print(f"  [跳过] 无有效数据: {txt_path}")
        return False
    
    # 写入 CSV
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Key", "Value"])   # 写入表头
        writer.writerows(rows)
    
    print(f"  [转换] {os.path.basename(txt_path)} -> {len(rows)} 行")
    return True

def process_directory(input_dir, output_dir):
    """递归处理 input_dir 下所有 .txt 文件"""
    txt_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".txt"):
                txt_files.append(os.path.join(root, file))
    
    if not txt_files:
        print(f"[错误] 在 {input_dir} 下未找到任何 .txt 文件")
        return 0, 0
    
    print(f"共找到 {len(txt_files)} 个 .txt 文件")
    print("-" * 50)
    
    success = 0
    fail = 0
    
    for txt_path in txt_files:
        # 计算相对路径，保持目录结构
        rel_path = os.path.relpath(txt_path, input_dir)
        csv_path = os.path.join(output_dir, rel_path).replace(".txt", ".csv")
        
        ensure_dir(os.path.dirname(csv_path))
        
        if convert_txt_to_csv(txt_path, csv_path):
            success += 1
        else:
            fail += 1
    
    return success, fail

def main():
    if not os.path.exists(INPUT_ROOT):
        print(f"[错误] 输入目录不存在: {INPUT_ROOT}")
        sys.exit(1)
    
    ensure_dir(OUTPUT_ROOT)
    
    success, fail = process_directory(INPUT_ROOT, OUTPUT_ROOT)
    
    print("-" * 50)
    print(f"\n===== 转换完成 =====")
    print(f"成功: {success}  失败: {fail}")

if __name__ == "__main__":
    main()