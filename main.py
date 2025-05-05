import sys
from PyQt5.QtWidgets import QApplication
from SudokuGame import SudokuGame
from Sudokucell import SudokuCell

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = SudokuGame()
    game.show()
    sys.exit(app.exec_())
