import os

from config import ships, game_name, menu_name, board_name
from ai_moves import ai_random_placement


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_board(board):
    col_headers = "    " + "  ".join(chr(ord("A") + i)
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
            if board[i][j] == "\U0001F6A2":
                return False
    return True


# try to replace below ifs with logical operator
def is_placement_valid(col, ship_size, board, row):
    if col + ship_size > len(board[0]):
        return False
    if (col > 0 and board[row][col - 1] == "\U0001F6A2") or \
            (col + ship_size < len(board) and board[row][col + ship_size] == "\U0001F6A2"):
        return False
    if (
            row > 0 and "\U0001F6A2" in board[row - 1][col:col + ship_size]):
        return False
    if row < len(board) - 1 and "\U0001F6A2" in board[row + 1][col:col + ship_size]:
        return False
    if (row + ship_size < len(
            board) and "\U0001F6A2" in board[row + ship_size][col:col + ship_size]):
        return False
    return True


def place_ships(board, ships, number_of_ships, user):
    while len(number_of_ships) != 0:
        print(f"\nNow placing ships player: {user}\n")
        print_board(board)
        print("\nAvailable ships: \n")
        for i, (ship_name, ship_size) in enumerate(ships.items(), start=1):
            print(f"{i}. {ship_name} (Size: {ship_size}) Available ships: ", number_of_ships.count(ship_name))
        ship_choice = input("\nChoose a ship: ")
        match ship_choice:
            case "1" | "2" | "3":
                ship_choice = int(ship_choice)
                ship_name, ship_size = list(ships.keys())[ship_choice - 1], \
                    list(ships.values())[ship_choice - 1]
                if ship_name not in number_of_ships:
                    clear_screen()
                    print("There are no more ships of this type")
                    continue
                print(f"\nPlacing {ship_name}")
                while True:
                    coordintaes = input("Enter coordintaes: ").upper()
                    if checking_coordinates(coordintaes, board):
                        break
                    print("Invalid coordinates. Please try again.")
                direction = "v" if ship_size == 1 else input("horizontal(h) or vertical(v): ").lower()
                # try to implement function get_col, get_row to avoid code repetition
                col = int(ord(coordintaes[0].upper()) - ord("A"))
                row = int(coordintaes[1:]) - 1
                match direction:
                    case "h":
                        if not is_placement_valid(col, ship_size, board, row):
                            clear_screen()
                            print("Invalid placement. Please try again.")
                            continue
                        for i in range(ship_size):
                            if board[row][col + i]!=".":
                                clear_screen()
                                print("Invalid placement. Please try again.")
                                continue
                        for i in range(ship_size):
                            board[row][col + i] = "\U0001F6A2"
                        number_of_ships.remove(ship_name)
                        clear_screen()
                    case "v":
                        # ToDo use is_placement_valid
                        if row + ship_size > len(board):
                            clear_screen()
                            print("Invalid placement. Please try again.")
                            continue
                        elif (col > 0 and board[row][col - 1] == "\U0001F6A2") or (col + ship_size < len(board) and board[row][col + ship_size] == "\U0001F6A2"):
                            clear_screen()
                            print("Invalid coordinates. Please try again.")
                            continue
                        elif (row > 0 and any(board[row - 1][col:col + ship_size]) == "\U0001F6A2") or\
                            (row + ship_size < len(board) and any(board[row + ship_size]
                                                                  [col:col + ship_size]) == "\U0001F6A2"):
                            clear_screen()
                            print("Invalid coordinates. Please try again.")
                            continue
                        elif (
                             row > 0 and "\U0001F6A2" in board[row - 1][col:col + ship_size] or row<len(board)-1 and "\U0001F6A2" in board[row + 1][col:col + ship_size] or
                             row +
                             ship_size < len(
                                 board) and "\U0001F6A2" in board[row + ship_size][col:col + ship_size]
                         ):
                             clear_screen()
                             print("Invalid coordinates. Please try again.")
                             continue
                        elif not is_valid_vertical_placement(board, row, col, ship_size):
                            clear_screen()
                            print("Invalid coordinates. Please try again.")
                            continue
                        elif (
                            row > 0 and "\U0001F6A2" in board[row - 1][col:col + ship_size]):
                            clear_screen()
                            print("Invalid coordinates. Please try again.")
                            continue
                        elif row<len(board)-1:
                              if "\U0001F6A2" in board[row + 1][col:col + ship_size]:
                                clear_screen()
                                print("Invalid coordinates. Please try again.")
                                continue
                        elif (row + ship_size < len(
                                 board) and "\U0001F6A2" in board[row + ship_size][col:col + ship_size]):
                             clear_screen()
                             print("Invalid coordinates. Please try again.")
                             continue
                        for i in range(ship_size):
                            if board[row + i][col] != ".":
                                clear_screen()
                                print("Invalid coordinates. Please try again.")
                                continue
                        for i in range(ship_size):
                            board[row + i][col] = "\U0001F6A2"
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
    clear_screen()
    menu_choose=True
    print("\n" + game_name)
    print(menu_name)
    print("1 - HUMAN vs HUMAN")
    print("2 - HUMAN vs AI")
    print("")
    print("x - quit")
    print("- "*10)
    while menu_choose:
        menu1 = input("Choose who you want to play with: \n")
        if menu1 == "1":
            user = input("\nFirst player name: \n")
            user2 = input("Second player name: \n")
            break
        elif menu1 == "2":
            user = input("\nHuman player name: \n")
            user2 = "AI player"
            break
        elif menu1 == "x":
            print("What a shame... :(\nBye bye)")
            exit()
        else:
            print("\nDon't be ridiculous :) \nYou must choose your opponent\n")
            continue
    clear_screen()

    print("\n" + game_name)
    print(board_name)
    print("- "*10)
    print("1 - 5x5 board")
    print("2 - 10x10 board")
    print("3 - 15x15 board")
    print("")
    print("x - quit")
    print("- "*10)
    menu2 = input("Choose: ")
    match menu2:
        case "1":
            board = [["\U0001F30A" for i in range(5)] for i in range(5)]
            board2 = [["\U0001F30A" for i in range(5)] for i in range(5)]
            number_of_ships = ["Cruiser", "Cruiser", "Destroyer", "Destroyer",
                   "Destroyer"]
            clear_screen()
            place_ships(board, ships, number_of_ships, user)
            print_board(board)
            clear_screen()
            number_of_ships = ["Cruiser", "Cruiser", "Destroyer", "Destroyer",
                   "Destroyer"]
            clear_screen()
            if user2 == "AI player":
                ai_random_placement(board2, ships, number_of_ships)
                print("AI player board:")
                print_board(board2)
            else:
                place_ships(board2, ships, number_of_ships, user2)
                print_board(board2)
            return user, user2, board, board2
        case "2":
            board = [["\U0001F30A" for i in range(10)] for i in range(10)]
            board2 = [["\U0001F30A" for i in range(10)] for i in range(10)]
            number_of_ships = ["Submarine", "Cruiser", "Cruiser", "Destroyer", "Destroyer",
                   "Destroyer"]
            clear_screen()
            place_ships(board, ships, number_of_ships, user)
            print_board(board)
            clear_screen()
            number_of_ships = ["Submarine", "Cruiser", "Cruiser", "Destroyer", "Destroyer",
                   "Destroyer"]
            if user2 == "AI player":
                ai_random_placement(board2, ships, number_of_ships)
                print("AI player board:")
                print_board(board2)
            else:
                place_ships(board2, ships, number_of_ships, user2)
                print_board(board2)
            return user, user2, board, board2
        case "3":
            board = [["\U0001F30A" for i in range(15)] for i in range(15)]
            board2 = [["\U0001F30A" for i in range(15)] for i in range(15)]
            number_of_ships = ["Submarine", "Submarine", "Cruiser", "Cruiser", "Cruiser", "Destroyer", "Destroyer", "Destroyer", "Destroyer"]
            clear_screen()
            place_ships(board, ships, number_of_ships, user)
            print_board(board)
            clear_screen()
            number_of_ships = ["Submarine", "Submarine", "Cruiser", "Cruiser", "Cruiser", "Destroyer", "Destroyer", "Destroyer", "Destroyer"]
            if user2 == "AI player":
                ai_random_placement(board2, ships, number_of_ships)
                print("AI player board:")
                print_board(board2)
            else:
                place_ships(board2, ships, number_of_ships, user2)
                print_board(board2)
            return user, user2, board, board2
        case "x":
            exit()
        case _:
             print("Choose the board size or quit")
    
# menu()