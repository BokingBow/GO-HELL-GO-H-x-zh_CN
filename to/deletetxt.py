import os

# ========== 配置 ==========
TARGET_DIR = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo\ChinesePatch_P"  # 要清理的目录
# ==========================

def delete_txt_files(root_dir):
    """删除指定目录下所有 .txt 文件"""
    deleted_count = 0
    
    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.txt'):
                file_path = os.path.join(foldername, filename)
                try:
                    os.remove(file_path)
                    print(f"  已删除: {file_path}")
                    deleted_count += 1
                except Exception as e:
                    print(f"  ❌ 删除失败: {file_path} - {e}")
    
    return deleted_count

def main():
    if not os.path.exists(TARGET_DIR):
        print(f"错误：目录不存在 - {TARGET_DIR}")
        return
    
    print(f"正在清理目录: {TARGET_DIR}")
    print("-" * 60)
    
    count = delete_txt_files(TARGET_DIR)
    
    print("-" * 60)
    print(f"✅ 清理完成！共删除 {count} 个 .txt 文件")

if __name__ == "__main__":
    main()