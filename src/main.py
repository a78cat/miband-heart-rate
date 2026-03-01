import logging
import sys

from PySide6.QtWidgets import QApplication
from src.control.ctrl_main import MainApp

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainApp()
    ui.show()
    sys.exit(app.exec())
