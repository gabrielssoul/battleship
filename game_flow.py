from config import winner_info
from placement import clear_screen, menu
from copy import deepcopy
from ai_moves import ai_random_shoot


def display_board(board, board2):
    print("    ", end="")
    for i in range(len(board)):
        print(chr(i + 65), end="  ")
    print("      ", end="")
    for i in range(len(board2)):
        print(chr(i + 65), end="  ")
    print()
    for i in range(len(board)+1):
        if i <= (len(board)-1):
            # ToDo try tu use ternary operator
            if i >= 9:
                print((i + 1), end=" ")
            else:
                print((i + 1), end="  ")
            for j in range(len(board)):
                print(board[i][j], end=" ")
            print("   ", end="")
            if i >= 9:
                print((i + 1), end=" ")
            else:
                print((i + 1), end="  ")
            for h in range(len(board2)):
                print(board2[i][h], end=" ")
        if i == len(board):
            print(f"\nYour board(first), Enemy board(second)")
        print()



def get_shot_coordinates(board_size):
    valid_input = False
    coordinates = None
    while not valid_input:
        coordinates = input("\nEnter your coordinates (e.g. B3): ")
        valid_input = are_coordinates_valid(coordinates, board_size)
        if not valid_input:
            print("Invalid input! Try again.")
            continue
    return convert_coordinates_to_numbers(coordinates)


def are_coordinates_valid(user_input, board_size):
    if board_size < 10 and len(user_input) < 2:
        return False
    if len(user_input) > 3:
        return False
    if user_input[0].isalpha() and user_input[1].isnumeric():
        user_input_converted = convert_coordinates_to_numbers(user_input)
        # ToDo combine below 2 lines into 1 if
        if (user_input_converted[0]) in range(board_size):
            if user_input_converted[1] in range(board_size):
                return True
    return False


def convert_coordinates_to_numbers(coordinates):
    converted_coordinates = []
    for i in range(len(coordinates)):
        converted_coordinates.append(i)
    converted_coordinates[1] = ord(coordinates[0].upper()) - 65
    if len(converted_coordinates) < 3:
        converted_coordinates[0] = int(coordinates[1]) - 1
    else:
        temp = [coordinates[1], coordinates[2]]
        joined_coordinates = "".join(temp)
        converted_coordinates[0] = int(joined_coordinates) - 1
        if converted_coordinates[0] < 10:
            converted_coordinates.pop(2)
    return converted_coordinates


def is_cell_occupied(hit_board, coordinates):
    return not (hit_board[coordinates[0]][coordinates[1]] == "\U0001F30A" or hit_board[coordinates[0]][coordinates[1]] == "\U0001F6A2")


def player_move(player, enemy_board, player_board):
    coordinates = None
    print(f"Now shooting player: {player}!\n")
    foe_board = deepcopy(enemy_board)
    foe_board = convert_opponents_board_to_display(foe_board)
    display_board(player_board, foe_board)
    cell_occupied = True
    while cell_occupied:
        coordinates = get_shot_coordinates(len(enemy_board))
        cell_occupied = is_cell_occupied(enemy_board, coordinates)
        if cell_occupied:
            print("You already shoot there. Try different place!")
    enemy_board = update_board_after_shoot(enemy_board, coordinates)
    winner = is_a_winner(enemy_board)
    return enemy_board, winner


def ai_move(player_board, player):
    print(f"Now shooting player: {player}!\n")
    cell_occupied = True
    while cell_occupied:
        coordinates = ai_random_shoot(len(player_board))
        cell_occupied = is_cell_occupied(player_board, coordinates)
    player_board = update_board_after_shoot(player_board, coordinates)
    winner = is_a_winner(player_board)
    return player_board, winner


def update_board_after_shoot(hit_board, coordinates):
    cell_on_hit_board = hit_board[coordinates[0]][coordinates[1]]
    if cell_on_hit_board == "\U0001F30A":
        hit_board[coordinates[0]][coordinates[1]] = "\U0000274C"
        print("\nYou missed!")
        input("Press enter to hide your board...")
        clear_screen()
    elif cell_on_hit_board == "\U0001F6A2":
        hit_surroundings = check_surroundings_of_hit(hit_board, coordinates)
        # print(is_ship_sunk(hit_surroundings))
        if is_ship_sunk(hit_surroundings):
            hit_board[coordinates[0]][coordinates[1]] = "\U0001F480"
            print("\nYou sunk a ship!")
            input("Press enter to hide your board...")
            clear_screen()
            for i in range(len(hit_surroundings)):
                hit_board[hit_surroundings[i][0]][hit_surroundings[i][1]] = "\U0001F480"
        else:
            hit_board[coordinates[0]][coordinates[1]] = "\U0001F4A5"
            print("\nYou hit a ship!")
            input("Press enter to hide your board...")
            clear_screen()
    return hit_board


