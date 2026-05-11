import os
import subprocess
import sys

# ========== 配置参数 ==========
TOOL_PATH = r"C:\Users\Boking Bow\Exe\PACKCRACK\UE4localizationsTool\UE4localizationsTool.exe"  # 文本提取工具的完整路径
TARGET_DIR = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo"                                       # 你的游戏资源文件夹（.uasset所在目录）
TARGET_SUBFOLDER = r"Content\Anzu\DataTable\Scenario"                                           # 要全部提取的文件夹（相对路径）
OUTPUT_ROOT = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo\Extract"                              # 所有提取结果统一放置的根目录
# =============================

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"[创建目录] {path}")

def export_single_file(rel_path):
    uasset_path = os.path.join(TARGET_DIR, rel_path)

    if not os.path.exists(uasset_path):
        print(f"[跳过] 文件不存在: {rel_path}")
        return False

    output_subdir = os.path.join(OUTPUT_ROOT, os.path.dirname(rel_path))
    ensure_dir(output_subdir)

    temp_txt = uasset_path + ".txt"
    target_txt = os.path.join(output_subdir, os.path.basename(uasset_path) + ".txt")

    cmd = [TOOL_PATH, "export", uasset_path]
    print(f"[导出] {rel_path}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            print(f"  失败: {result.stderr}")
            return False

        if os.path.exists(temp_txt):
            os.rename(temp_txt, target_txt)
            print(f"  输出 → {target_txt}")
            return True
        else:
            print(f"  警告: 未生成 {temp_txt}")
            return False
    except Exception as e:
        print(f"  异常: {e}")
        return False

def find_all_uasset_files(base_dir, subfolder):
    """递归查找指定文件夹下所有 .uasset 文件"""
    full_path = os.path.join(base_dir, subfolder)
    if not os.path.exists(full_path):
        print(f"[错误] 文件夹不存在: {full_path}")
        return []

    uasset_files = []
    for root, dirs, files in os.walk(full_path):
        for file in files:
            if file.endswith(".uasset"):
                # 获取相对于 TARGET_DIR 的路径
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, TARGET_DIR)
                uasset_files.append(rel_path)

    return uasset_files

def main():
    # 自动查找所有 .uasset 文件
    print(f"[扫描] {os.path.join(TARGET_DIR, TARGET_SUBFOLDER)}")
    uasset_list = find_all_uasset_files(TARGET_DIR, TARGET_SUBFOLDER)

    if not uasset_list:
        print("[错误] 未找到任何 .uasset 文件")
        sys.exit(1)

    print(f"共找到 {len(uasset_list)} 个 .uasset 文件")
    print("-" * 50)

    ensure_dir(OUTPUT_ROOT)

    success_count = 0
    fail_count = 0

    for rel_path in uasset_list:
        if export_single_file(rel_path):
            success_count += 1
        else:
            fail_count += 1
        print("-" * 50)

    print(f"\n===== 完成 =====")
    print(f"成功: {success_count}  失败: {fail_count}")

if __name__ == "__main__":
    main()