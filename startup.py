from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSplashScreen


class StartupWindow(QSplashScreen):
    def __init__(self):
        super(StartupWindow, self).__init__(QPixmap(":/assets/splash.png").scaled(640, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation), Qt.WindowStaysOnTopHint)
        self.setEnabled(False)
        self.show()
        QTimer.singleShot(3000, self.close)