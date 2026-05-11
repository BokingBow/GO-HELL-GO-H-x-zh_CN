import os
import re

# ========== 配置 ==========
INPUT_DIR = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo\Batch3"   # Translator++ 导出的问题文件目录
OUTPUT_DIR = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo\Fixed"              # 修复后的输出目录
ORIGINAL_DIR = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo\Batch"            # 筛除前的原始 CSV 目录
# ==========================

def fix_csv_file(input_path, output_path, original_path):
    """修复单个 CSV 文件"""
    # 读取所有行
    with open(input_path, 'r', encoding='utf-8') as f:
        input_lines = f.readlines()
    
    with open(original_path, 'r', encoding='utf-8') as f:
        original_lines = f.readlines()
    
    # 确保行数一致
    if len(input_lines) != len(original_lines):
        print(f"  警告：行数不一致！输入 {len(input_lines)}，原始 {len(original_lines)}")
        min_lines = min(len(input_lines), len(original_lines))
    else:
        min_lines = len(input_lines)
    
    output_lines = []
    for i in range(min_lines):
        input_line = input_lines[i].rstrip('\n')
        original_line = original_lines[i].rstrip('\n')
        
        # 情况1：空行（"",""）→ 恢复原始内容
        if input_line == '"",""':
            output_lines.append(original_line)
        # 情况2：有内容的行 → 去除双引号
        elif input_line.strip():
            # 匹配 "Key","Value" 格式，去除首尾双引号
            # 支持可能存在的空格（如 " Key"," Value"）
            match = re.match(r'"([^"]*)"\s*,\s*"([^"]*)"', input_line)
            if match:
                key = match.group(1)
                value = match.group(2)
                output_lines.append(f"{key},{value}")
            else:
                # 如果匹配失败（不应该发生），保持原样
                output_lines.append(input_line)
        # 情况3：空行（理论上不会走到这里，因为空行已经被情况1捕获）
        else:
            output_lines.append(original_line)
    
    # 写入输出文件
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(output_lines))
    
    print(f"  处理完成: {os.path.basename(input_path)}")

def main():
    # 遍历所有 CSV 文件
    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.endswith('.csv'):
                input_path = os.path.join(root, file)
                
                # 计算相对路径
                rel_path = os.path.relpath(input_path, INPUT_DIR)
                
                output_path = os.path.join(OUTPUT_DIR, rel_path)
                original_path = os.path.join(ORIGINAL_DIR, rel_path)
                
                # 检查原始文件是否存在
                if not os.path.exists(original_path):
                    print(f"跳过 {rel_path}：原始文件不存在")
                    continue
                
                print(f"处理: {rel_path}")
                fix_csv_file(input_path, output_path, original_path)
    
    print("\n全部处理完成！")

if __name__ == "__main__":
    main()