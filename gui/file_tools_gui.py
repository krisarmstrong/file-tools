import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QFileDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)
from PyQt6.QtGui import QPalette, QColor


class SortSentinel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SortSentinel 🛡️ - File Organizer")
        self.setGeometry(100, 100, 800, 600)
        self.set_dark_theme()
        layout = QVBoxLayout()

        self.label = QLabel("🧠 Drop a folder or click 'Choose Folder' to scan")
        layout.addWidget(self.label)

        self.btn = QPushButton("Choose Folder")
        self.btn.clicked.connect(self.choose_folder)
        layout.addWidget(self.btn)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Original Name", "Suggested Name"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        self.export_btn = QPushButton("Export Suggestions (.csv)")
        self.export_btn.clicked.connect(self.export_csv)
        layout.addWidget(self.export_btn)

        self.setLayout(layout)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.label.setText(f"Selected: {folder}")
            self.populate_preview(folder)

    def populate_preview(self, folder):
        self.table.setRowCount(0)
        for f in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, f)):
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(f))
                self.table.setItem(row, 1, QTableWidgetItem("suggested_" + f))

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Rename Plan", "", "CSV Files (*.csv)")
        if path:
            with open(path, "w") as f:
                f.write("Original,Suggested\n")
                for row in range(self.table.rowCount()):
                    orig = self.table.item(row, 0).text()
                    sugg = self.table.item(row, 1).text()
                    f.write(f"{orig},{sugg}\n")
            QMessageBox.information(self, "Exported", f"Plan saved to {path}")

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#121212"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#1e1e1e"))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#2b2b2b"))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.Button, QColor("#1e1e1e"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.BrightText, QColor("#ff0000"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#007acc"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
        self.setPalette(palette)


def run_gui():
    app = QApplication(sys.argv)
    window = SortSentinel()
    window.show()
    sys.exit(app.exec())
