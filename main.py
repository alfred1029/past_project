###############################################################################
# This file include all gameplay function of the game
#
###############################################################################

import copy
from splash import splash
from gui import generateGUI, initCard

RANK = {'A': 1, 'J': 11, 'Q': 12, 'K': 13} | {str(i): i for i in range(2, 11)}
SUIT = 'DCHS'

global score, move_count
cache = []                                      # Store game status
top = 0                                         # Top playable card of deck
bottom = 0                                      # Card after last playable card
restart = False                                 # Deck = columns[0]
move_count = 0
score = 0


def print_GUI(columns, stack, print_opt='NONE'):
    generateGUI(columns, stack, score, move_count)
    if print_opt != 'NONE':
        print(f'{print_opt} ', end='')


def restart_game():

    global top, bottom, score, move_count, cache, restart
    top, bottom, score, move_count, cache, restart = 0, 0, 0, 0, [], True
    return


def save_status(columns, stack):                # Copy whole list to cache

    cache_colums = copy.deepcopy(columns)
    cache_stack = copy.deepcopy(stack)
    cache.extend([[cache_colums, cache_stack, top, bottom, score]])
    return


def undo_move(columns, stack):                  # Copy from cache

    global top, bottom, score, move_count
    columns = copy.deepcopy(cache[-1][0])
    stack = copy.deepcopy(cache[-1][1])
    top = cache[-1][2]
    bottom = cache[-1][3]
    score = cache[-1][4]
    move_count += 1
    cache.pop(-1)
    return columns, stack


def flip_deck(columns):                         # Deck = columns[0]

    global top, bottom, score, move_count
    move_count += 1
    if top*-1 < len(columns[0]):
        top -= 1
        columns[0][top][2] = True
        if (bottom - top) > 3:                  # Only 3 cards or less are shown
            bottom -= 1
            columns[0][bottom][2] = False       # Other cards will be closed
    else:
        for cards in columns[0]:                # Reset the shown status
            cards[2] = False
        score -= 100
        if score < 0:
            score = 0
        top = 0
        bottom = 0
    return


def find_card(columns, stack, command):

    try:                                        # card = [suit, rank, status]
        target_card = [command[-1], RANK[''.join(command[:-1])], True]
    except Exception:
        return -1, -1, -1, -1
    card_suit = SUIT.find(target_card[0])
    if card_suit != -1:
        if stack[card_suit] == target_card[1]:  # 1330 means card in stack
            return 1330, 'A+', card_suit, target_card[1]
        if top != 0:                            # For Deck (columns[0])
            if columns[0][top] == target_card:
                return 0, top, card_suit, target_card[1]
        for col in range(1, 8):                 # For columns 1-7
            if not columns[col]:
                continue
            for row in reversed(range(len(columns[col]))):
                if not columns[col][row][2]:
                    break
                if columns[col][row] == target_card:
                    return col, row, card_suit, target_card[1]
    return -1, -1, -1, -1


def move_to_stack(columns, stack, col, row, suit, rank):

    global top, bottom, score, move_count
    if col < 1330:                              # Not in stack
        if row == len(columns[col])-1 or (col == 0 and row == top):
            if stack[suit] == rank-1:           # Check if it is playable card in deck
                save_status(columns, stack)     # Or last card in columns
                score += 10
                move_count += 1
                stack[suit] += 1
                columns[col].pop(row)
                if row > 0 and col != 0:
                    if not columns[col][-1][2]:
                        columns[col][-1][2] = True
                        score += 5
                elif col == 0:                  # Move top, bottom to keep 3 cards in view
                    top += 1
                    if bottom < 0:
                        columns[0][bottom][2] = True
                        bottom += 1
                return True
    return False


