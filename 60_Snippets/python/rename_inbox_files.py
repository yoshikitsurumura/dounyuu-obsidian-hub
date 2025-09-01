import os
import datetime
import re
import sys

# --- 設定 ---
# スクリプト自身の場所を基準に、Obsidian Vaultのルートパスを堅牢に取得
# 例: C:\Users\mayum\dounyuu\ObsidianVault\60_Snippets\python -> C:\Users\mayum\dounyuu\ObsidianVault
try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # 対話型環境などで__file__が未定義の場合のフォールバック
    SCRIPT_DIR = os.getcwd()

VAULT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
INBOX_PATH = os.path.join(VAULT_ROOT, '00_Inbox')

# タイムスタンプの正規表現パターン (YYYY-MM-DD_HHMMSS_)
TIMESTAMP_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}_\d{6}_')

# --- メイン処理 ---
def rename_files_in_inbox():
    """
    Inboxディレクトリ内のファイルをチェックし、
    タイムスタンプが付いていないファイルにタイムスタンプを付与してリネームする。
    """
    print(f"--- Running File Rename Script ---")
    print(f"Target directory: {INBOX_PATH}")
    
    if not os.path.isdir(INBOX_PATH):
        print(f"Error: Inbox directory not found at '{INBOX_PATH}'")
        return

    try:
        files = os.listdir(INBOX_PATH)
    except OSError as e:
        print(f"Error: Cannot access directory '{INBOX_PATH}': {e}")
        return
        
    renamed_count = 0

    for filename in files:
        # 既にタイムスタンプが付いているファイルはスキップ
        if TIMESTAMP_PATTERN.match(filename):
            continue

        old_filepath = os.path.join(INBOX_PATH, filename)

        # ディレクトリはスキップ
        if not os.path.isfile(old_filepath):
            continue

        try:
            # ファイルの作成日時を取得
            creation_time = os.path.getctime(old_filepath)
            dt_object = datetime.datetime.fromtimestamp(creation_time)
            
            # 新しいファイル名のタイムスタンプ部分を作成 (YYYY-MM-DD_HHMMSS)
            timestamp_str = dt_object.strftime('%Y-%m-%d_%H%M%S')
            
            # 新しいファイル名を生成
            new_filename = f"{timestamp_str}_{filename}"
            new_filepath = os.path.join(INBOX_PATH, new_filename)

            # ファイルをリネーム
            os.rename(old_filepath, new_filepath)
            print(f"  - Renamed: '{filename}' -> '{new_filename}'")
            renamed_count += 1

        except OSError as e:
            print(f"  - Error renaming file '{filename}': {e}")

    if renamed_count == 0:
        print("Result: No new files to rename.")
    else:
        print(f"Result: Finished. Renamed {renamed_count} file(s).")
    print(f"---------------------------------")


# --- 実行 ---
if __name__ == "__main__":
    rename_files_in_inbox()
