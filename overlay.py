import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QLabel, QLineEdit, QFileDialog, QDesktopWidget, QHeaderView
from PyQt5.QtCore import Qt, QPoint, QTimer, QSize
from PyQt5.QtGui import QColor, QIcon, QPixmap
import joblib
import concurrent.futures
import json
import keyboard
import time
import os
import pandas as pd
import requests
from sklearn.ensemble import RandomForestClassifier
import subprocess
from functools import partial

dic_labels = [
    'karma',
    'networkExp',
    # 'newPackageRank',
    # 'particlePack',
    # 'playername',
    # 'questSettings',
    # 'rankPlusColor',
]
achievements = [
    'bedwars_beds',
    'bedwars_bedwars_challenger',
    'bedwars_bedwars_killer',
    'bedwars_collectors_edition',
    'bedwars_level',
    'bedwars_loot_box',
    'bedwars_slumber_ticket_master',
    'bedwars_wins',
]
challenges = [
    'challenges','all_time'
    'BEDWARS__defensive',
    'BEDWARS__offensive',
    'BEDWARS__support',
]
statuses = [
    'Bedwars_openedChests',
    'Experience',
    '_items_purchased_bedwars',
    # 'activeWoodType',
    'beds_broken_bedwars',
    'beds_lost_bedwars',
    'coins',
    'deaths_bedwars',
    'diamond_resources_collected_bedwars',
    'emerald_resources_collected_bedwars',
    'fall_deaths_bedwars',
    'fall_final_deaths_bedwars',
    'fall_final_kills_bedwars',
    'fall_kills_bedwars',
    # 'favourites_2',
    'final_deaths_bedwars',
    'final_kills_bedwars',
    'games_played_bedwars',
    'games_played_bedwars_1',
    'kills_bedwars',
    'losses_bedwars',
    'void_deaths_bedwars',
    'void_final_deaths_bedwars',
    'void_final_kills_bedwars',
    'void_kills_bedwars',
    'wins_bedwars',
]

def getinfo(call):
    try:
        r = requests.get(call, timeout=5)
        r.raise_for_status()  # エラーがあれば例外を発生させる
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_status(uuid, API_KEY):
    uuid_link = f"https://api.hypixel.net/player?key={API_KEY}&uuid={uuid}"
    data_dic = getinfo(uuid_link)
    # pprint.pprint(data_dic)
    datas = []
    if (data_dic != None and "success" in data_dic and data_dic["success"] == True and "player" in data_dic and data_dic["player"] is not None) or not ("cause" in data_dic and data_dic["cause"] == "Key throttle"):
        for dic_label in dic_labels:
            if dic_label in data_dic["player"]:
                datas.append(data_dic["player"][dic_label])
            else:
                datas.append(0)
        for achievement in achievements:
            if 'achievements' in data_dic["player"] and achievement in data_dic["player"]['achievements']:
                datas.append(data_dic["player"]['achievements'][achievement])
            else:
                datas.append(0)
        for challenge in challenges:
            if 'challenges' in data_dic["player"] and 'all_time' in data_dic["player"]['challenges'] and challenge in data_dic["player"]['challenges']['all_time']:
                datas.append(data_dic["player"]['challenges']['all_time'][challenge])
            else:
                datas.append(0)
        for stats in statuses:
            if 'stats' in data_dic["player"] and 'Bedwars' in data_dic["player"]['stats'] and stats in data_dic["player"]['stats']['Bedwars']:
                datas.append(data_dic["player"]['stats']['Bedwars'][stats])
            else:
                datas.append(0)
        for a in range(len(datas)):
            if a in [27,32,18,6]:
            # if a in [9, 14, 4, 1]:
                if datas[a] == 0:
                    datas[a] = 1
        for j in [datas[28] / datas[27], datas[37] / datas[32], datas[17] / datas[18], datas[28] / datas[6], datas[31] / datas[6], datas[17] / datas[6]]:
        # for j in [datas[10] / datas[9], datas[16] / datas[14], datas[3] / datas[4], datas[10] / datas[1], datas[13] / datas[1], datas[3] / datas[1]]:
            datas.append(j)
        if "stats" in data_dic["player"] and "Bedwars" in data_dic["player"]["stats"] and "favourites_2" in data_dic["player"]["stats"]["Bedwars"]:
            shop = len(set(data_dic["player"]["stats"]["Bedwars"]["favourites_2"].split(",")) & set(["golden_apple", "fireball", "diamond_boots"]))
        else:
            shop = None
        if "userLanguage" in data_dic["player"]:
            language =  data_dic["player"]["userLanguage"]
        else:
            language = None
        return [datas, shop, language]
    else:
        return [None, None, None]
    
def games(uuid, API_KEY):
    games_link = f"https://api.hypixel.net/v2/recentgames?key={API_KEY}&uuid={uuid}"
    data_dic = getinfo(games_link)
    modes = []
    game_nums = []
    if data_dic != None and "games" in data_dic:
        if len(data_dic["games"]) == 3:
            modes.append(data_dic["games"][0]["gameType"])
            modes.append(data_dic["games"][1]["gameType"])
            modes.append(data_dic["games"][2]["gameType"])
        if len(data_dic["games"]) == 2:
            modes.append(data_dic["games"][0]["gameType"])
            modes.append(data_dic["games"][1]["gameType"])
        if len(data_dic["games"]) == 1:
            modes.append(data_dic["games"][0]["gameType"])
        for mode in modes:
            if mode == "BEDWARS":
                game_nums.append(0)
            elif mode == "SKYWARS":
                game_nums.append(1)
            elif mode == "TNTGAMES":
                game_nums.append(2)
            elif mode == "UHC":
                game_nums.append(3)
            elif mode == "MURDER_MYSTERY":
                game_nums.append(4)
            elif mode == "BUILD_BATTLE":
                game_nums.append(5)
            elif mode == "DUELS":
                game_nums.append(6)
            elif mode == "SKYBLOCK":
                game_nums.append(7)
            elif mode == "PIT":
                game_nums.append(8)
            else:
                game_nums.append(9)
    return game_nums