def move_to_columns(columns, stack, col, row, suit, rank):

    global move_count, score
    col_t = -1
    if rank == 13:
        for i in range(1, 8):
            if not columns[i]:
                col_t = i
                break
    else:
        target_rank = rank+1
        target_suit = SUIT[(suit+1) % 2::2]
        for i in range(1, 8):
            if columns[i]:
                if columns[i][-1][0] in target_suit and columns[i][-1][1] == target_rank:
                    col_t = i
                    break
    if col_t == -1:
        return False
    save_status(columns, stack)
    move_count += 1
    if col == 1330 and row == 'A+':
        columns[col_t].extend([[SUIT[suit], rank, True]])
        score -= 15
        if score < 0:
            score = 0
        stack[suit] -= 1
    elif col != 0:
        columns[col_t].extend(columns[col][row:])
        columns[col] = columns[col][:row]
        if columns[col]:
            if not columns[col][-1][2]:
                columns[col][-1][2] = True
                score += 5
    else:
        global top, bottom
        columns[col_t].extend([columns[0][row]])
        columns[0].pop(row)
        score += 5
        top += 1
        if bottom < 0:
            columns[0][bottom][2] = True
            bottom += 1
    return True


def play_game():
    splash()
    columns, stack = initCard()
    statement = "Greetings, Challenger! I'm the A range gatekeeper of ENGG1330 Hell.\nTell me, What's your name:"
    print_GUI(columns, stack, statement)
    name = input()
    statement = name + ', I appreciate your courage to come here! \nAnd now you are going to face your fear!'
    while (True):
        print_GUI(columns, stack, statement)
        statement = 'NONE'
        try:
            command = input('Please enter your command: ').upper().split(' ')
        except Exception:
            statement = 'Invalid input! Please try again!'
            continue
        if command[0] == 'EXIT':
            command = input('Are you sure to exit? Your current progress will be lost! Exit? (Y/N): ')
            if command.upper() == 'NO' or command.upper() == 'N':
                statement = 'Welcome are back, ' + name + '!'
            elif command.upper() == 'YES' or command.upper() == 'Y':
                return False
            else:
                command = input("Huh? I would't let you go unless you grade this assignment with full marks!\nFull marks? (Y/N): ")
                if not (command.upper() == 'YES' or command.upper() == 'Y'):
                    statement = "You can't leave unless you change you mind!"
                else:
                    return False
        elif command[0] == 'RESTART':
            command = input('Are you sure to restart game? Your current progress will be lost! Restart? (Y/N): ')
            if command.upper() == 'Y' or command.upper() == 'YES':
                restart_game()
                return restart
            else:
                statement = 'Welcome are back, ' + name + '!'
        elif (command[0] == 'UNDO' or command[0] == 'RE') and len(command) == 1:
            if cache:
                columns, stack = undo_move(columns, stack)
            else:
                statement = name + ', you have reach you limit! No more previous move!'
        elif (command[0] == 'FLIP' or command[0] == 'F') and len(command) == 1:
            if columns[0]:
                save_status(columns, stack)
                flip_deck(columns)
        elif len(command) == 1 or (len(command) == 2 and (command[1] == 'C' or command[1] == 'S')):
            card = find_card(columns, stack, command[0])
            if card[0] == -1:
                statement = 'Invalid input! Please try again!'
                continue
            elif command[-1] == 'C':
                if not move_to_columns(columns, stack, *card):
                    statement = 'No possible move! Please try again!'
            else:
                if not move_to_stack(columns, stack, *card):
                    if command[-1] == 'S':
                        statement = 'No possible move! Please try again!'
                    else:
                        if not move_to_columns(columns, stack, *card):
                            statement = 'No possible move! Please try again!'
            if all(columns[col][row][2] for col in range(1, 8) for row in range(len(columns[col]))):
                global score
                score += (52 - sum(stack)) * 10
                print(f'Congratulations! After this long journey, You Won!\nMoves taken: {move_count} Final score: {score} Grade: A+')
                command = input('Start a new game? (Y/N): ')
                if command.upper() == 'YES' or command.upper() == 'Y':
                    restart_game()
                elif not (command.upper() == 'NO' or command.upper() == 'N'):
                    command = input("Huh? I would't let you go unless you grade this assignment with full marks!\nFull marks? (Y/N): ")
                    if not (command.upper() == 'YES' or command.upper() == 'Y'):
                        restart_game()
                return restart
        else:
            statement = 'Invalid input! Please try again!'


def main():

    while (True):
        if not play_game():
            print('Goodbye! Have a good day!')
            break


main()
