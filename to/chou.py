import os
import shutil

# ========== 配置 ==========
TXT_DIR = r"F:\Reason\Origin\GO HELL GO 素材\to\Endnd"   # 翻译后的 .txt 目录
UASSET_DIR = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo"        # 包含 .uasset/.uexp 的目录
OUTPUT_DIR = r"F:\Reason\Origin\GO HELL GO 素材\ChinesePatch_P\gohellgo"  # 打包用的临时文件夹
# ==========================

def main():
    # 统计
    copied_uasset = 0
    copied_uexp = 0
    
    # 遍历所有 .txt 文件
    for root, dirs, files in os.walk(TXT_DIR):
        for file in files:
            if not file.endswith('.txt'):
                continue
            
            # 获取文件名（不含扩展名）
            basename = file[:-11]  # 去掉 .txt
            
            # 构建源文件路径（在 UASSET_DIR 中查找）
            # 需要保持相对路径结构
            rel_path = os.path.relpath(root, TXT_DIR)
            uasset_src = os.path.join(UASSET_DIR, rel_path, f"{basename}.uasset")
            uexp_src = os.path.join(UASSET_DIR, rel_path, f"{basename}.uexp")
            
            # 构建目标路径
            uasset_dst = os.path.join(OUTPUT_DIR, rel_path, f"{basename}.uasset")
            uexp_dst = os.path.join(OUTPUT_DIR, rel_path, f"{basename}.uexp")
            
            # 确保目标目录存在
            os.makedirs(os.path.dirname(uasset_dst), exist_ok=True)
            
            # 复制 .uasset（必须存在）
            if os.path.exists(uasset_src):
                shutil.copy2(uasset_src, uasset_dst)
                print(f"  ✅ 复制: {rel_path}/{basename}.uasset")
                copied_uasset += 1
            else:
                print(f"  ⚠️ 缺失: {rel_path}/{basename}.uasset")
            
            # 复制 .uexp（可能不存在，某些资源没有 .uexp）
            if os.path.exists(uexp_src):
                shutil.copy2(uexp_src, uexp_dst)
                print(f"  ✅ 复制: {rel_path}/{basename}.uexp")
                copied_uexp += 1
            # .uexp 不存在时不报错，正常情况
    
    print("\n" + "=" * 60)
    print("筛选完成报告")
    print("=" * 60)
    print(f"复制 .uasset: {copied_uasset} 个")
    print(f"复制 .uexp: {copied_uexp} 个")
    print(f"输出目录: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()