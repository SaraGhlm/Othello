import sys
import unittest
from PyQt5 import QtWidgets
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QSize
import GUI.main as main

app = QtWidgets.QApplication(sys.argv)

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        '''Create the GUI'''
        self.form = main.App()

    def test_defaults(self):
        '''Test the GUI in its default state'''
        self.assertEqual(self.form.title, 'Othello')
        self.assertEqual(self.form.size(), QSize(800, 600))
        self.assertEqual(self.form.setup_page.player_name.placeholderText(), 'Player name')
        self.assertEqual(self.form.setup_page.board_size_label.text(), 'Board size')
        self.assertEqual(self.form.setup_page.size.itemText(0), '8')
        self.assertEqual(self.form.setup_page.size.itemText(1), '10')
        self.assertEqual(self.form.setup_page.size.itemText(2), '12')
        self.assertEqual(self.form.setup_page.size.itemText(3), '14')

if __name__ == '__main__':
    unittest.main()