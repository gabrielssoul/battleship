import random
import time

def ai_random_placement(board, ships, number_of_ships):
    def is_valid_placement(row, col, ship_size, direction):
        if direction == "h":
            if col + ship_size > len(board[0]):
                return False
            placement_area = board[row][col:col + ship_size]
            surround = [board[r][c] for r in range(max(0, row - 1), min(len(board), row + 2))
                              for c in range(max(0, col - 1), min(len(board[0]), col + ship_size + 1))]
        else:
            if row + ship_size > len(board):
                return False
            placement_area = [board[row + i][col] for i in range(ship_size)]
            surround = [board[r][c] for r in range(max(0, row - 1), min(len(board), row + ship_size + 1))
                              for c in range(max(0, col - 1), min(len(board[0]), col + 2))]

        return all(cell == "\U0001F30A" for cell in placement_area) and not any(cell == "\U0001F6A2" for cell in surround)

    while len(number_of_ships) != 0:
        print("AI Player is placing ships...\n")
        ship_name = random.choice(number_of_ships)
        ship_size = ships[ship_name]
        print(f"Placing AI's {ship_name}")
        while True:
            col = random.randint(0, len(board[0]) - 1)
            row = random.randint(0, len(board) - 1)
            direction = random.choice(["h", "v"])
            if is_valid_placement(row, col, ship_size, direction):
                break
        for i in range(ship_size):
            if direction == "h":
                board[row][col + i] = "\U0001F6A2"
            else:
                board[row + i][col] = "\U0001F6A2"
        time.sleep(1)
        number_of_ships.remove(ship_name)
    return board

def ai_random_shoot(board_size):
    row = random.randint(0, board_size - 1)
    col = random.randint(0, board_size - 1)
    ai_hit = [row, col]
    return ai_hit