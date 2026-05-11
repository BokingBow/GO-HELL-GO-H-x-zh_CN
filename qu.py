import os
import shutil

# ========== 配置 ==========
SOURCE_DIR = r"F:\Reason\Origin\GO HELL GO 素材\ChinesePatch_P"      # _NEW 文件所在目录
OUTPUT_DIR = r"F:\Reason\Origin\GO HELL GO 素材\ChineseTest_P"   # 取出并重命名后的输出目录
# ==========================

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(root, SOURCE_DIR)
            
            if file.endswith('_NEW.uasset'):
                # 重命名：xxx_NEW.uasset -> xxx.uasset
                new_name = file.replace('_NEW.uasset', '.uasset')
                dest_dir = os.path.join(OUTPUT_DIR, rel_path)
                os.makedirs(dest_dir, exist_ok=True)
                dest_path = os.path.join(dest_dir, new_name)
                shutil.copy2(src_path, dest_path)
                print(f"✅ {file} -> {new_name}")
                
            elif file.endswith('_NEW.uexp'):
                # 重命名：xxx_NEW.uexp -> xxx.uexp
                new_name = file.replace('_NEW.uexp', '.uexp')
                dest_dir = os.path.join(OUTPUT_DIR, rel_path)
                os.makedirs(dest_dir, exist_ok=True)
                dest_path = os.path.join(dest_dir, new_name)
                shutil.copy2(src_path, dest_path)
                print(f"✅ {file} -> {new_name}")

    print(f"\n完成！输出目录: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()