import os
ships = {
    "Submarine": 3,
    "Cruiser": 2,
    "Destroyer": 1
}
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# def print_empty_board(cols, rows):
#     board = [["." for i in range(cols)] for i in range(rows)]
#     col_headers = "   " + " ".join(chr(ord("A") + i)
#                                    for i in range(len(board[0])))
#     print(col_headers)
#     for i, row in enumerate(board):
#         row_header = str(i + 1).ljust(2)
#         row_format = " ".join(row)
#         print(f"{row_header} {row_format}")
#     return board


def print_board(board):
    col_headers = "   " + " ".join(chr(ord("A") + i)
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

    col = ord(col) - ord("A")
    row = int(row) - 1

    return 0 <= row < len(board) and 0 <= col < len(board[0])

def is_valid_vertical_placement(board, row, col, ship_size):
    for i in range(max(0, row - 1), min(len(board), row + ship_size + 1)):
        for j in range(max(0, col - 1), min(len(board[0]), col + 2)):
            if board[i][j] == "S":
                return False
    return True


def place_ships(board, ships, number_of_ships, user):
    while len(number_of_ships) != 0:
        print(user+"\n")
        print_board(board)
        print("Ships:")
        for i, (ship_name, ship_size) in enumerate(ships.items(), start=1):
            print(f"{i}. {ship_name} (Size: {ship_size}) Available ships: ", number_of_ships.count(ship_name))
        ship_choice = input("Choose a ship: ")
        match ship_choice:
            case "1" | "2" | "3":
                ship_choice = int(ship_choice)
                ship_name, ship_size = list(ships.keys())[ship_choice - 1], \
                    list(ships.values())[ship_choice - 1]
                if ship_name not in number_of_ships:
                    clear_screen()
                    print("There are no more ships of this type")
                    continue
                print(f"Placing {ship_name}")
                while True:
                    coordintaes = input("Enter coordintaes: ").upper()
                    if checking_coordinates(coordintaes, board):
                        break
                    else:
                        clear_screen()
                        print("Invalid coordinates. Please try again.")
                if ship_size == 1:
                    direction = "v"
                else:
                    direction = input("horizontal(h) or vertical(v): ").lower()
                col = int(ord(coordintaes[0].upper()) - ord("A"))
                row = int(coordintaes[1:]) - 1
                match direction:
                    case "h":
                        if col + ship_size > len(board[0]):
                            clear_screen()
                            print("Invalid placement. Please try again.")
                            continue
                        elif (col > 0 and board[row][col - 1] == "S") or \
                                 (col + ship_size < len(board) and board[row][col + ship_size] == "S"):
                             clear_screen()
                             print("Invalid placement. Please try again.")
                             continue
                        elif (
                            row > 0 and "S" in board[row - 1][col:col + ship_size]):
                            clear_screen()
                            print("Invalid placement. Please try again.")
                            continue
                        elif row<len(board)-1 and "S" in board[row + 1][col:col + ship_size]:
                                clear_screen()
                                print("Invalid placement. Please try again.")
                                continue
                        elif (row + ship_size < len(
                                 board) and "S" in board[row + ship_size][col:col + ship_size]):
                             clear_screen()
                             print("Invalid placement. Please try again.")
                             continue
                        for i in range(ship_size):
                            if board[row][col + i]!=".":
                                clear_screen()
                                print("Invalid placement. Please try again.")
                                continue
                        for i in range(ship_size):
                            board[row][col + i] = "S"
                        number_of_ships.remove(ship_name)
                        clear_screen()
                    case "v":
                        if row + ship_size > len(board):
                            clear_screen()
                            print("Invalid placement. Please try again.")
                            continue
                        elif (col > 0 and board[row][col - 1] == "S") or (col + ship_size < len(board) and board[row][col + ship_size] == "S"):
                            clear_screen()
                            print("Invalid coordinates. Please try again.")
                            continue
                        elif (row > 0 and any(board[row - 1][col:col + ship_size]) == "S") or\
                            (row + ship_size < len(board) and any(board[row + ship_size]
                                                                  [col:col + ship_size]) == "S"):
                            clear_screen()
                            print("Invalid coordinates. Please try again.")
                            continue
                        elif (
                             row > 0 and "S" in board[row - 1][col:col + ship_size] or col<len(board)-1 and "S" in board[row + 1][col:col + ship_size] or
                             row +
                             ship_size < len(
                                 board) and "S" in board[row + ship_size][col:col + ship_size]
                         ):
                             clear_screen()
                             print("Invalid coordinates. Please try again.")
                             continue
                        elif not is_valid_vertical_placement(board, row, col, ship_size):
                            clear_screen()
                            print("Invalid coordinates. Please try again.")
                            continue
                        elif (
                            row > 0 and "S" in board[row - 1][col:col + ship_size]):
                            clear_screen()
                            print("Invalid coordinates. Please try again.")
                            continue
                        elif row<len(board)-1:
                              if "S" in board[row + 1][col:col + ship_size]:
                                clear_screen()
                                print("Invalid coordinates. Please try again.")
                                continue
                        elif (row + ship_size < len(
                                 board) and "S" in board[row + ship_size][col:col + ship_size]):
                             clear_screen()
                             print("Invalid coordinates. Please try again.")
                             continue
                        for i in range(ship_size):
                            if board[row + i][col] != ".":
                                clear_screen()
                                print("Invalid coordinates. Please try again.")
                                continue
                        for i in range(ship_size):
                            board[row + i][col] = "S"
                        number_of_ships.remove(ship_name)
                        clear_screen()
                    case _:
                        clear_screen()
                        print("Type (h) or (v) to choose direction")
                        continue
            case _:
                clear_screen()
                print("Enter a number (1-3) to choose a ship.")
    return board

def menu():
     print("\nWELCOME IN BATTLESHIP\n")
     print("MENU")
     print("- "*10)
     print("1 - 5x5 board")
     print("2 - 10x10 board")
     print("3 - 15x15 board")
     print("x - quit")
     print("- "*10)
     menu = input("Choose: ")
     match menu:
        case "1":
            user=input("First player name: ")
            user2=input("Second player name: ")
            board = [["." for i in range(5)] for i in range(5)]
            board2 = [["." for i in range(5)] for i in range(5)]
            number_of_ships = ["Cruiser", "Cruiser", "Destroyer", "Destroyer",
                   "Destroyer"]
            clear_screen()
            place_ships(board, ships, number_of_ships, user)
            print_board(board)
            clear_screen()
            number_of_ships = ["Cruiser", "Cruiser", "Destroyer", "Destroyer",
                   "Destroyer"]
            clear_screen()
            place_ships(board2, ships, number_of_ships, user2)
            print_board(board2)
            return user, user2, board, board2
        case "2":
            user=input("First player name: ")
            user2=input("Second player name: ")
            board = [["." for i in range(10)] for i in range(10)]
            board2 = [["." for i in range(10)] for i in range(10)]
            number_of_ships = ["Submarine", "Cruiser", "Cruiser", "Destroyer", "Destroyer",
                   "Destroyer"]
            clear_screen()
            place_ships(board, ships, number_of_ships, user)
            print_board(board)
            clear_screen()
            number_of_ships = ["Submarine", "Cruiser", "Cruiser", "Destroyer", "Destroyer",
                   "Destroyer"]
            place_ships(board2, ships, number_of_ships, user2)
            print_board(board2)
            return user, user2, board, board2
        case "3":
            user=input("First player name: ")
            user2=input("Second player name: ")
            board = [["." for i in range(15)] for i in range(15)]
            board2 = [["." for i in range(15)] for i in range(15)]
            number_of_ships = ["Submarine", "Submarine", "Cruiser", "Cruiser", "Cruiser", "Destroyer", "Destroyer", "Destroyer", "Destroyer"]
            clear_screen()
            place_ships(board, ships, number_of_ships, user)
            print_board(board)
            clear_screen()
            place_ships(board2, ships, number_of_ships, user2)
            print_board(board2)
            return user, user2, board, board2
        case "x":
            exit()
        case _:
             print("Choose the board size or quit")
    
menu()