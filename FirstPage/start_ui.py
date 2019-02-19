import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTextEdit, QComboBox, QRadioButton, \
    QDesktopWidget


class Button(QPushButton):

    def __init__(self, x, y, text, parent=None):
        super(Button, self).__init__(parent)
        self.setText(text)
        self.setGeometry(x, y, 170, 50)
        self.setStyleSheet("QPushButton { "
                           "font-size: 20px;"
                           "color: rgba(1, 1, 1, 0.7);"
                           "border: 2px solid #8f8f91; "
                           "border-radius: 6px; "
                           "background-color: rgba(255, 255, 255, 0.3); "
                           "min-width: 80px;} "
                           "QPushButton:hover { "
                           "background-color: rgba(255, 255, 255, 0.5);}"
                           "QPushButton:pressed { "
                           "background-color: rgba(255, 255, 255, 0.7);} "
                           "QPushButton:flat { "
                           "border: none; /* no border for a flat push button */} "
                           "QPushButton:default { "
                           "border-color: navy; /* make the default button prominent */}")


class Text(QTextEdit):

    def __init__(self, x, y, text, parent=None):
        super(Text, self).__init__(parent)
        self.setPlaceholderText(text)
        self.setGeometry(x, y, 180, 30)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.setStyleSheet("QTextEdit {"
                           "border: 0px solid black;"
                           "border-bottom: 1px solid rgba(0, 0, 0, 0.7);"
                           "color: rgba(255, 255, 255, 0.7);"
                           "background-color: rgba(0, 0, 0, 0);"
                           "font-size: 17px;}")


class Label(QLabel):

    def __init__(self, x, y, text, parent=None):
        super(Label, self).__init__(parent)
        self.setText(text)
        self.setGeometry(x, y, 200, 30)
        self.setStyleSheet("QLabel {"
                           "color: rgba(255, 255, 255, 0.7);"
                           "font-size: 20px;}")


class ComboBox(QComboBox):

    def __init__(self, x, y, parent=None):
        super(ComboBox, self).__init__(parent)
        self.setGeometry(x, y, 150, 30)
        self.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.setStyleSheet("QComboBox { "
                           "border: 0px solid black;"
                           "background-color: rgba(255, 255, 255, 0.7);"
                           "selection-background-color: rgb(168,168,168);"
                           "selection-color: rgba(0, 0, 0, 0.6);"
                           "color: rgba(0, 0, 0, 0.6);"
                           "font-size: 16px;}"
                           "QComboBox::drop-down {border: 0px;}"
                           "QComboBox::down-arrow { "
                           "image: url(../res/drop_down.png); width: 14px; height: 14px;}")


class RadioButton(QRadioButton):

    def __init__(self, x, y, text, parent=None):
        super(RadioButton, self).__init__(parent)
        self.setGeometry(x, y, 150, 30)
        self.setText(text)
        self.setStyleSheet("QRadioButton {"
                           "color: rgba(255, 255, 255, 0.7);"
                           "font-size: 17px}")


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Othello'
        self.setWindowTitle(self.title)
        self.center()

        # Background of the window
        bg = QLabel(self)
        bg.setGeometry(0, 0, 800, 600)
        bg.setStyleSheet("border-image: url(../res/bg.jpg);")

        # Text field to get player name
        self.player_name = Text(100, 90, "Player name", self)

        # Set board size
        Label(100, 180, "Board size", self)
        self.size = ComboBox(290, 180, self)
        self.size.addItem("8")
        self.size.addItem("10")
        self.size.addItem("12")
        self.size.addItem("14")

        # Allowing player to choose their color
        Label(100, 260, "Choose your color", self)
        self.colors = ComboBox(290, 260, self)
        self.colors.addItem("black")
        self.colors.addItem("white")

        # Allowing player to choose who play first
        Label(100, 350, "Who play first?", self)
        me = RadioButton(290, 350, "Me", self)
        RadioButton(360, 350, "Computer", self)
        me.setChecked(True)

        start_button = Button(200, 430, "start", self)
        start_button.clicked.connect(self.start_game)

        self.show()

    def center(self):
        """
            Center the window on the screen
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_game(self):
        """
            Start the game with the specified settings. Move to the second page of the game
        """
        name = self.player_name.toPlainText()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
