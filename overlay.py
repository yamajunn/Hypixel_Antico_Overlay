import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QColor, QIcon
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
            self.table_widget.setColumnCount(3)  # 2つのカラムを持つ
            self.table_widget.setHorizontalHeaderLabels(["MCID", "CHEAT", "PING"])  # カラムのヘッダー
            list_num = 16
            self.table_widget.setRowCount(list_num)  # 16行に変更
            self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)
            total_width = 400
            column_width = total_width // 3
            self.table_widget.setColumnWidth(0, column_width)
            self.table_widget.setColumnWidth(1, column_width)
            self.table_widget.setColumnWidth(2, column_width-1)

            # 以下、追加した行のデータを設定
            for i in range(list_num):
                mcid = QTableWidgetItem("")
                mcid.setFlags(mcid.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(i, 0, mcid)
                cheater = QTableWidgetItem("")
                cheater.setFlags(cheater.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(i, 1, cheater)
                ping = QTableWidgetItem("")
                ping.setFlags(ping.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(i, 2, ping)

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
                    if updated_values != None:
                        # テーブルのセルに更新した値を設定
                        if updated_values[1] == None or updated_values[1] >= 0.9:
                            color = QColor(255, 0, 0)
                        else:
                            color = QColor(255, 255, 255)
                        
                        item = QTableWidgetItem(str(updated_values[0]))
                        item.setForeground(color)
                        font = item.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(12)
                        item.setFont(font)  # 変更したフォントをセット
                        self.table_widget.setItem(num, 0, item)

                        item2 = QTableWidgetItem(f"{round(updated_values[1]*100, 2)}%")
                        item2.setForeground(color)
                        font = item2.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(11)
                        item2.setFont(font)  # 変更したフォントをセット
                        self.table_widget.setItem(num, 1, item2)

                        item3 = QTableWidgetItem(str(updated_values[2]))
                        item3.setForeground(color)
                        font = item3.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(11)
                        item3.setFont(font)  # 変更したフォントをセット
                        self.table_widget.setItem(num, 2, item3)
                    else:
                        item = QTableWidgetItem(str(players[num]))
                        item.setForeground(QColor(255, 0, 0))
                        font = item.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(12)
                        item.setFont(font)  # 変更したフォントをセット
                        self.table_widget.setItem(num, 0, item)
                        item2 = QTableWidgetItem("???")
                        item2.setForeground(QColor(255, 0, 0))
                        font = item2.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(11)
                        item2.setFont(font)  # 変更したフォントをセット
                        self.table_widget.setItem(num, 1, item2)
                        item3 = QTableWidgetItem("???")
                        item3.setForeground(QColor(255, 0, 0))
                        font = item3.font()  # フォントを取得
                        font.setBold(True)  # フォントを太くする
                        font.setPointSize(11)
                        item3.setFont(font)  # 変更したフォントをセット
                        self.table_widget.setItem(num, 2, item3)
                    QApplication.processEvents()
                    num += 1

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = DraggableWindow()
        ex.show()
        sys.exit(app.exec_())
