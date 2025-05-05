from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Sudokucell import SudokuCell
from utils import generate_sudoku
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
        self.setFixedSize(50, 50)
        self.setFont(QFont("Arial", 20))
        
        # 根据宫的位置设置背景色
        block_row, block_col = row // 3, col // 3
        if (block_row + block_col) % 2 == 0:
            self.base_style = "background-color: #f0f0f0;"  # 浅灰色宫
        else:
            self.base_style = "background-color: white;"  # 白色宫
        
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

class SudokuGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("数独游戏")
        self.setFixedSize(600, 700)
        
        # 主窗口和布局
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        
        # 标题
        self.title_label = QLabel("数独游戏")
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)
        
        # 控制面板
        self.control_panel = QWidget()
        self.control_layout = QHBoxLayout()
        self.control_panel.setLayout(self.control_layout)
        
        self.difficulty_label = QLabel("难度:")
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["简单", "中等", "困难"])
        
        self.start_button = QPushButton("开始游戏")
        self.reset_button = QPushButton("重新开始")
        self.check_button = QPushButton("检查答案")  # 新增检查按钮
        
        self.control_layout.addWidget(self.difficulty_label)
        self.control_layout.addWidget(self.difficulty_combo)
        self.control_layout.addStretch()
        self.control_layout.addWidget(self.start_button)
        self.control_layout.addWidget(self.reset_button)
        self.control_layout.addWidget(self.check_button)
        
        self.main_layout.addWidget(self.control_panel)
        
        # 数独面板
        self.sudoku_panel = QWidget()
        self.sudoku_layout = QGridLayout()
        self.sudoku_layout.setSpacing(0)
        self.sudoku_layout.setContentsMargins(2, 2, 2, 2)
        self.sudoku_panel.setLayout(self.sudoku_layout)
        
        # 创建单元格
        self.cells = []
        for row in range(9):
            row_cells = []
            for col in range(9):
                cell = SudokuCell(row, col)
                cell.clicked.connect(self.cell_clicked)
                self.sudoku_layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self.cells.append(row_cells)
        
        # 数字选择面板
        self.number_panel = QWidget()
        self.number_layout = QHBoxLayout()
        self.number_panel.setLayout(self.number_layout)
        
        for num in range(1, 10):
            btn = QPushButton(str(num))
            btn.setFixedSize(50, 50)
            btn.setFont(QFont("Arial", 20))
            btn.clicked.connect(lambda _, n=num: self.number_selected(n))
            self.number_layout.addWidget(btn)
        
        self.main_layout.addWidget(self.sudoku_panel)
        self.main_layout.addWidget(self.number_panel)
        
        # 连接信号
        self.start_button.clicked.connect(self.start_game)
        self.reset_button.clicked.connect(self.reset_game)
        self.check_button.clicked.connect(self.check_all)  # 连接检查按钮
        
        # 初始化游戏
        self.selected_cell = None
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.start_game()

    def cell_clicked(self):
        sender = self.sender()
        if self.selected_cell:
            self.selected_cell.setStyleSheet(self.selected_cell.styleSheet().replace("border: 2px solid red;", ""))
        
        self.selected_cell = sender
        if not sender.original:
            sender.setStyleSheet(sender.styleSheet() + "border: 2px solid red;")

    def number_selected(self, num):
        if self.selected_cell and not self.selected_cell.original:
            self.selected_cell.set_value(num)
            
            # 实时检查填入的数字是否正确
            row, col = self.selected_cell.row, self.selected_cell.col
            if num != 0:
                if num != self.solution[row][col]:
                    self.selected_cell.mark_wrong(True)
                else:
                    self.selected_cell.mark_wrong(False)
            
            self.check_win()

    def check_all(self):
        """检查所有已填数字是否正确"""
        has_error = False
        for row in range(9):
            for col in range(9):
                cell = self.cells[row][col]
                if not cell.original and cell.value != 0:
                    if cell.value != self.solution[row][col]:
                        cell.mark_wrong(True)
                        has_error = True
                    else:
                        cell.mark_wrong(False)
        
        if not has_error:
            QMessageBox.information(self, "检查结果", "所有已填数字都是正确的！")

    def generate_sudoku(self):
        # 生成一个完整的数独解决方案
        self.solution = self.generate_solution()
        
        # 根据难度决定挖空的数量
        difficulty = self.difficulty_combo.currentText()
        if difficulty == "简单":
            empty_cells = 30
        elif difficulty == "中等":
            empty_cells = 45
        else:  # 困难
            empty_cells = 60
        
        # 复制解决方案并挖空
        self.board = [row[:] for row in self.solution]
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        for i in range(empty_cells):
            row, col = cells[i]
            self.board[row][col] = 0
        
        # 更新UI
        self.update_board()

    def generate_solution(self):
        # 使用数独生成算法
        base = 3
        side = base * base
        
        def pattern(r, c): return (base * (r % base) + r // base + c) % side
        
        from random import sample
        def shuffle(s): return sample(s, len(s))
        
        rBase = range(base)
        rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, base * base + 1))
        
        return [[nums[pattern(r, c)] for c in cols] for r in rows]

    def update_board(self):
        for row in range(9):
            for col in range(9):
                value = self.board[row][col]
                original = value != 0
                self.cells[row][col].set_value(value, original)

    def start_game(self):
        self.generate_sudoku()
        self.selected_cell = None

    def reset_game(self):
        # 重置为当前游戏的初始状态
        for row in range(9):
            for col in range(9):
                value = self.board[row][col]
                original = value != 0
                self.cells[row][col].set_value(value, original)
        self.selected_cell = None

    def check_win(self):
        # 检查是否完成
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value == 0:
                    return
        
        # 检查是否正确
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value != self.solution[row][col]:
                    QMessageBox.information(self, "游戏结束", "抱歉，答案不正确！")
                    return
        
        QMessageBox.information(self, "恭喜", "你成功解决了这个数独！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = SudokuGame()
    game.show()
    sys.exit(app.exec_())