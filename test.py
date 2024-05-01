import sys
import os

# sys.pathに含まれるディレクトリからモジュールを検索する
modules = []
for path in sys.path:
    # ディレクトリが存在する場合
    if os.path.isdir(path):
        # ディレクトリ内のファイルを検索して、.pyファイルをモジュールとしてリストに追加
        for filename in os.listdir(path):
            if filename.endswith(".py"):
                modules.append(filename[:-3])

# モジュールをソートして出力
modules.sort()
for module in modules:
    print(module)