def pols(uuid, POLSU_KEY):
    url = "https://api.polsu.xyz/polsu/ping"
    querystring = {"uuid":f"{uuid}"}
    headers = {"Api-Key": POLSU_KEY}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # HTTP エラーがあれば例外を発生させる
        pings = response.json()
        # print(pings)
        if pings != None and "success" in pings and pings["success"] == True and "data" in pings and "history" in pings["data"] and "avg" in pings["data"]["history"][0] and len(pings["data"]["history"]) != 0:
            ping = int(pings["data"]["history"][0]["avg"])
        else:
            ping = "???"
    except requests.exceptions.RequestException as e:
        ping = "???"
    return ping

def status(name, API_KEY, POLSU_KEY):
    name_link = f"https://api.mojang.com/users/profiles/minecraft/{name}"
    info = getinfo(name_link)
    if info != None and "id" in info:
        uuid = info["id"]
        return_status = get_status(info["id"], API_KEY)
        return [return_status[0], pols(uuid, POLSU_KEY), games(uuid, API_KEY), return_status[1], return_status[2], uuid]
    else:
        return [None, None, None, None, None, None]

def judgment_cheater(data, model, scaler):
    if data is None:
        return None
    def_columns = ['karma', 'networkExp', 'bedwars_beds', 'bedwars_bedwars_challenger',
        'bedwars_bedwars_killer', 'bedwars_collectors_edition', 'bedwars_level',
        'bedwars_loot_box', 'bedwars_slumber_ticket_master', 'bedwars_wins',
        'challenges', 'all_timeBEDWARS__defensive', 'BEDWARS__offensive',
        'BEDWARS__support', 'Bedwars_openedChests', 'Experience',
        '_items_purchased_bedwars', 'beds_broken_bedwars', 'beds_lost_bedwars',
        'coins', 'deaths_bedwars', 'diamond_resources_collected_bedwars',
        'emerald_resources_collected_bedwars', 'fall_deaths_bedwars',
        'fall_final_deaths_bedwars', 'fall_final_kills_bedwars',
        'fall_kills_bedwars', 'final_deaths_bedwars', 'final_kills_bedwars',
        'games_played_bedwars', 'games_played_bedwars_1', 'kills_bedwars',
        'losses_bedwars', 'void_deaths_bedwars', 'void_final_deaths_bedwars',
        'void_final_kills_bedwars', 'void_kills_bedwars', 'wins_bedwars',
        'fkdr', 'wlr', 'bblr', 'fk_lev', 'bb_lev', 'kill_lev']
    use_column = ['karma', 'bedwars_level',
        'bedwars_loot_box',
        'all_timeBEDWARS__defensive', 'BEDWARS__offensive',
        'BEDWARS__support', 'Bedwars_openedChests',
        'beds_broken_bedwars', 'beds_lost_bedwars',
        'deaths_bedwars', 'diamond_resources_collected_bedwars',
        'emerald_resources_collected_bedwars', 'fall_deaths_bedwars',
        'final_deaths_bedwars', 'final_kills_bedwars',
        'games_played_bedwars', 'games_played_bedwars_1', 'kills_bedwars',
        'losses_bedwars', 'void_deaths_bedwars', 'void_final_deaths_bedwars',
        'void_final_kills_bedwars', 'void_kills_bedwars', 'wins_bedwars'
        ]
    
    indices_to_remove = []
    for i, col in enumerate(def_columns):
        if not col in use_column:
            indices_to_remove.append(i)
    
    filtered_data = [value for index, value in enumerate(data) if index not in indices_to_remove]
    df = pd.DataFrame([filtered_data], columns=use_column)
    # Cheatカラムを削除して、各レコードの合計を計算する
    row_sums = df.sum(axis=1)

    # 分母が0になる可能性がある行のインデックスを取得
    zero_division_indices = row_sums[row_sums == 0].index

    # 10,000をその行の合計値で割った値を計算して保持する
    divisors = pd.Series(0, index=df.index)  # 全ての行を0で初期化
    divisors[zero_division_indices] = 0  # 分母が0になる行のみ0に設定
    divisors = divisors.astype('float64')
    divisors[~divisors.index.isin(zero_division_indices)] = 10000 / row_sums[~row_sums.index.isin(zero_division_indices)]
    scaled = df.mul(divisors, axis=0)

    y_pred = model.predict_proba(scaled)
    # print(y_pred)
    return y_pred[0][0]

def checker(mcid, model, scaler, API_KEY, POLSU_KEY):
    data, ping, mode, shop, language, met = status(mcid, API_KEY, POLSU_KEY)
    cheater = judgment_cheater(data, model, scaler)
    if not data is None:
        return [mcid, cheater, ping, mode, shop, language, met, data[6], round(data[38], 2), round((data[28]+data[31])/data[29], 2)]
    else:
        return [mcid, cheater, ping, mode, shop, language, met, None, None, None]

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# path = r"/Users/chinq500/Library/Application Support/minecraft/versions/1.8.9/logs/latest.log"
# path = r"C:/Users/Owner/AppData/Roaming/.minecraft/logs/blclient/minecraft/latest.log"
with open(resource_path('met_player.json'), 'w') as f:
    json.dump({}, f, indent=4)

with open(resource_path('table.json'), 'w') as w1:
    json.dump([], w1)

def who(s):
    l = s.split("\n")
    who_list = []
    for item in l:
        if item[40:47] == "ONLINE:":
            who_list = item[48:].split(", ")
    return who_list

def auto_who(s):
    l = s.split("\n")
    who_list = []
    for item in l:
        if (" が参加しました (" in item and "/" in item and ")！" in item) or (" has joined (" in item and "/" in item and ")!" in item):
            for i, string in enumerate(list(item[40:])):
                if string == " ":
                    who_list.append(item[40:40+i])
                    break
    return who_list

def exit_player(s):
    l = s.split("\n")
    who_list = []
    for item in l:
        if " が退出しました！" in item:
            for i, string in enumerate(list(item[40:])):
                if string == " ":
                    who_list.append(item[40:40+i])
                    break
    return who_list

