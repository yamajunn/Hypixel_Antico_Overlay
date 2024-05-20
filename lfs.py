import os
import subprocess

# 監視するディレクトリ
watch_directory = "./"

# 監視するファイルサイズの閾値（100 MB以上のファイルをGit LFSに追加）
size_threshold_mb = 10

# 監視対象のディレクトリ内のファイルを取得
files = os.listdir(watch_directory)

for file in files:
    # ファイルのパスを取得
    file_path = os.path.join(watch_directory, file)
    
    # ファイルサイズをMB単位で取得
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    
    if size_mb > size_threshold_mb:
        # 大きなファイルをGit LFSに追加
        subprocess.run(["git", "lfs", "track", file_path])
        print(f"Added {file_path} to Git LFS")
