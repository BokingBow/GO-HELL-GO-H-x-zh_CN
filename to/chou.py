import os
import shutil

# ========== 配置 ==========
TXT_DIR = r"F:\Reason\Origin\GO HELL GO 素材\1_4\Extract"   # 翻译后的 .txt 目录
UASSET_DIR = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo_1_4"        # 包含 .uasset/.uexp 的目录
OUTPUT_DIR = r"F:\Reason\Origin\GO HELL GO 素材\ChinesePatch_P\gohellgo"  # 打包用的临时文件夹
OVERWRITE = False  # 是否覆盖已存在的文件，设为 True 则覆盖，False 则跳过
# ==========================

def should_skip(dst_path):
    """检查目标文件是否已存在，如果存在则跳过（除非 OVERWRITE 为 True）"""
    if OVERWRITE:
        return False  # 覆盖模式：不跳过
    return os.path.exists(dst_path)

def main():
    # 统计
    copied_uasset = 0
    copied_uexp = 0
    copied_txt = 0
    skipped_uasset = 0
    skipped_uexp = 0
    skipped_txt = 0
    
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
            
            # ========== 处理 .txt 文件 ==========
            txt_src = os.path.join(root, file)
            txt_dst = os.path.join(OUTPUT_DIR, rel_path, file)
            
            # 确保目标目录存在
            os.makedirs(os.path.dirname(txt_dst), exist_ok=True)
            
            if should_skip(txt_dst):
                print(f"  ⏭️ 跳过（已存在）: {rel_path}/{file}")
                skipped_txt += 1
            else:
                shutil.copy2(txt_src, txt_dst)
                print(f"  📄 复制 txt: {rel_path}/{file}")
                copied_txt += 1
            
            # ========== 处理 .uasset 文件 ==========
            uasset_src = os.path.join(UASSET_DIR, rel_path, f"{basename}.uasset")
            uasset_dst = os.path.join(OUTPUT_DIR, rel_path, f"{basename}.uasset")
            
            if os.path.exists(uasset_src):
                if should_skip(uasset_dst):
                    print(f"  ⏭️ 跳过（已存在）: {rel_path}/{basename}.uasset")
                    skipped_uasset += 1
                else:
                    shutil.copy2(uasset_src, uasset_dst)
                    print(f"  ✅ 复制 uasset: {rel_path}/{basename}.uasset")
                    copied_uasset += 1
            else:
                print(f"  ⚠️ 缺失: {rel_path}/{basename}.uasset")
            
            # ========== 处理 .uexp 文件 ==========
            uexp_src = os.path.join(UASSET_DIR, rel_path, f"{basename}.uexp")
            uexp_dst = os.path.join(OUTPUT_DIR, rel_path, f"{basename}.uexp")
            
            if os.path.exists(uexp_src):
                if should_skip(uexp_dst):
                    print(f"  ⏭️ 跳过（已存在）: {rel_path}/{basename}.uexp")
                    skipped_uexp += 1
                else:
                    shutil.copy2(uexp_src, uexp_dst)
                    print(f"  ✅ 复制 uexp: {rel_path}/{basename}.uexp")
                    copied_uexp += 1
            # .uexp 不存在时不报错，正常情况
    
    # 输出报告
    print("\n" + "=" * 60)
    print("筛选完成报告")
    print("=" * 60)
    print(f"复制 .txt: {copied_txt} 个 | 跳过（已存在）: {skipped_txt} 个")
    print(f"复制 .uasset: {copied_uasset} 个 | 跳过（已存在）: {skipped_uasset} 个")
    print(f"复制 .uexp: {copied_uexp} 个 | 跳过（已存在）: {skipped_uexp} 个")
    print(f"输出目录: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()