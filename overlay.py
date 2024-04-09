import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QLabel
from PyQt5.QtCore import Qt, QPoint, QTimer, QEvent
from PyQt5.QtGui import QColor, QIcon, QPixmap
import joblib
import concurrent.futures
import json
import keyboard

from who import checker

# path = r"/Users/chinq500/Library/Application Support/minecraft/versions/1.8.9/logs/latest.log"
path = r"C:/Users/Owner/AppData/Roaming/.minecraft/logs/blclient/minecraft/latest.log"
with open('met_player.json', 'w') as f:
    json.dump({}, f, indent=4)

with open('table.json', 'w') as w1:
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
        if " が参加しました (" in item:
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
    
with open(path) as f:
    f.read()
    class DraggableWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.initUI()
            self.installEventFilter(self)
            keyboard.add_hotkey('f5', lambda: self.ShowOrHide())
            self.f5_disabled = False

        def ShowOrHide(self):
            if not self.f5_disabled:
                if self.isHidden():
                    print("show")
                    self.show()
                else:
                    print("hide")
                    self.hide()

        def initUI(self):
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 枠を消して最前面に表示する
            self.setGeometry(0, 0, 400, 380)  # ウィンドウサイズ
            self.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")
            self.setAttribute(Qt.WA_TranslucentBackground)  # 背景を透明にする
            self.setWindowIcon(QIcon('logo.ico'))  # アイコンを設定
            self.oldPos = self.pos()  # ウィンドウの初期位置
            self.f5_pressed = False  # f5_pressed属性を追加
            self.setFocus()
            
            # テーブルウィジェットを作成して内容を追加
            self.table_widget = QTableWidget(self)
            self.table_widget.setStyleSheet(
                "QHeaderView::section {"
                "    background-color: rgba(255, 255, 255, 0.2);"
                "    color: white;"
                "}"
            )
            self.table_widget.setColumnCount(9)  # 7つのカラムを持つ
            self.table_widget.setHorizontalHeaderLabels(["MCID", "G%", "PING", "LG", "1", "2", "3", "QB", "MET"])  # カラムのヘッダー
            list_num = 16
            self.table_widget.setRowCount(list_num)  # 16行に変更
            self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)
            total_width = 400
            self.table_widget.setColumnWidth(0, 110)
            self.table_widget.setColumnWidth(1, 30)
            self.table_widget.setColumnWidth(2, 20)
            self.table_widget.setColumnWidth(3, 50)
            self.table_widget.setColumnWidth(4, 20)
            self.table_widget.setColumnWidth(5, 20)
            self.table_widget.setColumnWidth(6, 20)
            self.table_widget.setColumnWidth(7, 20)
            self.table_widget.setColumnWidth(8, 20)
            self.table_widget.setColumnWidth(9, 20)

            # 以下、追加した行のデータを設定
            for i in range(list_num):
                self.table_widget.setRowHeight(i, 20)
                
            
            self.table_widget.setGeometry(0, 30, 400, 345)  # 位置とサイズを設定
            self.table_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); color: white;")
            self.table_widget.verticalHeader().setVisible(False)  # 垂直ヘッダーを非表示にする

            # 更新タイマーを設定して定期的にテーブルを更新
            self.update_timer = QTimer(self)
            self.update_timer.timeout.connect(self.update_table)
            self.update_timer.start(1000)  # 1秒ごとに更新

            # 更新タイマーを設定して定期的にテーブルを更新
            self.reset_timer = QTimer(self)
            self.reset_timer.timeout.connect(self.reset_json)
            self.reset_timer.start(60000)  # 1分ごとに更新

            # 閉じるボタン
            self.closeButton = QPushButton('×', self)
            self.closeButton.setGeometry(self.width()-40, 0, 40, 30)
            self.closeButton.setStyleSheet("border: 2px solid rgba(200, 200, 200, 250); color: white;")
            self.closeButton.clicked.connect(self.close)

            # フレームを作成して黒い枠を設定
            frame = QFrame(self)
            frame.setFrameStyle(QFrame.Box)
            frame.setLineWidth(5)
            frame.setStyleSheet("border: 2px solid rgba(200, 200, 200, 250);")
            frame.setGeometry(0, 0, 360, 30)

            # 画像を表示するための QLabel を作成し、親を frame に設定
            image_label = QLabel(frame)
            # 画像を読み込む
            pixmap = QPixmap('logo_white.png')
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

            # レイアウトを設定
            layout = QVBoxLayout(self)
            # layout.addWidget(frame)
            layout.setContentsMargins(0, 0, 0, 0)
            self.setLayout(layout)

        def mousePressEvent(self, event):
            if event.button() == Qt.LeftButton:
                self.oldPos = event.globalPos()  # クリック時のマウス位置を取得

        def mouseMoveEvent(self, event):
            if event.buttons() == Qt.LeftButton:
                delta = QPoint(event.globalPos() - self.oldPos)  # 移動量を計算
                self.move(self.x() + delta.x(), self.y() + delta.y())  # ウィンドウを移動
                self.oldPos = event.globalPos()  # 新しい位置を保存
        def reset_json(self):
            with open('table.json', 'w') as w3:
                json.dump([], w3)
        def update_table(self):
            model = joblib.load('Cheater.pkl')
            scaler = joblib.load('scaler.joblib')
            mode_list = ["bed.png", "eye.png", "tnt.png", "gapple.png", "bow.png", "bench.png", "fishing.png", "hub.png", "dirt.png", "none.png"]
            # checker関数を使ってログ内容から更新する値を取得
            s = f.read()
            values = []
            players = who(s)
            if players != []:
                with open('table.json') as r:
                    li = json.load(r)
                    for l in li:
                        if l[0] in players:
                            players.remove(l[0])
                            values.append(l)
                self.f5_disabled = True
                self.table_widget.clearContents()
                self.show()
                print(players)
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    return_value = list(executor.map(lambda mcid: checker(mcid, model, scaler), players))
                    values += return_value
                with open('table.json', 'wt') as w2:
                    json.dump(return_value, w2, indent=4)
                for num, updated_values in enumerate(values):
                    # print(updated_values, type(updated_values))
                    met_num = 0
                    with open('met_player.json') as r:
                        di = json.load(r)
                        if updated_values[6] != None:
                            if updated_values[6] in di:
                                met_num = di[updated_values[6]]
                                di[updated_values[6]] += 1
                            else:
                                di[updated_values[6]] = 1
                            with open('met_player.json', 'w') as w:
                                json.dump(di, w, indent=4)
                    # print(updated_values)
                    pixmap0 = QPixmap(f"images/{mode_list[9]}")
                    pixmap1 = QPixmap(f"images/{mode_list[9]}")
                    pixmap2 = QPixmap(f"images/{mode_list[9]}")
                    pixmap0 = pixmap0.scaled(23, 23)
                    pixmap1 = pixmap1.scaled(23, 23)
                    pixmap2 = pixmap2.scaled(23, 23)

                    if updated_values[1] == None or updated_values[1] == "???" or float(updated_values[1]) >= 0.9:
                        g_color = QColor(255, 0, 0)
                        back_g = QColor(200, 0, 0, 30)
                    elif updated_values[1] >= 0.6:
                        g_color = QColor(255, 165, 0)
                        back_g = QColor(200, 135, 0, 30)
                    else:
                        g_color = QColor(255, 255, 255)
                        back_g = QColor(200, 200, 200, 30)
                    if updated_values[2] == None or updated_values[2] == "???" or updated_values[2] > 230:
                        ping_color = QColor(255, 0, 0)
                        back_ping = QColor(200, 0, 0, 30)
                    elif 170 <= updated_values[2] <= 230:
                        ping_color = QColor(255, 165, 0)
                        back_ping = QColor(200, 135, 0, 30)
                    else:
                        ping_color = QColor(255, 255, 255)
                        back_ping = QColor(200, 200, 200, 30)
                    if updated_values[4] == None or updated_values[4] == "???":
                        qb_color = QColor(255, 0, 0)
                        back_qb = QColor(200, 0, 0, 30)
                        updated_values[4] = "???"
                    elif updated_values[4] <= 2:
                        qb_color = QColor(255, 0, 0)
                        back_qb = QColor(200, 0, 0, 50)
                    elif updated_values[2] == 1:
                        qb_color = QColor(255, 165, 0)
                        back_qb = QColor(200, 135, 0, 30)
                    else:
                        qb_color = QColor(255, 255, 255)
                        back_qb = QColor(200, 200, 200, 30)
                    if updated_values != None and updated_values[1] != None:
                        # テーブルのセルに更新した値を設定
                        if updated_values[3] != None:
                            if len(updated_values[3]) == 3:
                                pixmap0 = QPixmap(f"images/{mode_list[updated_values[3][0]]}")
                                pixmap1 = QPixmap(f"images/{mode_list[updated_values[3][1]]}")
                                pixmap2 = QPixmap(f"images/{mode_list[updated_values[3][2]]}")
                            elif len(updated_values[3]) == 2:
                                pixmap0 = QPixmap(f"images/{mode_list[updated_values[3][0]]}")
                                pixmap1 = QPixmap(f"images/{mode_list[updated_values[3][1]]}")
                                pixmap2 = QPixmap(f"images/{mode_list[9]}")
                            if len(updated_values[3]) == 1:
                                pixmap0 = QPixmap(f"images/{mode_list[updated_values[3][0]]}")
                                pixmap1 = QPixmap(f"images/{mode_list[9]}")
                                pixmap2 = QPixmap(f"images/{mode_list[9]}")

                        # 画像を適切なサイズにスケーリング
                        pixmap0 = pixmap0.scaled(23, 23)
                        pixmap1 = pixmap1.scaled(23, 23)
                        pixmap2 = pixmap2.scaled(23, 23)
                        
                        item1 = QTableWidgetItem(str(updated_values[0]))
                        item1.setForeground(QColor(255, 255, 255))
                        font = item1.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(9)
                        item1.setFont(font)  # 変更したフォントをセット
                        item1.setBackground(QColor(255, 255, 255, 30))  # 背景色を設定
                        self.table_widget.setItem(num, 0, item1)

                        item2 = QTableWidgetItem(f"{int(updated_values[1]*100)}%")
                        item2.setForeground(g_color)
                        font = item2.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(10)
                        item2.setFont(font)  # 変更したフォントをセット
                        item2.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                        item2.setBackground(back_g)  # 背景色を設定
                        self.table_widget.setItem(num, 1, item2)

                        item3 = QTableWidgetItem(str(updated_values[2]))
                        item3.setForeground(ping_color)
                        font = item3.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(11)
                        item3.setFont(font)  # 変更したフォントをセット
                        item3.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                        item3.setBackground(back_ping)  # 背景色を設定
                        self.table_widget.setItem(num, 2, item3)

                        item4 = QTableWidgetItem(str(updated_values[5]))
                        item4.setForeground(QColor(255, 255, 255))
                        font = item4.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(7)
                        item4.setFont(font)  # 変更したフォントをセット
                        item4.setBackground(QColor(255, 255, 255, 30))  # 背景色を設定
                        self.table_widget.setItem(num, 3, item4)

                        label5 = QLabel()
                        label5.setAlignment(Qt.AlignCenter)
                        label5.setPixmap(pixmap0)
                        self.table_widget.setCellWidget(num, 4, label5)
                        
                        label6 = QLabel()
                        label6.setAlignment(Qt.AlignCenter)
                        label6.setPixmap(pixmap1)
                        self.table_widget.setCellWidget(num, 5, label6)

                        label7 = QLabel()
                        label7.setAlignment(Qt.AlignCenter)
                        label7.setPixmap(pixmap2)
                        self.table_widget.setCellWidget(num, 6, label7)

                        item8 = QTableWidgetItem(str(updated_values[4]))
                        item8.setForeground(qb_color)
                        font = item8.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(11)
                        item8.setFont(font)  # 変更したフォントをセット
                        item8.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                        item8.setBackground(back_qb)  # 背景色を設定
                        self.table_widget.setItem(num, 7, item8)

                        item9 = QTableWidgetItem(str(met_num))
                        item9.setForeground(QColor(255, 255, 255))
                        font = item9.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(11)
                        item9.setFont(font)  # 変更したフォントをセット
                        item9.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                        item9.setBackground(QColor(255, 255, 255, 30))  # 背景色を設定
                        self.table_widget.setItem(num, 8, item9)
                    else:
                        item1 = QTableWidgetItem(str(updated_values[0]))
                        item1.setForeground(g_color)
                        font = item1.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(9)
                        item1.setFont(font)  # 変更したフォントをセット
                        item1.setBackground(QColor(255, 255, 255, 30))  # 背景色を設定
                        self.table_widget.setItem(num, 0, item1)
                        item2 = QTableWidgetItem("???")
                        item2.setForeground(g_color)
                        font = item2.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(10)
                        item2.setFont(font)  # 変更したフォントをセット
                        item2.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                        item2.setBackground(back_g)  # 背景色を設定
                        self.table_widget.setItem(num, 1, item2)
                        item3 = QTableWidgetItem("???")
                        item3.setForeground(ping_color)
                        font = item3.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(11)
                        item3.setFont(font)  # 変更したフォントをセット
                        item3.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                        item3.setBackground(back_ping)  # 背景色を設定
                        self.table_widget.setItem(num, 2, item3)
                        item4 = QTableWidgetItem("???")
                        item4.setForeground(QColor(255, 255, 255))
                        font = item4.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(7)
                        item4.setFont(font)  # 変更したフォントをセット
                        item4.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                        item4.setBackground(QColor(255, 255, 255, 30))  # 背景色を設定
                        self.table_widget.setItem(num, 3, item4)
                        label5 = QLabel()
                        label5.setAlignment(Qt.AlignCenter)
                        label5.setPixmap(pixmap0)
                        self.table_widget.setCellWidget(num, 4, label5)
                        label6 = QLabel()
                        label6.setAlignment(Qt.AlignCenter)
                        label6.setPixmap(pixmap1)
                        self.table_widget.setCellWidget(num, 5, label6)
                        label7 = QLabel()
                        label7.setAlignment(Qt.AlignCenter)
                        label7.setPixmap(pixmap2)
                        self.table_widget.setCellWidget(num, 6, label7)
                        item8 = QTableWidgetItem("???")
                        item8.setForeground(qb_color)
                        font = item8.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(11)
                        item8.setFont(font)  # 変更したフォントをセット
                        item8.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                        item8.setBackground(back_qb)  # 背景色を設定
                        self.table_widget.setItem(num, 7, item8)
                        item9 = QTableWidgetItem(str(met_num))
                        item9.setForeground(QColor(255, 255, 255))
                        font = item9.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(11)
                        item9.setFont(font)  # 変更したフォントをセット
                        item9.setTextAlignment(Qt.AlignCenter)  # テキストを中央に配置
                        item9.setBackground(QColor(255, 255, 255, 30))  # 背景色を設定
                        self.table_widget.setItem(num, 8, item9)
                    QApplication.processEvents()
                self.f5_disabled = False

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = DraggableWindow()
        ex.show()
        sys.exit(app.exec_())