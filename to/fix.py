import os
import shutil

# ========== 配置 ==========
DIR_ORIGINAL = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo\Batch"   # 原始 CSV 目录（筛除后）
DIR_FIXED = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo\Fixed"       # 修复后 CSV 目录
DIR_OUTPUT = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo\Fixed_Padded"  # 补齐后的输出目录（可选，如不设则覆盖原文件）
BACKUP_ENABLED = False  # 补齐前是否备份原文件
# ==========================

def ensure_trailing_newline(file_path):
    """确保文件末尾有换行符"""
    with open(file_path, 'rb+') as f:
        f.seek(0, os.SEEK_END)
        if f.tell() == 0:
            return  # 空文件，不需要处理
        f.seek(-1, os.SEEK_END)
        last_byte = f.read(1)
        if last_byte != b'\n':
            f.write(b'\n')
            print(f"    已添加末尾换行符: {os.path.basename(file_path)}")

def preprocess_fixed_files():
    """预处理：给 Fixed 文件夹中所有 CSV 文件末尾添加换行符"""
    print("\n" + "=" * 60)
    print("预处理：添加末尾换行符")
    print("=" * 60)
    
    for root, dirs, files in os.walk(DIR_FIXED):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                ensure_trailing_newline(file_path)
    
    print("预处理完成\n")

def count_lines(file_path):
    """统计文件行数"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)

def read_lines(file_path):
    """读取文件所有行"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def write_lines(file_path, lines):
    """写入文件"""
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(lines)

def pad_lines(original_lines, fixed_lines):
    """
    用原始文件的行补齐修复文件
    返回补齐后的行列表和补齐数量
    """
    orig_len = len(original_lines)
    fixed_len = len(fixed_lines)
    
    if fixed_len <= orig_len:
        # 补齐：从原始文件末尾追加缺失的行
        padded_lines = fixed_lines + original_lines[fixed_len:orig_len]
        return padded_lines, orig_len - fixed_len
    else:
        # 修复文件更长，返回 None 和超出数量
        return None, fixed_len - orig_len

def process_file(orig_path, fixed_path, output_path=None):
    """处理单个文件"""
    orig_lines = read_lines(orig_path)
    fixed_lines = read_lines(fixed_path)
    
    orig_len = len(orig_lines)
    fixed_len = len(fixed_lines)
    
    if fixed_len == orig_len:
        print(f"  ✅ {os.path.basename(orig_path)}: 行数匹配 ({orig_len})")
        # 行数匹配，直接复制（如果输出路径不同）
        if output_path and output_path != fixed_path:
            write_lines(output_path, fixed_lines)
        return True, 0
    
    padded_lines, diff = pad_lines(orig_lines, fixed_lines)
    
    if padded_lines is not None:
        # 修复文件更短，补齐
        print(f"  ⚠️ {os.path.basename(orig_path)}: 修复文件更短 ({fixed_len} < {orig_len})，补齐 {diff} 行")
        
        # 备份原文件（可选）
        if BACKUP_ENABLED and output_path == fixed_path:
            backup_path = fixed_path + ".backup"
            shutil.copy2(fixed_path, backup_path)
            print(f"     已备份至: {backup_path}")
        
        # 写入补齐后的内容
        target_path = output_path if output_path else fixed_path
        write_lines(target_path, padded_lines)
        return True, diff
    else:
        # 修复文件更长，抛出警告
        print(f"  ❌ {os.path.basename(orig_path)}: 修复文件更长 ({fixed_len} > {orig_len})，超出 {diff} 行！需要人工检查")
        return False, diff

def main():
    # 预处理：确保 Fixed 文件夹中所有文件末尾有换行符
    preprocess_fixed_files()
    
    mismatched_files = []
    total_padded = 0
    total_longer = 0
    
    # 确保输出目录存在
    if DIR_OUTPUT:
        os.makedirs(DIR_OUTPUT, exist_ok=True)
    
    # 获取所有原始文件
    for root, dirs, files in os.walk(DIR_ORIGINAL):
        for file in files:
            if not file.endswith('.csv'):
                continue
            
            orig_path = os.path.join(root, file)
            rel_path = os.path.relpath(orig_path, DIR_ORIGINAL)
            fixed_path = os.path.join(DIR_FIXED, rel_path)
            
            # 检查修复文件是否存在
            if not os.path.exists(fixed_path):
                print(f"  ⚠️ {rel_path}: 修复文件不存在，跳过")
                continue
            
            # 确定输出路径
            if DIR_OUTPUT:
                output_path = os.path.join(DIR_OUTPUT, rel_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
            else:
                output_path = fixed_path
            
            print(f"\n📄 {rel_path}")
            success, diff = process_file(orig_path, fixed_path, output_path)
            
            if success:
                if diff > 0:
                    total_padded += diff
            else:
                mismatched_files.append((rel_path, diff))
                total_longer += diff
    
    # 输出总结报告
    print("\n" + "=" * 60)
    print("处理完成报告")
    print("=" * 60)
    
    if mismatched_files:
        print(f"\n❌ 以下文件行数更长，需要人工检查 ({len(mismatched_files)} 个):")
        for rel_path, diff in mismatched_files:
            print(f"  {rel_path}: 多出 {diff} 行")
        print("\n建议：检查这些文件是否有重复内容或导出错误")
    else:
        print("\n✅ 所有文件行数一致（已自动补齐）")
    
    if total_padded > 0:
        print(f"\n📝 共补齐 {total_padded} 行")
    
    if DIR_OUTPUT:
        print(f"\n📁 输出目录: {DIR_OUTPUT}")
    else:
        print(f"\n📁 已覆盖原修复目录文件")

if __name__ == "__main__":
    main()