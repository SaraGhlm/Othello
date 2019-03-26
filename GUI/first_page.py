from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets


class FirstPage:

    def __init__(self, widget, widget_size):
        font_size = 20
        self.combo_box_style = """QComboBox {{ 
                            border: 0px solid black;
                            background-color: rgba(255, 255, 255, 0.7);
                            selection-background-color: rgb(168,168,168);
                            selection-color: rgba(0, 0, 0, 0.6);
                            color: rgba(0, 0, 0, 0.6);
                            font-size: {}px;}}
                            QComboBox::drop-down {{border: 0px;}}
                            QComboBox::down-arrow {{ 
                            image: url(res/drop_down.png); width: 14px; height: 14px;}}""".format(font_size)
        self.label_style = """QLabel {{
                        color: rgba(255, 255, 255, 0.7);
                        font-size: {}px;}}""".format(font_size)
        self.text_style = """QTextEdit {{
                        border: 0px solid black;
                        border-bottom: 1px solid rgba(0, 0, 0, 0.7);
                        color: rgba(255, 255, 255, 0.7);
                        background-color: rgba(0, 0, 0, 0);
                        font-size: {}px;}}""".format(font_size)
        self.button_style = """QPushButton {{ 
                        font-size: {}px;
                        color: rgba(1, 1, 1, 0.7);
                        border: 2px solid #8f8f91; 
                        border-radius: 6px; 
                        background-color: rgba(255, 255, 255, 0.3); 
                        min-width: 80px;}} 
                        QPushButton:hover {{ 
                        background-color: rgba(255, 255, 255, 0.5);}}
                        QPushButton:pressed {{ 
                        background-color: rgba(255, 255, 255, 0.7);}}
                        QPushButton:flat {{ 
                        border: none; /* no border for a flat push button */}} 
                        QPushButton:default {{ 
                        border-color: navy; /* make the default button prominent */}}""".format(font_size)
        self.radio_button_style = """QRadioButton {{
                        color: rgba(255, 255, 255, 0.7);
                        font-size: {}px}}""".format(font_size)

        self.group_box_style = """QGroupBox {
                                border: 0px;}"""

        self.background_label = QtWidgets.QLabel(widget)
        self.background_label.setGeometry(0, 0, widget_size[0], widget_size[1])
        self.background_label.setStyleSheet("border-image: url(res/bg.jpg);")

        self.two_player_radio_button = QtWidgets.QRadioButton(widget)
        self.two_player_radio_button.setGeometry(widget_size[0]/8, widget_size[1]/8, 150, 30)
        self.two_player_radio_button.setText("Two Player")
        self.two_player_radio_button.setStyleSheet(self.radio_button_style)
        self.two_player_radio_button.clicked.connect(self.show_two_player_setup)

        self.one_player_radio_button = QtWidgets.QRadioButton(widget)
        self.one_player_radio_button.setGeometry(widget_size[0]/8 + 160, widget_size[1]/8, 150, 30)
        self.one_player_radio_button.setText("One Player")
        self.one_player_radio_button.setStyleSheet(self.radio_button_style)
        self.one_player_radio_button.clicked.connect(self.show_one_player_setup)

        self.zero_player_radio_button = QtWidgets.QRadioButton(widget)
        self.zero_player_radio_button.setGeometry(widget_size[0]/8 + 160*2, widget_size[1]/8, 150, 30)
        self.zero_player_radio_button.setText("Zero Player")
        self.zero_player_radio_button.setStyleSheet(self.radio_button_style)
        self.zero_player_radio_button.clicked.connect(self.show_zero_player_setup)

        self.board_size_label = QtWidgets.QLabel(widget)
        self.board_size_label.setText("Board size")
        self.board_size_label.setGeometry(widget_size[0]/8, widget_size[0]/5, 200, 30)
        self.board_size_label.setStyleSheet(self.label_style)

        self.board_size_combo_box = QtWidgets.QComboBox(widget)
        self.board_size_combo_box.setGeometry(widget_size[0]/8 + 230, widget_size[0]/5, 150, 30)
        self.board_size_combo_box.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.board_size_combo_box.setStyleSheet(self.combo_box_style)
        self.board_size_combo_box.setCurrentIndex(0)
        self.board_size_combo_box.addItem("8")
        self.board_size_combo_box.addItem("10")
        self.board_size_combo_box.addItem("12")
        self.board_size_combo_box.addItem("14")

        self.color_label = QtWidgets.QLabel(widget)
        self.color_label.setText("Choose your color")
        self.color_label.setGeometry(widget_size[0]/8, widget_size[0]/5 + 80*2, 200, 30)
        self.color_label.setStyleSheet(self.label_style)

        self.colors_combo_box = QtWidgets.QComboBox(widget)
        self.colors_combo_box.setGeometry(widget_size[0]/8 + 230, widget_size[0]/5 + 80*2, 150, 30)
        self.colors_combo_box.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.colors_combo_box.setStyleSheet(self.combo_box_style)
        self.colors_combo_box.addItem("Black")
        self.colors_combo_box.addItem("White")

        self.level_label = QtWidgets.QLabel(widget)
        self.level_label.setText("Choose level")
        self.level_label.setGeometry(widget_size[0]/8, widget_size[0]/5 + 80*2, 200, 30)
        self.level_label.setStyleSheet(self.label_style)

        self.level_combo_box = QtWidgets.QComboBox(widget)
        self.level_combo_box.setGeometry(widget_size[0]/8 + 230, widget_size[0]/5 + 80*2, 150, 30)
        self.level_combo_box.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.level_combo_box.setStyleSheet(self.combo_box_style)
        self.level_combo_box.addItem("Beginner")
        self.level_combo_box.addItem("Intermediate")
        self.level_combo_box.addItem("Hard")

        self.start_button = QtWidgets.QPushButton(widget)
        self.start_button.setText("Start")
        self.start_button.setGeometry(widget_size[0]/8 + 110, widget_size[0]/5 + 80*3, 170, 50)
        self.start_button.setStyleSheet(self.button_style)
        self.start_button.clicked.connect(widget.start_game)

        # Zero player options
        self.first_player_label = QtWidgets.QLabel(widget)
        self.first_player_label.setText("First Player")
        self.first_player_label.setGeometry(widget_size[0]/8, widget_size[0]/5 + 80, 200, 30)
        self.first_player_label.setStyleSheet(self.label_style)

        self.first_player_combo_box = QtWidgets.QComboBox(widget)
        self.first_player_combo_box.setGeometry(widget_size[0]/8 + 230, widget_size[0]/5 + 80, 250, 30)
        self.first_player_combo_box.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.first_player_combo_box.setStyleSheet(self.combo_box_style)
        self.first_player_combo_box.addItem("Combination_Beginner")
        self.first_player_combo_box.addItem("Combination_Intermediate")
        self.first_player_combo_box.addItem("Combination_Hard")

        self.second_player_label = QtWidgets.QLabel(widget)
        self.second_player_label.setText("Second Player")
        self.second_player_label.setGeometry(widget_size[0]/8, widget_size[0]/5 + 80*2, 200, 30)
        self.second_player_label.setStyleSheet(self.label_style)

        self.second_player_combo_box = QtWidgets.QComboBox(widget)
        self.second_player_combo_box.setGeometry(widget_size[0]/8 + 230, widget_size[0]/5 + 80*2, 250, 30)
        self.second_player_combo_box.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.second_player_combo_box.setStyleSheet(self.combo_box_style)
        self.second_player_combo_box.addItem("Combination_Beginner")
        self.second_player_combo_box.addItem("Combination_Intermediate")
        self.second_player_combo_box.addItem("Combination_Hard")

        self.hide_setup()
        widget.show()

    def hide(self):
        """
            Hiding the whole setup page
        """
        self.background_label.hide()
        self.board_size_label.hide()
        self.board_size_combo_box.hide()
        self.color_label.hide()
        self.colors_combo_box.hide()
        self.level_label.hide()
        self.level_combo_box.hide()
        self.first_player_label.hide()
        self.first_player_combo_box.hide()
        self.second_player_label.hide()
        self.second_player_combo_box.hide()
        self.start_button.hide()
        self.two_player_radio_button.hide()
        self.one_player_radio_button.hide()
        self.zero_player_radio_button.hide()

    def hide_setup(self):
        """
            Hiding setup options which are based on game mode. Used at the beginning of the game
        """
        self.board_size_label.hide()
        self.board_size_combo_box.hide()
        self.color_label.hide()
        self.colors_combo_box.hide()
        self.level_label.hide()
        self.level_combo_box.hide()
        self.first_player_label.hide()
        self.first_player_combo_box.hide()
        self.second_player_label.hide()
        self.second_player_combo_box.hide()
        self.start_button.hide()

    def show(self):
        """
            Showing the initial state of setup page
        """
        self.background_label.show()
        self.one_player_radio_button.show()
        self.two_player_radio_button.show()
        self.zero_player_radio_button.show()

    def show_two_player_setup(self):
        self.hide_setup()
        self.board_size_label.show()
        self.board_size_combo_box.show()
        self.start_button.show()

    def show_one_player_setup(self):
        self.hide_setup()
        self.board_size_label.show()
        self.board_size_combo_box.show()
        self.color_label.show()
        self.colors_combo_box.show()
        self.first_player_label.setText("Computer Player")
        self.first_player_label.show()
        self.first_player_combo_box.show()
        self.start_button.show()

    def show_zero_player_setup(self):
        self.hide_setup()
        self.board_size_label.show()
        self.board_size_combo_box.show()
        self.first_player_label.setText("First Player")
        self.first_player_label.show()
        self.first_player_combo_box.show()
        self.second_player_label.show()
        self.second_player_combo_box.show()
        self.start_button.show()