class ImageTableWidgetItem(QTableWidgetItem):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.widget = QLabel()
        self.widget.setPixmap(QPixmap(image_path))
        self.widget.setAlignment(Qt.AlignCenter)
        self.setSizeHint(self.widget.sizeHint())

    def clone(self):
        new_item = ImageTableWidgetItem(self.image_path)
        return new_item

    def __lt__(self, other):
        # Sort items numerically instead of alphabetically
        return float(self.text()) < float(other.text())
try:
    with open('key.json') as k:
        key = json.load(k)
        print(key)
        key[6]
except Exception:
    with open('key.json', 'w') as kk:
        json.dump(["f5", "838bf3d7-9d38-4d3d-a99f-a967ba52c208", "a5759d02-94e9-466a-8e40-6679b1ccb256", "C:/Users/Owner/AppData/Roaming/.minecraft/logs/blclient/minecraft/latest.log", 0, 0, 13], kk)
    with open('key.json') as k:
        key = json.load(k)
        print(key)

def antico():
    with open(key[3]) as f:
        f.read()
        class DraggableWindow(QWidget):
            def __init__(self):
                super().__init__()
                self.initUI()
                self.installEventFilter(self)

                with open('key.json') as k:
                    key = json.load(k)
                def on_key_event(event):
                    if event.event_type == keyboard.KEY_DOWN:
                        if event.name == key[0]:
                            self.ShowOrHide()
                keyboard.on_press(on_key_event)

                self.pressed = False
                self.check = False
                self.players = []

            def ShowOrHide(self):
                if not self.pressed:
                    if self.isHidden():
                        print("show")
                        self.show()
                    else:
                        print("hide")
                        self.hide()

            def initUI(self):
                screen = QDesktopWidget().screenGeometry()
                self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 枠を消して最前面に表示する
                self.setGeometry(key[4], key[5], int(screen.width()//1.5), int(screen.height()//1.5))  # ウィンドウサイズ
                self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
                self.setAttribute(Qt.WA_TranslucentBackground)  # 背景を透明にする
                self.setWindowIcon(QIcon(resource_path('logo.ico')))  # アイコンを設定
                self.oldPos = self.pos()  # ウィンドウの初期位置
                self.setFocus()
                
                # テーブルウィジェットを作成して内容を追加
                self.table_widget = QTableWidget(self)
                horizontal_header = self.table_widget.horizontalHeader()
                horizontal_header.setStyleSheet(
                    "QHeaderView::section {"
                    "    background-color: rgba(0, 0, 0, 0.5);"
                    "    color: white;"
                    "}"
                )

                vertical_header = self.table_widget.verticalHeader()
                vertical_header.setStyleSheet(
                    "QHeaderView::section {"
                    "    background-color: rgba(0, 0, 0, 0.5);"
                    "    color: white;"
                    "}"
                )
                self.table_widget.setColumnCount(12)
                self.table_widget.setHorizontalHeaderLabels(["STAR", "MCID", "G%", "PING", "LG", "1", "2", "3", "QB", "MET", "FKDR", "KILL AVG"])  # カラムのヘッダー
                list_num = 16
                self.table_widget.setRowCount(list_num)  # 16行に変更
                self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)
                self.table_widget.setFrameStyle(QFrame.NoFrame)

                self.table_widget.setColumnWidth(0, screen.width()//27)
                self.table_widget.setColumnWidth(1, screen.width()//12)
                self.table_widget.setColumnWidth(2, screen.width()//27)
                self.table_widget.setColumnWidth(3, screen.width()//27)
                self.table_widget.setColumnWidth(4, screen.width()//27)
                self.table_widget.setColumnWidth(5, screen.width()//27)
                self.table_widget.setColumnWidth(6, screen.width()//27)
                self.table_widget.setColumnWidth(7, screen.width()//27)
                self.table_widget.setColumnWidth(8, screen.width()//27)
                self.table_widget.setColumnWidth(9, screen.width()//27)
                self.table_widget.setColumnWidth(10, screen.width()//27)
                self.table_widget.setColumnWidth(11, screen.width()//27)

                # 以下、追加した行のデータを設定
                for i in range(list_num):
                    self.table_widget.setRowHeight(i, screen.height()//35)

                self.table_widget.setGeometry(0, 30, screen.width(), screen.height())  # 位置とサイズを設定

                # self.table_widget.setGeometry(0, 30, 800, screen.height()//2)  # 位置とサイズを設定
                self.table_widget.setStyleSheet("""
                    background-color: rgba(0, 0, 0, 0);
                    color: white;
                    QTableWidget::corner {
                        background-color: rgba(255, 255, 255, 0.2);
                        color: white;
                    }
                    QTableCornerButton::section {
                        border-width: 1px;
                        border-color: #BABABA;
                        border-style: solid;
                    }
                """)

                # 更新タイマーを設定して定期的にテーブルを更新
                self.update_timer = QTimer(self)
                self.update_timer.timeout.connect(self.who_checker)
                self.update_timer.start(1000)  # 1秒ごとに更新

                # 更新タイマーを設定して定期的にテーブルを更新
                self.check_timer = QTimer(self)
                self.check_timer.timeout.connect(self.updater)
                self.check_timer.start(1000)  # 1秒ごとに更新

                # 更新タイマーを設定して定期的にテーブルを更新
                self.reset_timer = QTimer(self)
                self.reset_timer.timeout.connect(self.reset_json)
                self.reset_timer.start(60000)  # 1分ごとに更新

                # 閉じるボタン
                self.closeButton = QPushButton('×', self)
                self.closeButton.setGeometry(int(screen.width()//2.5)-200, 0, 40, 30)
                self.closeButton.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border: 2px solid rgba(200, 200, 200, 250); color: white;")
                self.closeButton.clicked.connect(self.close)

                # フレームを作成して黒い枠を設定
                frame = QFrame(self)
                frame.setFrameStyle(QFrame.Box)
                frame.setLineWidth(5)
                frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border: 2px solid rgba(200, 200, 200, 250);")
                frame.setGeometry(0, 0, int(screen.width()//2.5)-200, 30)

                # 画像を表示するための QLabel を作成し、親を frame に設定
                image_label = QLabel(frame)
                # 画像を読み込む
                pixmap = QPixmap(resource_path('logo_white.png'))
                scaled_pixmap = pixmap.scaled(30, 30, aspectRatioMode=Qt.KeepAspectRatio)
                # QLabel に画像をセット
                image_label.setPixmap(scaled_pixmap)
                # 画像の位置を設定
                image_label.setGeometry(5, 0, 360, 30)
                image_label.setStyleSheet("background-color: rgba(0, 0, 0, 0); border: 2px solid rgba(255, 255, 255, 0);")

                # フレームにテキストを追加するラベルを作成
                label = QLabel("Anti Cockroach", frame)
                label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 0); border: 2px solid rgba(255, 255, 255, 0);")
                font = label.font()  # フォントを取得
                font.setBold(True)  # フォントを太くする
                label.setFont(font)  # 変更したフォントをセット
                label.setGeometry(45, 0, 360, 30)  # ラベルのサイズと位置を設定

                self.settings_button = QPushButton(self)
                self.settings_button.setIcon(QIcon(resource_path("gear.png")))
                self.settings_button.setIconSize(QSize(25, 25))
                self.settings_button.setGeometry(int(screen.width()//2.5)-240, 5, 20, 20)
                self.settings_button.clicked.connect(self.open_settings)

                # レイアウトを設定
                layout = QVBoxLayout(self)
                # layout.addWidget(frame)
                layout.setContentsMargins(0, 0, 0, 0)
                self.setLayout(layout)

            def open_settings(self):
                screen = QDesktopWidget().screenGeometry()
                self.settings_window = QWidget()
                self.settings_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 枠を消して最前面に表示する
                self.settings_window.setGeometry(self.x()+int(screen.width()//2.5)-160, self.y(), 200, 375)  # ウィンドウサイズ
                self.settings_window.setAttribute(Qt.WA_TranslucentBackground)  # 背景を透明にする  
                self.settings_window.setWindowIcon(QIcon(resource_path('logo.ico')))  # アイコンを設定
                self.settings_window.setFocus()

                # フレームを作成して黒い枠を設定
                settings_frame = QFrame(self.settings_window)
                settings_frame.setFrameStyle(QFrame.Box)
                settings_frame.setLineWidth(5)
                settings_frame.setStyleSheet("border: 2px solid rgba(200, 200, 200, 250); background-color: rgba(0, 0, 0, 100);")
                settings_frame.setGeometry(0, 0, 200, 375)

                # 閉じるボタンを作成し、右上に配置
                close_button = QPushButton('×', self.settings_window)
                close_button.setGeometry(self.settings_window.width()-40, 0, 40, 30)
                close_button.setStyleSheet("border: 2px solid rgba(200, 200, 200, 250); color: white;")
                close_button.clicked.connect(self.settings_window.close)

                # ラベルを作成してテキストを設定し、ウィンドウに配置
                label = QLabel("SETTINGS", self.settings_window)
                label.setGeometry(10, 10, 60, 30)  # 適切な位置に配置
                label.setStyleSheet("color: white;")

                layout = QVBoxLayout()

                self.input_box_f = QLineEdit(self.settings_window)
                self.input_box_f.setGeometry(10, 40, 70, 30)
                self.input_box_f.setStyleSheet("background-color: rgba(0, 0, 0, 20); color: white;")
                layout.addWidget(self.input_box_f)

                self.button = QPushButton('SET FONT SIZE', self.settings_window)
                self.button.clicked.connect(self.get_font)
                self.button.setGeometry(90, 40, 100, 30)
                self.button.setStyleSheet("background-color: white;")
                layout.addWidget(self.button)

                self.key_label = QLabel('PLESS THE SHOW or HIDE KEY')
                layout.addWidget(self.key_label)

                self.button = QPushButton('PLESS THE SHOW or HIDE KEY', self.settings_window)
                self.button.clicked.connect(self.get_key)
                self.button.setGeometry(10, 80, 180, 30)
                self.button.setStyleSheet("background-color: white;")
                layout.addWidget(self.button)

                self.input_box = QLineEdit(self.settings_window)
                self.input_box.setGeometry(10, 130, 180, 30)
                self.input_box.setStyleSheet("background-color: rgba(0, 0, 0, 20); color: white;")
                layout.addWidget(self.input_box)

                self.button = QPushButton('SET HYPIXEL API', self.settings_window)
                self.button.setGeometry(10, 170, 180, 30)
                self.button.setStyleSheet("background-color: white;")
                self.button.clicked.connect(self.get_text)
                layout.addWidget(self.button)

                self.input_box2 = QLineEdit(self.settings_window)
                self.input_box2.setGeometry(10, 230, 180, 30)
                self.input_box2.setStyleSheet("background-color: rgba(0, 0, 0, 20); color: white;")
                layout.addWidget(self.input_box2)

                self.button2 = QPushButton('SET POLSU API', self.settings_window)
                self.button2.setGeometry(10, 270, 180, 30)
                self.button2.setStyleSheet("background-color: white;")
                self.button2.clicked.connect(self.get_text_polsu)
                layout.addWidget(self.button2)

                self.button3 = QPushButton('SELECT LOG FILE', self.settings_window)
                self.button3.setGeometry(10, 325, 180, 30)
                self.button3.setStyleSheet("background-color: white;")
                self.button3.clicked.connect(self.get_file_path)
                layout.addWidget(self.button3)
                
                self.settings_window.show()

            def get_key(self):
                self.key_label.setText('Set Key')
                keyboard.on_press(self.on_press)
            
            def get_file_path(self):
                file_dialog = QFileDialog()
                file_dialog.setFileMode(QFileDialog.AnyFile)
                file_dialog.setViewMode(QFileDialog.Detail)
                if file_dialog.exec_():
                    file_paths = file_dialog.selectedFiles()
                    if len(file_paths) > 0:
                        file_path = file_paths[0]
                        print(file_path)
            
            def get_text(self):
                key = self.input_box.text()
                print("Set HYPIXEL API:", key)
                if key != "":
                    with open('key.json') as k:
                        read_key = json.load(k)
                    read_key[1] = key
                    with open('key.json', 'w') as kk:
                        json.dump(read_key, kk)
            
            def get_font(self):
                key = self.input_box_f.text()
                print("Set Font:", key)
                if key != "" and key.isdecimal():
                    with open('key.json') as k:
                        read_key = json.load(k)
                    read_key[6] = int(key)
                    with open('key.json', 'w') as kk:
                        json.dump(read_key, kk)
            
            def get_text_polsu(self):
                key = self.input_box2.text()
                print("Set POLSU API:", key)
                if key != "":
                    with open('key.json') as k:
                        read_key = json.load(k)
                    read_key[2] = key
                    with open('key.json', 'w') as kk:
                        json.dump(read_key, kk)

            def on_press(self, event):
                key = event.name
                self.key_label.setText(f'Key pressed: {key}')
                keyboard.unhook_all()
                print(f'Set: {key}')
                keyboard.add_hotkey(key, lambda: self.ShowOrHide())
                with open('key.json') as k:
                    read_key = json.load(k)
                    print(read_key)
                read_key[0] = key
                with open('key.json', 'w') as kk:
                    json.dump(read_key, kk)
                
            def mousePressEvent(self, event):
                if event.button() == Qt.LeftButton:
                    self.oldPos = event.globalPos()  # クリック時のマウス位置を取得

            def mouseMoveEvent(self, event):
                if event.buttons() == Qt.LeftButton:
                    delta = QPoint(event.globalPos() - self.oldPos)  # 移動量を計算
                    self.move(self.x() + delta.x(), self.y() + delta.y())  # ウィンドウを移動
                    try:
                        screen = QDesktopWidget().screenGeometry()
                        self.settings_window.move(self.x() + int(screen.width()//2.5)-110, self.y() + delta.y())
                    except AttributeError:
                        pass
                    # print(self.x() + delta.x(), self.y() + delta.y())
                    with open('key.json') as k:
                        key = json.load(k)
                    key[4] = self.x() + delta.x()
                    key[5] = self.y() + delta.y()
                    with open('key.json', 'w') as kk:
                        json.dump(key, kk)
                    self.oldPos = event.globalPos()  # 新しい位置を保存
            def reset_json(self):
                with open(resource_path('table.json'), 'w') as w3:
                    json.dump([], w3)

            def updater(self):
                if self.check:
                    players = self.players
                    values = []
                    model = joblib.load(resource_path('Cheater.pkl'))
                    scaler = joblib.load(resource_path('scaler.joblib'))
                    mode_list = ["pix_bed.png", "pix_eye.png", "pix_tnt.png", "pix_gapple.png", "pix_bow.png", "pix_bench.png", "pix_fishing.png", "pix_hub.png", "pix_dirt.png", "pix_none.png"]
                    with open(resource_path('table.json')) as r:
                        li = json.load(r)
                        for l in li:
                            if l[0] in players and time.time() - l[10] <= 60:
                                players.remove(l[0])
                                values.append(l)
                    # print(players)
                    with open('key.json') as k:
                        key = json.load(k)
                    API_KEY = key[1]
                    POLSU_KEY = key[2]
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        return_value = list(executor.map(lambda mcid: checker(mcid, model, scaler, API_KEY, POLSU_KEY), players))
                    values += return_value
                    with open(resource_path('table.json'), 'wt') as w2:
                        now = time.time()
                        save_list = []
                        for value in return_value:
                            value.append(now)
                            save_list.append(value)
                        json.dump(save_list, w2, indent=4)
                    def sort_key(item):
                        if item is None or item[7] is None:
                            return -float('inf')  # None や整数以外の要素を降順にするため、inf を返す
                        elif not isinstance(item[7], int):
                            return -float('inf')  # None や整数以外の要素を降順にするため、inf を返す
                        return -item[7]  # 整数の場合は、そのままの値を返す

                    values.sort(key=sort_key)
                    row_count = sum(1 for row in range(self.table_widget.rowCount()) if self.table_widget.item(row, 0) is not None)
                    # print(self.table_widget.item(0, 0))
                    for num, updated_values in enumerate(values):
                        print(self.table_widget.item(num, 0))
                        row = row_count + num
                        met_num = 0
                        with open(resource_path('met_player.json')) as r:
                            di = json.load(r)
                            if updated_values[6] != None:
                                if updated_values[6] in di:
                                    met_num = di[updated_values[6]]
                                    di[updated_values[6]] += 1
                                else:
                                    di[updated_values[6]] = 1
                                with open(resource_path('met_player.json'), 'w') as w:
                                    json.dump(di, w, indent=4)
                        # print(updated_values)
                        pixmap0 = QPixmap(resource_path(mode_list[9]))
                        pixmap1 = QPixmap(resource_path(mode_list[9]))
                        pixmap2 = QPixmap(resource_path(mode_list[9]))
                        pixmap0 = pixmap0.scaled(28, 28)
                        pixmap1 = pixmap1.scaled(28, 28)
                        pixmap2 = pixmap2.scaled(28, 28)

                        font_size = int(key[6])

                        if updated_values[1] == None or updated_values[1] == "???" or float(updated_values[1]) >= 0.9:
                            g_color = QColor(255, 0, 0)
                            back_g = QColor(50, 0, 0, 150)
                        elif updated_values[1] >= 0.6:
                            g_color = QColor(255, 165, 0)
                            back_g = QColor(50, 20, 0, 150)
                        else:
                            g_color = QColor(255, 255, 255)
                            back_g = QColor(50, 50, 50, 150)
                        if updated_values[2] is None or updated_values[2] == "???" or updated_values[2] > 230:
                            ping_color = QColor(255, 0, 0)
                            back_ping = QColor(50, 0, 0, 150)
                        elif 170 <= updated_values[2] <= 230:
                            ping_color = QColor(255, 165, 0)
                            back_ping = QColor(50, 20, 0, 150)
                        else:
                            ping_color = QColor(255, 255, 255)
                            back_ping = QColor(50, 50, 50, 150)
                        if updated_values[4] is None or updated_values[4] == "???":
                            qb_color = QColor(255, 0, 0)
                            back_qb = QColor(50, 0, 0, 150)
                            updated_values[4] = "???"
                        elif updated_values[4] == 3:
                            qb_color = QColor(255, 0, 0)
                            back_qb = QColor(50, 0, 0, 150)
                        elif updated_values[4] == 1 or updated_values[4] == 2:
                            qb_color = QColor(255, 165, 0)
                            back_qb = QColor(50, 20, 0, 150)
                        else:
                            qb_color = QColor(255, 255, 255)
                            back_qb = QColor(50, 50, 50, 150)
                        if updated_values[8] is None or updated_values[8] == "???" or updated_values[8] > 7:
                            fkdr_color = QColor(255, 0, 0)
                            back_fkdr = QColor(50, 0, 0, 150)
                        elif updated_values[8] > 3:
                            fkdr_color = QColor(255, 165, 0)
                            back_fkdr = QColor(50, 20, 0, 150)
                        else:
                            fkdr_color = QColor(255, 255, 255)
                            back_fkdr = QColor(50, 50, 50, 150)
                        language_list = ["ENGLISH", "JAPANESE", "None"]
                        language_list2 = ["ENG", "JP", "none"]
                        if updated_values[5] in language_list:
                            updated_values[5] = language_list2[language_list.index(updated_values[5])]
                        else:
                            updated_values[5] = "oth"
                        
                        if updated_values != None and updated_values[1] != None:
                            # テーブルのセルに更新した値を設定
                            if updated_values[3] != None:
                                if len(updated_values[3]) == 3:
                                    pixmap0 = QPixmap(resource_path(mode_list[updated_values[3][0]]))
                                    pixmap1 = QPixmap(resource_path(mode_list[updated_values[3][1]]))
                                    pixmap2 = QPixmap(resource_path(mode_list[updated_values[3][2]]))
                                elif len(updated_values[3]) == 2:
                                    pixmap0 = QPixmap(resource_path(mode_list[updated_values[3][0]]))
                                    pixmap1 = QPixmap(resource_path(mode_list[updated_values[3][1]]))
                                    pixmap2 = QPixmap(resource_path(mode_list[9]))
                                if len(updated_values[3]) == 1:
                                    pixmap0 = QPixmap(resource_path(mode_list[updated_values[3][0]]))
                                    pixmap1 = QPixmap(resource_path(mode_list[9]))
                                    pixmap2 = QPixmap(resource_path(mode_list[9]))
                            
                            # screen = QDesktopWidget().screenGeometry()
                            # 画像を適切なサイズにスケーリング
                            pixmap0 = pixmap0.scaled(28, 28)
                            pixmap1 = pixmap1.scaled(28, 28)
                            pixmap2 = pixmap2.scaled(28, 28)

                            item = QTableWidgetItem(str(updated_values[7]))
                            item.setForeground(QColor(255, 255, 255))
                            font = item.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item.setFont(font)  # 変更したフォントをセット
                            item.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                            item.setBackground(QColor(50, 50, 50, 150))  # 背景色を設定
                            self.table_widget.setItem(row, 0, item)

                            item1 = QTableWidgetItem(str(updated_values[0]))
                            item1.setForeground(QColor(255, 255, 255))
                            font = item1.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item1.setFont(font)  # 変更したフォントをセット
                            item1.setBackground(QColor(50, 50, 50, 150))  # 背景色を設定
                            self.table_widget.setItem(row, 1, item1)

                            item2 = QTableWidgetItem(f"{int(updated_values[1]*100)}%")
                            item2.setForeground(g_color)
                            font = item2.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item2.setFont(font)  # 変更したフォントをセット
                            item2.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                            item2.setBackground(back_g)  # 背景色を設定
                            self.table_widget.setItem(row, 2, item2)

                            item3 = QTableWidgetItem(str(updated_values[2]))
                            item3.setForeground(ping_color)
                            font = item3.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item3.setFont(font)  # 変更したフォントをセット
                            item3.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                            item3.setBackground(back_ping)  # 背景色を設定
                            self.table_widget.setItem(row, 3, item3)

                            item4 = QTableWidgetItem(str(updated_values[5]))
                            item4.setForeground(QColor(255, 255, 255))
                            font = item4.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item4.setFont(font)  # 変更したフォントをセット
                            item4.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                            item4.setBackground(QColor(50, 50, 50, 150))  # 背景色を設定
                            self.table_widget.setItem(row, 4, item4)

                            label5 = QLabel()
                            label5.setAlignment(Qt.AlignCenter)
                            label5.setPixmap(pixmap0)
                            label5.setStyleSheet("background-color: rgba(50, 50, 50, 150);")
                            self.table_widget.setCellWidget(row, 5, label5)
                            
                            label6 = QLabel()
                            label6.setAlignment(Qt.AlignCenter)
                            label6.setPixmap(pixmap1)
                            label6.setStyleSheet("background-color: rgba(50, 50, 50, 150);")
                            self.table_widget.setCellWidget(row, 6, label6)

                            label7 = QLabel()
                            label7.setAlignment(Qt.AlignCenter)
                            label7.setPixmap(pixmap2)
                            label7.setStyleSheet("background-color: rgba(50, 50, 50, 150);")
                            self.table_widget.setCellWidget(row, 7, label7)

                            item8 = QTableWidgetItem(str(updated_values[4]))
                            item8.setForeground(qb_color)
                            font = item8.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item8.setFont(font)  # 変更したフォントをセット
                            item8.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                            item8.setBackground(back_qb)  # 背景色を設定
                            self.table_widget.setItem(row, 8, item8)

                            item9 = QTableWidgetItem(str(met_num))
                            item9.setForeground(QColor(255, 255, 255))
                            font = item9.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item9.setFont(font)  # 変更したフォントをセット
                            item9.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                            item9.setBackground(QColor(50, 50, 50, 150))  # 背景色を設定
                            self.table_widget.setItem(row, 9, item9)

                            item10 = QTableWidgetItem(str(updated_values[8]))
                            item10.setForeground(fkdr_color)
                            font = item10.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item10.setFont(font)  # 変更したフォントをセット
                            item10.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                            item10.setBackground(back_fkdr)  # 背景色を設定
                            self.table_widget.setItem(row, 10, item10)

                            item11 = QTableWidgetItem(str(updated_values[9]))
                            item11.setForeground(QColor(255, 255, 255))
                            font = item11.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item11.setFont(font)  # 変更したフォントをセット
                            item11.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                            item11.setBackground(QColor(50, 50, 50, 150))  # 背景色を設定
                            self.table_widget.setItem(row, 11, item11)
                        else:
                            item = QTableWidgetItem("???")
                            item.setForeground(QColor(255, 255, 255))
                            font = item.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item.setFont(font)  # 変更したフォントをセット
                            item.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                            item.setBackground(QColor(50, 50, 50, 150))  # 背景色を設定
                            self.table_widget.setItem(row, 0, item)
                            item1 = QTableWidgetItem(str(updated_values[0]))
                            item1.setForeground(g_color)
                            font = item1.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item1.setFont(font)  # 変更したフォントをセット
                            item1.setBackground(QColor(50, 50, 50, 150))  # 背景色を設定
                            self.table_widget.setItem(row, 1, item1)
                            item2 = QTableWidgetItem("???")
                            item2.setForeground(g_color)
                            font = item2.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item2.setFont(font)  # 変更したフォントをセット
                            item2.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                            item2.setBackground(back_g)  # 背景色を設定
                            self.table_widget.setItem(row, 2, item2)
                            item3 = QTableWidgetItem("???")
                            item3.setForeground(ping_color)
                            font = item3.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item3.setFont(font)  # 変更したフォントをセット
                            item3.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                            item3.setBackground(back_ping)  # 背景色を設定
                            self.table_widget.setItem(row, 3, item3)
                            item4 = QTableWidgetItem("???")
                            item4.setForeground(QColor(255, 0, 0))
                            font = item4.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item4.setFont(font)  # 変更したフォントをセット
                            item4.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                            item4.setBackground(QColor(50, 50, 50, 150))  # 背景色を設定
                            self.table_widget.setItem(row, 4, item4)
                            label5 = QLabel()
                            label5.setAlignment(Qt.AlignCenter)
                            label5.setPixmap(pixmap0)
                            label5.setStyleSheet("background-color: rgba(50, 50, 50, 150);")
                            self.table_widget.setCellWidget(row, 5, label5)
                            label6 = QLabel()
                            label6.setAlignment(Qt.AlignCenter)
                            label6.setPixmap(pixmap1)
                            label6.setStyleSheet("background-color: rgba(50, 50, 50, 150);")
                            self.table_widget.setCellWidget(row, 6, label6)
                            label7 = QLabel()
                            label7.setAlignment(Qt.AlignCenter)
                            label7.setPixmap(pixmap2)
                            label7.setStyleSheet("background-color: rgba(50, 50, 50, 150);")
                            self.table_widget.setCellWidget(row, 7, label7)
                            item8 = QTableWidgetItem("???")
                            item8.setForeground(qb_color)
                            font = item8.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item8.setFont(font)  # 変更したフォントをセット
                            item8.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                            item8.setBackground(back_qb)  # 背景色を設定
                            self.table_widget.setItem(row, 8, item8)
                            item9 = QTableWidgetItem(str(met_num))
                            item9.setForeground(QColor(255, 255, 255))
                            font = item9.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item9.setFont(font)  # 変更したフォントをセット
                            item9.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                            item9.setBackground(QColor(50, 50, 50, 150))  # 背景色を設定
                            self.table_widget.setItem(row, 9, item9)
                            item10 = QTableWidgetItem("???")
                            item10.setForeground(fkdr_color)
                            font = item10.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item10.setFont(font)  # 変更したフォントをセット
                            item10.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                            item10.setBackground(back_fkdr)  # 背景色を設定
                            self.table_widget.setItem(row, 10, item10)
                            item11 = QTableWidgetItem("???")
                            item11.setForeground(QColor(255, 0, 0))
                            font = item11.font()  # フォントを取得
                            font.setBold(True)  # フォントを太くする
                            font.setPointSize(font_size)
                            item11.setFont(font)  # 変更したフォントをセット
                            item11.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                            item11.setBackground(QColor(50, 50, 50, 150))  # 背景色を設定
                            self.table_widget.setItem(row, 11, item11)
                        QApplication.processEvents()
                    self.pressed = False
                    self.check = False
            
            def who_checker(self):
                s = f.read()
                # print(s)
                who_players = who(s)
                if who_players != []:
                    self.table_widget.clearContents()
                    self.show()
                auto_players = auto_who(s)
                players = list(set(auto_players+who_players))
                if players != [] and len(players) <= 16:
                    self.pressed = True
                    self.players = players
                    self.check = True

        if __name__ == '__main__':
            app = QApplication(sys.argv)
            ex = DraggableWindow()
            ex.show()
            sys.exit(app.exec_())

def setting():
    try:
        with open(key[3]) as f:
            f.read()
        new_window = antico()
        new_window.show()
    except FileNotFoundError:
        class ErrorWindow(QWidget):
            def __init__(self):
                super().__init__()
                self.installEventFilter(self)

                self.settings_window = None  # 初期化しておく
                self.initUI()  # initUI を呼び出す
            def settings(self):
                screen = QDesktopWidget().screenGeometry()
                self.settings_window = QWidget()
                self.settings_window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 枠を消して最前面に表示する
                self.settings_window.setGeometry(0, 0, 200, 410)  # ウィンドウサイズ
                self.settings_window.setAttribute(Qt.WA_TranslucentBackground)  # 背景を透明にする
                self.settings_window.setWindowIcon(QIcon(resource_path('logo.ico')))  # アイコンを設定
                self.settings_window.setFocus()

                # フレームを作成して黒い枠を設定
                settings_frame = QFrame(self.settings_window)
                settings_frame.setFrameStyle(QFrame.Box)
                settings_frame.setLineWidth(5)
                settings_frame.setStyleSheet("border: 2px solid rgba(200, 200, 200, 250); background-color: rgba(0, 0, 0, 100);")
                settings_frame.setGeometry(0, 0, 200, 410)

                # 閉じるボタンを作成し、右上に配置
                close_button = QPushButton('×', self.settings_window)
                close_button.setGeometry(self.settings_window.width()-40, 0, 40, 30)
                close_button.setStyleSheet("border: 2px solid rgba(200, 200, 200, 250); color: white;")
                close_button.clicked.connect(self.settings_window.close)

                # ラベルを作成してテキストを設定し、ウィンドウに配置
                label = QLabel("SETTINGS", self.settings_window)
                label.setGeometry(10, 10, 60, 30)  # 適切な位置に配置
                label.setStyleSheet("color: white;")

                layout = QVBoxLayout()

                self.input_box_f = QLineEdit(self.settings_window)
                self.input_box_f.setGeometry(10, 40, 70, 30)
                self.input_box_f.setStyleSheet("background-color: rgba(0, 0, 0, 20); color: white;")
                layout.addWidget(self.input_box_f)

                self.button = QPushButton('SET FONT SIZE', self.settings_window)
                self.button.clicked.connect(self.get_font)
                self.button.setGeometry(90, 40, 100, 30)
                self.button.setStyleSheet("background-color: white;")
                layout.addWidget(self.button)

                self.key_label = QLabel('PLESS THE SHOW or HIDE KEY')
                layout.addWidget(self.key_label)

                self.button = QPushButton('PLESS THE SHOW or HIDE KEY', self.settings_window)
                self.button.clicked.connect(self.get_key)
                self.button.setGeometry(10, 80, 180, 30)
                self.button.setStyleSheet("background-color: white;")
                self.button.clicked.connect(self.get_key)
                layout.addWidget(self.button)

                self.input_box = QLineEdit(self.settings_window)
                self.input_box.setGeometry(10, 130, 180, 30)
                self.input_box.setStyleSheet("background-color: rgba(0, 0, 0, 20); color: white;")
                layout.addWidget(self.input_box)

                self.button = QPushButton('SET HYPIXEL API', self.settings_window)
                self.button.setGeometry(10, 165, 180, 30)
                self.button.setStyleSheet("background-color: white;")
                self.button.clicked.connect(self.get_text)
                layout.addWidget(self.button)

                self.input_box2 = QLineEdit(self.settings_window)
                self.input_box2.setGeometry(10, 215, 180, 30)
                self.input_box2.setStyleSheet("background-color: rgba(0, 0, 0, 20); color: white;")
                layout.addWidget(self.input_box2)

                self.button2 = QPushButton('SET POLSU API', self.settings_window)
                self.button2.setGeometry(10, 250, 180, 30)
                self.button2.setStyleSheet("background-color: white;")
                self.button2.clicked.connect(self.get_text_polsu)
                layout.addWidget(self.button2)

                self.button3 = QPushButton('SELECT LOG FILE', self.settings_window)
                self.button3.setGeometry(10, 300, 180, 30)
                self.button3.setStyleSheet("background-color: rgba(240, 200, 200, 250);")
                self.button3.clicked.connect(self.get_file_path)
                layout.addWidget(self.button3)

                self.button4 = QPushButton('EXIT (PLZ RESTART)', self.settings_window)
                self.button4.setGeometry(30, 350, 140, 30)
                self.button4.setStyleSheet("background-color: rgba(150, 150, 150, 250);")
                self.button4.clicked.connect(self.close_window)
                layout.addWidget(self.button4)

                self.settings_window.show()

            def close_window(self):
                self.settings_window.close()
                # new_window = antico()
                # new_window.show()
            def get_key(self):
                self.key_label.setText('Set Key')
                keyboard.on_press(self.on_press)

            def get_font(self):
                key = self.input_box_f.text()
                print("Set Font:", key)
                if key != "":
                    with open('key.json') as k:
                        read_key = json.load(k)
                    read_key[6] = key
                    with open('key.json', 'w') as kk:
                        json.dump(read_key, kk)
            
            def get_file_path(self):
                file_dialog = QFileDialog()
                file_dialog.setFileMode(QFileDialog.AnyFile)
                file_dialog.setViewMode(QFileDialog.Detail)
                if file_dialog.exec_():
                    file_paths = file_dialog.selectedFiles()
                    if len(file_paths) > 0:
                        file_path = file_paths[0]
                        print(file_path)
            
            def get_text(self):
                key = self.input_box.text()
                print("Set HYPIXEL API:", key)
                if key != "":
                    with open('key.json') as k:
                        read_key = json.load(k)
                    read_key[1] = key
                    with open('key.json', 'w') as kk:
                        json.dump(read_key, kk)
            
            def get_text_polsu(self):
                key = self.input_box2.text()
                print("Set POLSU API:", key)
                if key != "":
                    with open('key.json') as k:
                        read_key = json.load(k)
                    read_key[2] = key
                    with open('key.json', 'w') as kk:
                        json.dump(read_key, kk)

            def on_press(self, event):
                key = event.name
                self.key_label.setText(f'Key pressed: {key}')
                keyboard.unhook_all()
                print(f'Set: {key}')
                keyboard.add_hotkey(key, lambda: self.ShowOrHide())
                with open('key.json') as k:
                    read_key = json.load(k)
                read_key[0] = key
                with open('key.json', 'w') as kk:
                    json.dump(read_key, kk)
            
            def get_file_path(self):
                file_dialog = QFileDialog()
                file_dialog.setFileMode(QFileDialog.AnyFile)
                file_dialog.setViewMode(QFileDialog.Detail)
                if file_dialog.exec_():
                    file_paths = file_dialog.selectedFiles()
                    if len(file_paths) > 0:
                        file_path = file_paths[0]
                        print(file_path)
                        with open('key.json') as k:
                            read_key = json.load(k)
                        read_key[3] = file_path
                        with open('key.json', 'w') as kk:
                            json.dump(read_key, kk)

            def initUI(self):
                self.settings()

        if __name__ == '__main__':
            app = QApplication(sys.argv)
            window = ErrorWindow()
            sys.exit(app.exec_())

setting()
# name = "Gokiton"
# model = joblib.load(resource_path('Cheater.pkl'))
# scaler = joblib.load(resource_path('scaler.joblib'))
# print(checker(name, model, scaler))