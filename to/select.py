import os
import csv

# ========== 配置 ==========
INPUT_DIR = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo\Batch"      # 原始 CSV 所在目录
OUTPUT_DIR = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo\Batch2"     # 空行版本输出目录
# =========================

def should_blank_line(line):
    """判断是否需要替换为空行"""
    if not line.strip():
        return False
    # 检查是否以控制关键词开头
    if line.startswith('Arg') or line.startswith('Command') or \
       line.startswith('PageCtrl'):
        return True
    return False

def process_file(input_path, output_path):
    """处理单个 CSV 文件"""
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if should_blank_line(line):
            new_lines.append(',\n')   # 空行（保留逗号作为占位符）
        else:
            new_lines.append(line)
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        f.writelines(new_lines)
    
    print(f"处理: {input_path} -> {output_path}")

def main():
    # 遍历所有 CSV 文件
    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.endswith('.csv'):
                input_path = os.path.join(root, file)
                # 计算相对路径，保持目录结构
                rel_path = os.path.relpath(input_path, INPUT_DIR)
                output_path = os.path.join(OUTPUT_DIR, rel_path)
                process_file(input_path, output_path)

if __name__ == "__main__":
    main()