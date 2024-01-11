# coding=utf-8
import copy
import time
from os import system
import platform

initial_board = []  # двумерный массив игрового поля


# функция для очистки консоли
def clear_the_console():
    operation_system = platform.system()  # получаем ОС
    if 'windows' in operation_system:
        system('cls')
    else:
        system('clear')


# чтение игрового поля из консоли
def read_the_board_from_console():
    print("'X' - крестик\n"
          "'O' - нолик\n"
          "'-' - пустая клетка")
    str1 = input()  # ввод первой строки
    str2 = input()  # ввод второй строки
    str3 = input()  # ввод третьей строки

    # temp - временный массив, в котором будут храниться строки игрового поля
    temp = [str1[0] if str1[0] != "-" else " ", str1[1] if str1[1] != "-" else " ", str1[2] if str1[2] != "-" else " "]
    initial_board.append(temp)
    temp = [str2[0] if str2[0] != "-" else " ", str2[1] if str2[1] != "-" else " ", str2[2] if str2[2] != "-" else " "]
    initial_board.append(temp)
    temp = [str3[0] if str3[0] != "-" else " ", str3[1] if str3[1] != "-" else " ", str3[2] if str3[2] != "-" else " "]
    initial_board.append(temp)


# прочитаем игровое поле из файла board.txt
def read_the_board_from_file():
    f = open('board.txt')
    for line in f:
        # temp - временный массив, в котором будут храниться строки игрового поля
        temp = [line[0] if line[0] != "-" else " ", line[1] if line[1] != "-" else " ",
                line[2] if line[2] != "-" else " "]
        initial_board.append(temp)
    f.close()


# функция для проверки пустоты поля
def is_board_empty(board) -> bool:
    is_empty = True
    for i in range(3):
        for j in range(3):
            # если в клетке стоит Х или О, то оно уже не пустое, вернем False
            if board[i][j] == "X" or board[i][j] == "O":
                return False
    return True


# функция для определения выигрышной клеточки противника
def defense(board):
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == "-":
                # в пустую клетку ставим "О" и если после этого противник выиграет, то возвращаем координаты этой клетки
                board[i][j] = "O"
                if is_winner(initial_board, "O"):
                    best_move = (i, j)
                    return best_move
                else:
                    board[i][j] = " "
                    continue
    return best_move


# красивый вывод игрового поля
def print_board(board):
    print("-------------")
    for row in board:
        print("| " + " | ".join(map(str, row)) + " |")
        print("-------------")


# проверяет выиграл ли игрок
def is_winner(board, player) -> bool:
    # проверка по столбцам и строкам
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True

    # проверка по диагоналям
    diagonal1 = all(board[i][i] == player for i in range(3))
    diagonal2 = all(board[i][2 - i] == player for i in range(3))
    if diagonal1 or diagonal2:
        return True

    return False


# оценка состояние игры
def evaluate(board, player):
    # если текущий игрок выиграл, возвращаем 1, проиграл - -1, поле пустое - 0, ничья - Tie
    if is_winner(board, player):
        return 1
    elif is_winner(board, 'X' if player == 'O' else 'O'):
        return -1
    elif all(board[i][j] != ' ' for i in range(3) for j in range(3)):
        return 0
    else:
        return 'Tie'


# алгоритм минимакс
def minimax(board, depth, is_maximizing, player):
    # оцениваем состояние текущего поля для текущего игрока
    result = evaluate(board, player)
    # Если игра завершена (есть победитель или ничья), возвращается оценка текущего состояния игры
    if result != 'Tie':
        return result

    # если максимизируем (ищем выигрыш для "Х"), то функция рекурсивно вызывает себя для каждой пустой клетки поля
    if is_maximizing:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = player
                    eval = minimax(board, depth + 1, False, player)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
        return max_eval
    # если минимизируем, то функция рекурсивно вызывает себя для нахождения минимальной оценки
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X' if player == 'O' else 'O'
                    eval = minimax(board, depth + 1, True, player)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
        return min_eval


# ищет лучший ход
def find_best_move(board, last_player):
    # ставим противоположного игрока
    player = 'O' if last_player == 'X' else 'X'

    best_val = float('-inf')
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                # в пустую клетку ставим символ противника и вызываем функцию минимакс, чтобы получить оценку этого хода
                board[i][j] = player
                move_val = minimax(board, 0, False, player)
                # отменяем последний ход
                board[i][j] = ' '

                if move_val == 1:
                    return i, j

    return best_move


def main():
    last_player = 'O'
    ans = int(input("Как вы хотите вводить игровое поле?\n"
                    "(1) - Консоль\n"
                    "(2) - Файлик\n"))
    clear_the_console()
    if ans == 1:
        read_the_board_from_console()
    elif ans == 2:
        print("В папке с программкой лежит файл 'board.txt'. Введите в него игровое поле и отправтье 'OK',"
              "когда введете")
        print("'X' - крестик\n"
              "'O' - нолик\n"
              "'-' - пустая клетка")
        ans1 = input()
        if ans1 == "OK":
            read_the_board_from_file()
        else:
            print("Не понял ответа...")
            exit(0)
    else:
        print("Не понял ответа...")
        exit(0)

    clear_the_console()
    print("Исходное поле:")
    print_board(initial_board)

    # если ввели пустое поле, то лучший ход будет - занять центральную клетку
    if is_board_empty(initial_board):
        initial_board[1][1] = 'X'
        best_move = (1, 1)
    else:
        best_move = find_best_move(copy.deepcopy(initial_board), last_player)
        initial_board[best_move[0]][best_move[1]] = "X"
        if best_move == (-1, -1):
            best_move = defense(initial_board)
            initial_board[best_move[0]][best_move[1]] = "X"
    if best_move == (-1, -1):
        print("Ход не найден..")
        exit(0)
    print("Хммм...")
    time.sleep(1)
    clear_the_console()
    print(f"Лучший следующий ход: {best_move}")
    print_board(initial_board)


if __name__ == "__main__":
    main()