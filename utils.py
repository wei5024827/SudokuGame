import random

def generate_solution():
    """生成一个完整的数独解决方案"""
    base = 3
    side = base * base

    def pattern(r, c): return (base * (r % base) + r // base + c) % side

    def shuffle(s): return random.sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    return [[nums[pattern(r, c)] for c in cols] for r in rows]

def generate_sudoku(difficulty):
    """根据难度生成数独棋盘"""
    solution = generate_solution()
    board = [row[:] for row in solution]
    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)

    if difficulty == "简单":
        empty_cells = 30
    elif difficulty == "中等":
        empty_cells = 45
    else:  # 困难
        empty_cells = 60

    for i in range(empty_cells):
        row, col = cells[i]
        board[row][col] = 0

    return board, solution
