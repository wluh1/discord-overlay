import sys

from PyQt5 import QtGui

from tray_icon.system_tray_icon import SystemTrayIcon
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow


def main():
    # Start the app
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("assets/discord_icon.ico"))

    main_window = MainWindow()
    main_window.show()

    # Set tray icon
    trayIcon = SystemTrayIcon(None, main_window)
    trayIcon.show()

    sys.exit(app.exec_())


main()