ships = {
    "Submarine": 3,
    "Cruiser": 2,
    "Destroyer": 1
}
number_of_ships = ["Submarine", "Cruiser", "Cruiser", "Destroyer", "Destroyer",
                   "Destroyer"]
board = [['.' for i in range(10)] for i in range(10)]
board2 = [['.' for i in range(10)] for i in range(10)]
def user_name():
    user=input("What is your name?: ")
    user2=input("What is your name?: ")


def print_empty_board(cols, rows):
    board = [['.' for i in range(cols)] for i in range(rows)]
    col_headers = "   " + " ".join(str(i + 1)
                                   for i in range(len(board[0])))
    print(col_headers)
    for i, row in enumerate(board):
        row_header = chr(ord('A') + i).ljust(2)
        row_format = " ".join(row)
        print(f"{row_header} {row_format}")
    return board


def print_board(board):
    col_headers = "   " + " ".join(chr(ord('A') + i)
                                   for i in range(len(board[0])))
    print(col_headers)
    for i, row in enumerate(board):
        row_header = str(i + 1).ljust(2)
        row_format = " ".join(row)
        print(f"{row_header} {row_format}")
    return board


def checking_coordinates(coordinates, board):
    if len(coordinates) < 2:
        return False
    col = coordinates[0].upper()
    row = coordinates[1:]

    if not col.isalpha() or not row.isdigit():
        return False

    col = ord(col) - ord('A')
    row = int(row) - 1

    return 0 <= row < len(board) and 0 <= col < len(board[0])


def place_ships(board, ships):
    while len(number_of_ships) != 0:
        print("Ships:")
        for i, (ship_name, ship_size) in enumerate(ships.items(), start=1):
            print(f"{i}. {ship_name} (Size: {ship_size})")
        ship_choice = input("Choose a ship: ")
        match ship_choice:
            case "1" | "2" | "3":
                ship_choice = int(ship_choice)
                ship_name, ship_size = list(ships.keys())[ship_choice - 1], \
                    list(ships.values())[ship_choice - 1]
                if ship_name not in number_of_ships:
                    print("There are no more ships of this type")
                    continue
                print(f"Placing {ship_name}")
                while True:
                    coordintaes = input("Enter coordintaes: ").upper()
                    if checking_coordinates(coordintaes, board):
                        break
                    else:
                        print("Invalid coordinates. Please try again.")
                if ship_size == 1:
                    direction = "h"
                else:
                    direction = input("horizontal(h) or vertical(v): ").lower()
                row = int(ord(coordintaes[0].upper()) - ord('A'))
                col = int(coordintaes[1:]) - 1
                match direction:
                    case "h":
                        if (col > 0 and board[row][col - 1] == 'S') or \
                                (col + ship_size < len(board) and board[row][col + ship_size] == 'S'):
                            print("Invalid placement. Please try again.")
                            continue
                        if (
                            row > 0 and 'S' in board[row - 1][col:col + ship_size] or
                            row +
                            ship_size < len(
                                board) and 'S' in board[row + ship_size][col:col + ship_size]
                        ):
                            print("Invalid placement. Please try again.")
                            continue
                        for i in range(ship_size):
                            if board[row][col + i] != '.':
                                print("Invalid placement. Please try again.")
                                continue
                        for i in range(ship_size):
                            board[row][col + i] = 'S'
                        print_board(board)
                        number_of_ships.remove(ship_name)
                    case "v":
                        if (col > 0 and board[row][col - 1] == 'S') or \
                                (col + ship_size < len(board) and board[row][col + ship_size] == 'S'):
                            print("Invalid placement. Please try again.")
                            continue
                        if (row > 0 and any(board[row - 1][col:col + ship_size]) == 'S') or\
                            (row + ship_size < len(board) and any(board[row + ship_size]
                                                                  [col:col + ship_size]) == 'S'):
                            print("Invalid placement. Please try again.")
                            continue
                        if (
                            row > 0 and 'S' in board[row - 1][col:col + ship_size] or
                            row +
                            ship_size < len(
                                board) and 'S' in board[row + ship_size][col:col + ship_size]
                        ):
                            print("Invalid placement. Please try again.")
                            continue
                        for i in range(ship_size):
                            if board[row + i][col] != '.':
                                print("Invalid placement. Please try again.")
                                continue
                        for i in range(ship_size):
                            board[row + i][col] = 'S'
                        print_board(board)
                        number_of_ships.remove(ship_name)
                    case _:
                        print("Type (h) or (v) to choose direction")
                        continue
            case _:
                print("Enter a number (1-3) to choose a ship.")
    return board


print_empty_board(10, 10)
place_ships(board, ships)
print_board(board)