def check_surroundings_of_hit(hit_board, coordinates):
    hit_cell = coordinates.copy()
    checked_coordinates = []
    list_of_cells = []
    check_count = 0
    while check_count < 2:
        if hit_cell[1]-1 >= 0:
            left_cell = [hit_cell[0], hit_cell[1] - 1]
            list_of_cells.append(left_cell)
        right_cell = [hit_cell[0], hit_cell[1] + 1]
        list_of_cells.append(right_cell)
        if hit_cell[0] - 1 >= 0:
            upper_cell = [hit_cell[0] - 1, hit_cell[1]]
            list_of_cells.append(upper_cell)
        lower_cell = [hit_cell[0] + 1, hit_cell[1]]
        list_of_cells.append(lower_cell)
        for i in range(len(list_of_cells)):
            try:
                if (hit_board[list_of_cells[i][0]][list_of_cells[i][1]] == "\U0001F6A2" or
                        hit_board[list_of_cells[i][0]][list_of_cells[i][1]] == "\U0001F4A5"):
                    item_to_add = [list_of_cells[i][0], list_of_cells[i][1],
                                   hit_board[list_of_cells[i][0]][list_of_cells[i][1]]]
                    checked_coordinates.append(item_to_add)
            except IndexError:
                continue
        check_count += 1
        if 0 < len(checked_coordinates) < 2:
            hit_cell[0] = checked_coordinates[0][0]
            hit_cell[1] = checked_coordinates[0][1]
        else:
            break
    for i in range(len(checked_coordinates)):
        original_cell = [coordinates[0], coordinates[1], "\U0001F6A2"]
        if checked_coordinates[i] == original_cell:
            checked_coordinates.pop(i)
            break
    return checked_coordinates


def is_ship_sunk(hit_surroundings):
    for i in range(len(hit_surroundings)):
        if "\U0001F6A2" in hit_surroundings[i]:
            return False
    return True


def is_a_winner(board_to_check):
    for i in range(len(board_to_check)):
        for j in range(len(board_to_check)):
            if board_to_check[i][j] == "\U0001F6A2":
                return False
    return True


def convert_opponents_board_to_display(opponents_board):
    for i in range(len(opponents_board)):
        for j in range(len(opponents_board)):
            if opponents_board[i][j] == "\U0001F6A2":
                opponents_board[i][j] = "\U0001F30A"
    return opponents_board


def display_win(player, board):
    clear_screen()
    print(winner_info, "\n")
    print("")
    print(f"Congratulations, {player} won!\n")
    print("    ", end="")
    for i in range(len(board)):
        print(chr(i + 65), end="  ")
    print()
    for i in range(len(board)):
        print((i + 1), end="  ")
        for j in range(len(board)):
            print(board[i][j], end=" ")
        print()

def human_vs_human(player_1, player_2, board_player_1, board_player_2):
    winner = False
    current_player = player_1
    player_board = board_player_1
    opponent_board = board_player_2
    while not winner:
        clear_screen()
        opponent_board, winner = player_move(current_player, opponent_board, player_board)
        if winner:
            display_win(current_player, opponent_board)
            break
        if current_player == player_1:
            current_player = player_2
            player_board = board_player_2
            opponent_board = board_player_1
        else:
            current_player = player_1
            player_board = board_player_1
            opponent_board = board_player_2
        input(f"Now is {current_player}'s turn. Pres enter to continue...")

def human_vs_ai(human, ai_player, human_board, ai_board):
    winner = False
    while not winner:
        clear_screen()
        ai_board, winner = player_move(human, ai_board, human_board)
        if winner:
            display_win(human, ai_board)
            break
        human_board, winner = ai_move(human_board, ai_player)
        if winner:
            display_win(ai_player, human_board)
            break

if __name__ == "__main__":
    player_1, player_2, board_player_1, board_player_2 = menu()
    clear_screen()
    input("Game begins. Press enter to continue...")
    if player_2 == "AI player":
        human_vs_ai(player_1, player_2, board_player_1, board_player_2)
    else:
        human_vs_human(player_1, player_2, board_player_1, board_player_2)