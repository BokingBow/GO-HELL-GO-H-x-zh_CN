import os
import subprocess
import sys

# ========== 配置参数（请根据你的实际情况修改）==========
TOOL_PATH = r"C:\Users\Boking Bow\Exe\PACKCRACK\UE4localizationsTool\UE4localizationsTool.exe"  # 文本提取工具的完整路径
TARGET_DIR = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo"                                       # 你的游戏资源文件夹（.uasset所在目录）
OUTPUT_ROOT = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo\Extract"                              # 所有提取结果统一放置的根目录
LIST_FILE = r"F:\Reason\Origin\GO HELL GO 素材\gohellgo\filelist.txt"                           # 记录需要提取的.uasset清单（每行一个相对路径）
# ========================================================

def ensure_dir(path):
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"[目录创建] {path}")

def export_single_file(rel_path):
    """对单个 .uasset 文件执行导出"""
    uasset_path = os.path.join(TARGET_DIR, rel_path)
    
    # 检查文件是否存在
    if not os.path.exists(uasset_path):
        print(f"[跳过] 文件不存在: {rel_path}")
        return False

    # 构建输出目录：保持原有目录结构
    output_subdir = os.path.join(OUTPUT_ROOT, os.path.dirname(rel_path))
    ensure_dir(output_subdir)

    # .txt 文件的保存位置（会自动放在Output/对应目录下）
    # 注意：UE4LocalizationsTool 的 export 会在被导出文件同目录下生成 .txt
    # 我们需要先 copy 一份到 OUTPUT_ROOT 里（或者直接让工具输出到那里？工具不支持指定输出路径）
    # 折中方案：先导出到原目录，再移动到统一输出目录
    temp_uasset = os.path.join(TARGET_DIR, rel_path)
    temp_txt = temp_uasset + ".txt"

    # 调用工具导出（在原目录生成 .txt）
    cmd = [TOOL_PATH, "export", temp_uasset]
    print(f"[导出] {rel_path}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            print(f"  失败: {result.stderr}")
            return False
        
        # 检查 .txt 是否生成
        if os.path.exists(temp_txt):
            # 移动到统一输出目录
            target_txt = os.path.join(output_subdir, os.path.basename(uasset_path) + ".txt")
            os.rename(temp_txt, target_txt)
            print(f"  输出 → {target_txt}")
            return True
        else:
            print(f"  警告: 工具执行成功但未生成 {temp_txt}")
            return False
            
    except Exception as e:
        print(f"  异常: {e}")
        return False

def main():
    # 检查清单文件是否存在
    if not os.path.exists(LIST_FILE):
        print(f"[错误] 清单文件不存在: {LIST_FILE}")
        sys.exit(1)

    # 确保输出根目录存在
    ensure_dir(OUTPUT_ROOT)

    # 读取清单
    with open(LIST_FILE, "r", encoding="utf-8") as f:
        rel_paths = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not rel_paths:
        print("[错误] 清单文件中没有指定任何 .uasset 文件")
        sys.exit(1)

    print(f"共需要处理 {len(rel_paths)} 个文件")
    
    success_count = 0
    fail_count = 0

    for rel_path in rel_paths:
        if export_single_file(rel_path):
            success_count += 1
        else:
            fail_count += 1
        print("-" * 50)

    print(f"\n===== 处理完成 =====")
    print(f"成功: {success_count}  失败: {fail_count}")

if __name__ == "__main__":
    main()