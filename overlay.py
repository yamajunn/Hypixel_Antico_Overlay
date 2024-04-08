import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QLabel
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QColor, QIcon, QPixmap
import joblib
import concurrent.futures

from who import checker

# path = r"/Users/chinq500/Library/Application Support/minecraft/versions/1.8.9/logs/latest.log"
path = r"C:/Users/Owner/AppData/Roaming/.minecraft/logs/blclient/minecraft/latest.log"

def who(s):
    l = s.split("\n")
    who_list = []
    for item in l:
        if item[40:47] == "ONLINE:":
            who_list = item[48:].split(", ")
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

        def initUI(self):
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 枠を消して最前面に表示する
            self.setGeometry(0, 0, 400, 380)  # ウィンドウサイズ
            self.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")
            self.setAttribute(Qt.WA_TranslucentBackground)  # 背景を透明にする
            self.setWindowIcon(QIcon('logo.ico'))  # アイコンを設定
            self.oldPos = self.pos()  # ウィンドウの初期位置
            
            # テーブルウィジェットを作成して内容を追加
            self.table_widget = QTableWidget(self)
            self.table_widget.setStyleSheet(
                "QHeaderView::section {"
                "    background-color: rgba(255, 255, 255, 0.2);"
                "    color: white;"
                "}"
            )
            self.table_widget.setColumnCount(8)  # 7つのカラムを持つ
            self.table_widget.setHorizontalHeaderLabels(["MCID", "CHEAT", "PING", "LG", "1", "2", "3", "SHOP"])  # カラムのヘッダー
            list_num = 16
            self.table_widget.setRowCount(list_num)  # 16行に変更
            self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)
            total_width = 400
            self.table_widget.setColumnWidth(0, 110)
            self.table_widget.setColumnWidth(1, 50)
            self.table_widget.setColumnWidth(2, 40)
            self.table_widget.setColumnWidth(3, 50)
            self.table_widget.setColumnWidth(4, 25)
            self.table_widget.setColumnWidth(5, 25)
            self.table_widget.setColumnWidth(6, 25)
            self.table_widget.setColumnWidth(7, 25)
            self.table_widget.setColumnWidth(8, 25)

            # 以下、追加した行のデータを設定
            for i in range(list_num):
                mcid = QTableWidgetItem("G")
                mcid.setFlags(mcid.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(i, 0, mcid)
                cheater = QTableWidgetItem("O")
                cheater.setFlags(cheater.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(i, 1, cheater)
                ping = QTableWidgetItem("K")
                ping.setFlags(ping.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(i, 2, ping)
                mode = QTableWidgetItem("I")
                mode.setFlags(mode.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(i, 3, mode)
                mode = QTableWidgetItem("B")
                mode.setFlags(mode.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(i, 4, mode)
                mode = QTableWidgetItem("U")
                mode.setFlags(mode.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(i, 5, mode)
                mode = QTableWidgetItem("R")
                mode.setFlags(mode.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(i, 6, mode)
                mode = QTableWidgetItem("I")
                mode.setFlags(mode.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(i, 6, mode)

                self.table_widget.setRowHeight(i, 20)
                
            
            self.table_widget.setGeometry(0, 30, 400, 345)  # 位置とサイズを設定
            self.table_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); color: white;")
            self.table_widget.verticalHeader().setVisible(False)  # 垂直ヘッダーを非表示にする

            # 更新タイマーを設定して定期的にテーブルを更新
            self.update_timer = QTimer(self)
            self.update_timer.timeout.connect(self.update_table)
            self.update_timer.start(1000)  # 1秒ごとに更新

            # 閉じるボタン
            self.closeButton = QPushButton('×', self)
            self.closeButton.setGeometry(self.width()-40, 0, 40, 30)
            self.closeButton.setStyleSheet("border: 2px solid rgba(200, 200, 200, 250); color: white;")
            self.closeButton.clicked.connect(self.close)

            # フレームを作成して黒い枠を設定
            frame = QFrame(self)
            frame.setFrameStyle(QFrame.Box)
            frame.setLineWidth(5)
            frame.setStyleSheet("border: 2px solid rgba(255, 255, 255, 0.3);")
            frame.setGeometry(0, 0, 360, 30)

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

        def update_table(self):
            model = joblib.load('Cheater.pkl')
            scaler = joblib.load('scaler.joblib')
            mode_list = ["bed.png", "eye.png", "tnt.png", "gapple.png", "bow.png", "bench.png", "fishing.png", "hub.png", "dirt.png", "none.png"]
            # checker関数を使ってログ内容から更新する値を取得
            s = f.read()
            players = who(s)
            if players != []:
                self.table_widget.clearContents()
                num = 0
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    return_values = list(executor.map(lambda mcid: checker(mcid, model, scaler), players))
                for num, updated_values in enumerate(return_values):
                    print(updated_values)
                    pixmap0 = QPixmap(f"images/{mode_list[9]}")
                    pixmap1 = QPixmap(f"images/{mode_list[9]}")
                    pixmap2 = QPixmap(f"images/{mode_list[9]}")
                    pixmap0 = pixmap0.scaled(23, 23)
                    pixmap1 = pixmap1.scaled(23, 23)
                    pixmap2 = pixmap2.scaled(23, 23)

                    if updated_values[1] == None or updated_values[1] >= 0.9:
                        color = QColor(255, 0, 0)
                    else:
                        color = QColor(255, 255, 255)
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
                        
                        item = QTableWidgetItem(str(updated_values[0]))
                        item.setForeground(color)
                        font = item.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(9)
                        item.setFont(font)  # 変更したフォントをセット
                        self.table_widget.setItem(num, 0, item)

                        item2 = QTableWidgetItem(f"{int(updated_values[1]*100)}%")
                        item2.setForeground(color)
                        font = item2.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(7)
                        item2.setFont(font)  # 変更したフォントをセット
                        self.table_widget.setItem(num, 1, item2)

                        item3 = QTableWidgetItem(str(updated_values[2]))
                        item3.setForeground(color)
                        font = item3.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(7)
                        item3.setFont(font)  # 変更したフォントをセット
                        self.table_widget.setItem(num, 2, item3)

                        item4 = QTableWidgetItem(str(updated_values[5]))
                        item4.setForeground(color)
                        font = item4.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(7)
                        item4.setFont(font)  # 変更したフォントをセット
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

                        item7 = QTableWidgetItem(str(updated_values[4]))
                        item7.setForeground(color)
                        font = item7.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(7)
                        item7.setFont(font)  # 変更したフォントをセット
                        self.table_widget.setItem(num, 7, item7)
                    else:
                        item = QTableWidgetItem(str(players[num]))
                        item.setForeground(QColor(255, 0, 0))
                        font = item.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(9)
                        item.setFont(font)  # 変更したフォントをセット
                        self.table_widget.setItem(num, 0, item)
                        item2 = QTableWidgetItem("???")
                        item2.setForeground(QColor(255, 0, 0))
                        font = item2.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(7)
                        item2.setFont(font)  # 変更したフォントをセット
                        self.table_widget.setItem(num, 1, item2)
                        item3 = QTableWidgetItem("???")
                        item3.setForeground(QColor(255, 0, 0))
                        font = item3.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(7)
                        item3.setFont(font)  # 変更したフォントをセット
                        self.table_widget.setItem(num, 2, item3)
                        item4 = QTableWidgetItem("???")
                        item4.setForeground(color)
                        font = item4.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(7)
                        item4.setFont(font)  # 変更したフォントをセット
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
                        item8.setForeground(color)
                        font = item8.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(7)
                        item8.setFont(font)  # 変更したフォントをセット
                        self.table_widget.setItem(num, 7, item8)
                    QApplication.processEvents()
                    num += 1

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = DraggableWindow()
        ex.show()
        sys.exit(app.exec_())
