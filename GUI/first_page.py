import sys

from PyQt5.QtCore import Qt

from PyQt5 import QtWidgets
import GUI.main

class FirstPage():

    def __init__(self, widget):
        # super().__init__()
        self.combo_box_style = """QComboBox { 
                            border: 0px solid black;
                            background-color: rgba(255, 255, 255, 0.7);
                            selection-background-color: rgb(168,168,168);
                            selection-color: rgba(0, 0, 0, 0.6);
                            color: rgba(0, 0, 0, 0.6);
                            font-size: 16px;}
                            QComboBox::drop-down {border: 0px;}
                            QComboBox::down-arrow { 
                            image: url(res/drop_down.png); width: 14px; height: 14px;}"""
        self.label_style = """QLabel {
                        color: rgba(255, 255, 255, 0.7);
                        font-size: 20px;}"""
        self.text_style = """QTextEdit {
                        border: 0px solid black;
                        border-bottom: 1px solid rgba(0, 0, 0, 0.7);
                        color: rgba(255, 255, 255, 0.7);
                        background-color: rgba(0, 0, 0, 0);
                        font-size: 17px;}"""
        self.button_style = """QPushButton { 
                        font-size: 20px;
                        color: rgba(1, 1, 1, 0.7);
                        border: 2px solid #8f8f91; 
                        border-radius: 6px; 
                        background-color: rgba(255, 255, 255, 0.3); 
                        min-width: 80px;} 
                        QPushButton:hover { 
                        background-color: rgba(255, 255, 255, 0.5);}
                        QPushButton:pressed { 
                        background-color: rgba(255, 255, 255, 0.7);} 
                        QPushButton:flat { 
                        border: none; /* no border for a flat push button */} 
                        QPushButton:default { 
                        border-color: navy; /* make the default button prominent */}"""
        self.radio_button_style = """QRadioButton {
                        color: rgba(255, 255, 255, 0.7);
                        font-size: 17px}"""

        # Background of the window
        self.bg = QtWidgets.QLabel(widget)
        self.bg.setGeometry(0, 0, 800, 600)
        self.bg.setStyleSheet("border-image: url(res/bg.jpg);")

        self.player_name = QtWidgets.QTextEdit(widget)
        self.player_name.setPlaceholderText("Player name")
        self.player_name.setGeometry(100, 90, 180, 30)
        self.player_name.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.player_name.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.player_name.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.player_name.setStyleSheet(self.text_style)

        self.board_size_label = QtWidgets.QLabel(widget)
        self.board_size_label.setText("Board size")
        self.board_size_label.setGeometry(100, 180, 200, 30)
        self.board_size_label.setStyleSheet(self.label_style)

        self.size = QtWidgets.QComboBox(widget)
        self.size.setGeometry(290, 180, 150, 30)
        self.size.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.size.setStyleSheet(self.combo_box_style)
        self.size.setCurrentIndex(0)
        self.size.addItem("8")
        self.size.addItem("10")
        self.size.addItem("12")
        self.size.addItem("14")

        self.color_label = QtWidgets.QLabel(widget)
        self.color_label.setText("Choose your color")
        self.color_label.setGeometry(100, 260, 200, 30)
        self.color_label.setStyleSheet(self.label_style)

        self.colors = QtWidgets.QComboBox(widget)
        self.colors.setGeometry(290, 260, 150, 30)
        self.colors.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.colors.setStyleSheet(self.combo_box_style)
        self.colors.addItem("Black")
        self.colors.addItem("White")

        self.first_to_play_label = QtWidgets.QLabel(widget)
        self.first_to_play_label.setText("Who should play first?")
        self.first_to_play_label.setGeometry(100, 350, 200, 30)
        self.first_to_play_label.setStyleSheet(self.label_style)

        self.me = QtWidgets.QRadioButton(widget)
        self.me.setGeometry(310, 350, 150, 30)
        self.me.setText("Me")
        self.me.setStyleSheet(self.radio_button_style)
        self.me.setChecked(True)

        self.computer = QtWidgets.QRadioButton(widget)
        self.computer.setGeometry(380, 350, 150, 30)
        self.computer.setText("Computer")
        self.computer.setStyleSheet(self.radio_button_style)

        self.start_button = QtWidgets.QPushButton(widget)
        self.start_button.setText("Start")
        self.start_button.setGeometry(200, 430, 170, 50)
        self.start_button.setStyleSheet(self.button_style)
        self.start_button.clicked.connect(widget.start_game)
        widget.show()


    def clear(self):
        self.bg.hide()
        self.player_name.hide()
        self.board_size_label.hide()
        self.size.hide()
        self.color_label.hide()
        self.colors.hide()
        self.first_to_play_label.hide()
        self.me.hide()
        self.computer.hide()
        self.start_button.hide()
