from PyQt5 import QtGui, QtWidgets, QtCore
from settings.settings import current_settings


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        icon = QtGui.QIcon("./assets/discord_icon.png")
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.parent = parent
        menu = QtWidgets.QMenu(parent)
        
        hideAction = menu.addAction("Hide/Show")
        hideAction.triggered.connect(self.hide_show)
        
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self.exit)

        self.setContextMenu(menu)
        self.activated.connect(self.open_settings)


    def hide_show(self):
        print("Hide show")
        if self.parent.isVisible():
            self.parent.hide()
        else:
            self.parent.show()


    def open_settings(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.parent.show_settings()


    def exit(self):
        current_settings.save_data()
        QtCore.QCoreApplication.exit()