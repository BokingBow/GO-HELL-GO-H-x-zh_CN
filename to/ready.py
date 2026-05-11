import os
import subprocess
import sys

# ========== 配置参数 ==========
TOOL_PATH = r"C:\Users\Boking Bow\Exe\PACKCRACK\UE4localizationsTool\UE4localizationsTool.exe"
TARGET_DIR = r"F:\Reason\Origin\GO HELL GO 素材\ChinesePatch_P\gohellgo"  # .uasset 和 .txt 在同一目录
# =============================

def import_all():
    """批量导入所有翻译（.txt 和 .uasset 在同一目录）"""
    
    # 检查目录是否存在
    if not os.path.exists(TARGET_DIR):
        print(f"[错误] 目标目录不存在: {TARGET_DIR}")
        sys.exit(1)
    
    print("=" * 60)
    print("开始批量导入")
    print("=" * 60)
    
    success_count = 0
    fail_count = 0
    
    # 遍历目标目录中的所有 .txt 文件
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if not file.endswith('.txt'):
                continue
            
            txt_path = os.path.join(root, file)
            
            # 检查对应的 .uasset 是否存在
            uasset_path = txt_path.replace('.uasset.txt', '.uasset')
            if not os.path.exists(uasset_path):
                print(f"\n⚠️ 跳过: {file} - 对应的 .uasset 不存在")
                continue
            
            # 执行导入命令
            cmd = [TOOL_PATH, "import", txt_path]
            
            print(f"\n📄 导入: {file}")
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=False)
                if result.returncode == 0:
                    print(f"  ✅ 成功")
                    success_count += 1
                else:
                    print(f"  ❌ 失败: {result.stderr}")
                    fail_count += 1
            except Exception as e:
                print(f"  ❌ 异常: {e}")
                fail_count += 1
    
    # 输出报告
    print("\n" + "=" * 60)
    print("导入完成报告")
    print("=" * 60)
    print(f"成功: {success_count}  失败: {fail_count}")

def main():
    import_all()

if __name__ == "__main__":
    main()