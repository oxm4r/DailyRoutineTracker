import sys, os, json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QListWidget,
    QPushButton, QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

DATA_FILE = "routine_data.json"

def load_data():
    return json.load(open(DATA_FILE, "r", encoding="utf-8")) if os.path.exists(DATA_FILE) else {"today": [], "previous": []}

def save_data(data):
    json.dump(data, open(DATA_FILE, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

class RoutineApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📅 My Routine")
        self.setGeometry(200, 150, 360, 480)
        self.setStyleSheet("background: #f4f4f4;")   # Solid background

        self.data = load_data()
        font = QFont("Segoe UI", 10)

        layout = QVBoxLayout()

        # Title
        title = QLabel("✨ Today ✨", alignment=Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title.setStyleSheet("color:#333; background:#ddd; padding:6px; border-radius:6px;")
        layout.addWidget(title)

        # Today's list
        self.today = QListWidget(font=font, styleSheet="background:#fff; border:1px solid #ccc; border-radius:6px;")
        layout.addWidget(self.today)

        # Buttons
        for text, color, action in [
            ("➕ Add", "#4CAF50", self.add_task),
            ("✅ Done", "#2196F3", self.mark_done),
        ]:
            btn = QPushButton(text, clicked=action)
            btn.setStyleSheet(f"background:{color}; color:white; border:none; border-radius:6px; padding:6px;")
            layout.addWidget(btn)

        # Previous
        prev_label = QLabel("📚 Previous", alignment=Qt.AlignCenter)
        prev_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        prev_label.setStyleSheet("color:#333; background:#ddd; padding:6px; border-radius:6px;")
        layout.addWidget(prev_label)

        self.prev = QListWidget(font=font, styleSheet="background:#fff; border:1px solid #ccc; border-radius:6px;")
        layout.addWidget(self.prev)

        self.setLayout(layout)
        self.load_tasks()

    def load_tasks(self):
        self.today.clear(), self.prev.clear()
        self.today.addItems(self.data["today"])
        self.prev.addItems(self.data["previous"])

    def add_task(self):
        text, ok = QInputDialog.getText(self, "New Task", "Enter task:")
        if ok and text.strip():
            self.data["today"].append(text.strip())
            save_data(self.data)
            self.load_tasks()

    def mark_done(self):
        item = self.today.currentItem()
        if not item:
            QMessageBox.warning(self, "⚠️ No Task", "Select a task first!")
            return
        task = item.text()
        self.data["today"].remove(task)
        self.data["previous"].append(task)
        save_data(self.data)
        self.load_tasks()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = RoutineApp()
    win.show()
    sys.exit(app.exec_())
