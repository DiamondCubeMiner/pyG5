"""
Created on 30 Jul 2026.

@author: Ben Lauret
"""

__version__ = "0.0.4"
__appName__ = "pyG5"

import argparse
import logging
import sys
import platform


from PySide6.QtCore import (
    Qt,
    QTimer,
    QCoreApplication,
    QSettings,
    Signal,
)
from PySide6.QtWidgets import QApplication

from pyG5.pyG5Network import pyG5NetWorkManager
from pyG5.pyG5View import pyG5AIWidget
from pyG5.pyG5Main import pyG5BaseWindow


class pyG5AIApp(QApplication):
    """pyG5AIApp PySide6 application.

    Args:
        sys.argv

    Returns:
        self
    """

    def __init__(self):
        """g5Widget Constructor.

        Args:
            parent: Parent Widget

        Returns:
            self
        """
        QApplication.__init__(self, sys.argv)

        QCoreApplication.setOrganizationName("pyG5")
        QCoreApplication.setOrganizationDomain("pyg5.org")
        QCoreApplication.setApplicationName("pyG5")
        self.settings = QSettings(
            QSettings.Format.IniFormat,
            QSettings.Scope.UserScope,
            QCoreApplication.organizationDomain(),
            "pyG5",
        )

        # parse the command line arguments
        self.argument_parser()

        # set the verbosity
        if self.args.verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        logging.info("{} v{}".format(self.__class__.__name__, __version__))

        self.networkManager = pyG5NetWorkManager()

        self.paintTimer = QTimer()
        self.paintTimer.timeout.connect(
            self.painTimerCB
        )  # Let the interpreter run each 500 ms.
        self.paintTimer.start(25)  # You may change this if you wish.

        # The QWidget widget is the base class of all user interface objects in PySide6.
        self.mainWindow = pyG5AIWindow()

        self.networkManager.drefUpdate.connect(
            self.mainWindow.pyG5AIWidget.drefHandler
        )

        # Show window
        self.mainWindow.loadSettings()

        if platform.machine() == "aarch64":
            self.mainWindow.setWindowFlags(
                self.mainWindow.windowFlags() | Qt.FramelessWindowHint
            )
            self.mainWindow.setWindowState(Qt.WindowFullScreen)

        self.mainWindow.show()

    def painTimerCB(self):
        """Trigger update of all the widgets."""
        self.mainWindow.pyG5AIWidget.update()

    def argument_parser(self):
        """Initialize the arguments passed from the command line."""
        self.parser = argparse.ArgumentParser(
            description="{} Application v{}".format(__appName__, __version__)
        )
        self.parser.add_argument(
            "-v", "--verbose", help="increase verbosity", action="store_true"
        )

        self.args = self.parser.parse_args()


class pyG5AIWindow(pyG5BaseWindow):
    """pyG5AIApp PySide6 application.

    Args:
        sys.argv

    Returns:
        self
    """

    closed = Signal()

    def __init__(self, parent=None):
        """g5Widget Constructor.

        Args:
            parent: Parent Widget

        Returns:
            self
        """
        pyG5BaseWindow.__init__(self, parent)

        self.pyG5AI = pyG5AIWidget()

        self.setCentralWidget(self.pyG5AI)


if __name__ == "__main__":
    """Main application."""
    a = pyG5AIApp()

    sys.exit(a.exec())

    pass
