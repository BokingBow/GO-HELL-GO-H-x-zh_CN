import os
import shutil

# ========== 配置 ==========
PATCH_DIR = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo_1_4"           # 升级补丁解包后的目录
OUTPUT_BASE = r"F:\Reason\Origin\GO HELL GO 素材\PatchAnalysis" # 分析结果输出目录
FILELIST_TXT = r"F:\Reason\Origin\GO HELL GO 素材\to\filelist.txt" # 之前翻译过的文件清单
# ==========================

def read_filelist(filelist_path):
    """读取 filelist.txt，返回需要翻译的文件路径集合"""
    with open(filelist_path, 'r', encoding='utf-8') as f:
        # 读取每一行，去除换行符和可能的空白字符
        return set(line.strip() for line in f if line.strip())

def walk_all_files(root_dir):
    """遍历目录，返回所有文件的相对路径集合"""
    files = set()
    for root, dirs, files_in_dir in os.walk(root_dir):
        for file in files_in_dir:
            # 获取相对于根目录的完整路径
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, root_dir)
            files.add(rel_path)
    return files

def main():
    # 1. 读取翻译过的文件清单
    translated_files = read_filelist(FILELIST_TXT)
    print(f"翻译过的文件数量: {len(translated_files)}")
    
    # 2. 遍历补丁目录，获取所有文件
    patch_files = walk_all_files(PATCH_DIR)
    print(f"补丁目录文件数量: {len(patch_files)}")
    
    # 3. 分类
    # 类别 A: 在补丁中存在且在翻译清单中（需要更新翻译）
    need_update = patch_files & translated_files
    
    # 类别 B: 在补丁中存在但不在翻译清单中（未修改过的更新）
    need_review = patch_files - translated_files
    
    # 类别 C: 在翻译清单中但不在补丁中（文件已被移除或改名，可以忽略）
    removed = translated_files - patch_files
    
    # 4. 输出报告
    print("\n" + "=" * 60)
    print("分类结果")
    print("=" * 60)
    print(f"📝 需要更新翻译的文件: {len(need_update)} 个")
    print(f"👀 未修改过的更新文件: {len(need_review)} 个")
    print(f"🗑️ 已移除/改名的文件: {len(removed)} 个")
    
    # 5. 将分类结果输出到文件
    os.makedirs(OUTPUT_BASE, exist_ok=True)
    
    with open(os.path.join(OUTPUT_BASE, "need_update.txt"), 'w', encoding='utf-8') as f:
        for path in sorted(need_update):
            f.write(path + '\n')
    
    with open(os.path.join(OUTPUT_BASE, "need_review.txt"), 'w', encoding='utf-8') as f:
        for path in sorted(need_review):
            f.write(path + '\n')
    
    with open(os.path.join(OUTPUT_BASE, "removed.txt"), 'w', encoding='utf-8') as f:
        for path in sorted(removed):
            f.write(path + '\n')
    
    # 可选：复制需要更新的文件到单独文件夹，方便处理
    update_output_dir = os.path.join(OUTPUT_BASE, "need_update_files")
    for rel_path in need_update:
        src = os.path.join(PATCH_DIR, rel_path)
        dst = os.path.join(update_output_dir, rel_path)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    
    print(f"\n📁 输出目录: {OUTPUT_BASE}")
    print(f"   - need_update.txt: 需要更新翻译的文件清单")
    print(f"   - need_review.txt: 未修改过的更新文件清单")
    print(f"   - removed.txt: 已移除的文件清单")
    print(f"   - need_update_files/: 需要更新翻译的文件副本")

if __name__ == "__main__":
    main()