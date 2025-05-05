import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QComboBox, 
                             QMessageBox, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SudokuCell(QPushButton):
    def __init__(self, row, col, value=0):
        super().__init__()
        self.row = row
        self.col = col
        self.value = value
        self.original = False
        self.is_wrong = False  # 标记是否为错误数字
        
        # 设置固定大小和字体
        self.setFixedSize(60, 60)  # 调整为适合9x9方格的大小
        self.setFont(QFont("Arial", 20))
        
        # 根据宫的位置设置背景色和边框
        block_row, block_col = row // 3, col // 3
        if (block_row + block_col) % 2 == 0:
            self.base_style = (
                "background-color: #f0f0f0; "
                "border: 1px solid black; "
                "border-top: 1px solid black; "
                "border-bottom: 1px solid black;"
            )  # 浅灰色宫
        else:
            self.base_style = (
                "background-color: white; "
                "border: 1px solid black; "
                "border-top: 1px solid black; "
                "border-bottom: 1px solid black;"
            )  # 白色宫
        
        self.setStyleSheet(self.base_style)
        self.update_display()
    
    def update_display(self):
        if self.value != 0:
            self.setText(str(self.value))
            if self.original:
                self.setStyleSheet(self.base_style + "color: black;")
                self.setEnabled(False)
            elif self.is_wrong:
                self.setStyleSheet(self.base_style + "color: red;")  # 错误数字显示红色
            else:
                self.setStyleSheet(self.base_style + "color: blue;")  # 用户输入的正确数字
        else:
            self.setText("")
            self.is_wrong = False
            self.setStyleSheet(self.base_style)
    
    def set_value(self, value, original=False):
        self.value = value
        self.original = original
        if not original:
            self.is_wrong = False
        self.update_display()
    
    def mark_wrong(self, is_wrong):
        self.is_wrong = is_wrong
        self.update_display()

