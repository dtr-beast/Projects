from collections import OrderedDict
from random import randint
from sys import exit

c = 0
cells = OrderedDict()


def main():
    global cells
    cells = OrderedDict(
        [((1, 3), ' '), ((2, 3), ' '), ((3, 3), ' '),
         ((1, 2), ' '), ((2, 2), ' '), ((3, 2), ' '),
         ((1, 1), ' '), ((2, 1), ' '), ((3, 1), ' ')])

    commands = take_command()
    P1 = User('O') if commands[0] == 'user' else EasyAI('O') if commands[0] == 'easy' else MediumAI('O')
    P2 = User('X') if commands[1] == 'user' else EasyAI('X') if commands[1] == 'easy' else MediumAI('X')

    displayBoard()

    global c
    c = 1
    P1.make_move()
    displayBoard()
    while c < 9:
        P2.make_move()
        displayBoard()
        if checkGameStatus():
            break
        P1.make_move()
        displayBoard()
        if checkGameStatus():
            break


class AI:
    def __init__(self, sign):
        self.sign = sign

    def make_move(self):
        while True:
            x, y = randint(1, 3), randint(1, 3)
            if cells[(x, y)] != ' ':
                continue

            cells[(x, y)] = self.sign
            # displayBoard()
            break


class EasyAI(AI):
    def make_move(self):
        print('Making move level "easy"')
        super(EasyAI, self).make_move()
        # displayBoard()


class MediumAI(AI):
    def make_move(self):
        print('Making move level "medium"')

        # Adding Awareness
        for i in range(1, 4):
            for j in range(1, 4):
                if cells[(i, j)] == cells[(i, (j % 3) + 1)]:
                    if cells[(i, max((j + 2) % 3, 1))] == ' ':
                        cells[(i, max((j + 2) % 3, 1))] = self.sign
                        return None

                elif cells[(i, j)] == cells[((i % 3) + 1, j)]:
                    if cells[(max((i + 2) % 3, 1), j)] == ' ':
                        cells[(max((i + 2) % 3, 1), j)] = self.sign
                        return None
        else:
            if cells[(1, 3)] == cells[(2, 2)]:
                if cells[(3, 1)] == ' ':
                    cells[(3, 1)] = self.sign
                    return None

            elif cells[(2, 2)] == cells[(3, 1)]:
                if cells[(1, 3)] == ' ':
                    cells[(1, 3)] = self.sign
                    return None
            elif cells[(1, 3)] == cells[(3, 1)]:
                if cells[(2, 2)] == ' ':
                    cells[(2, 2)] = self.sign
                    return None
            elif cells[(1, 1)] == cells[(2, 2)]:
                if cells[(3, 3)] == ' ':
                    cells[(3, 3)] = self.sign
                    return None
            elif cells[(2, 2)] == cells[(3, 3)]:
                if cells[(1, 1)] == ' ':
                    cells[(1, 1)] = self.sign
                    return None
            elif cells[(1, 1)] == cells[(3, 3)]:
                if cells[(2, 2)] == ' ':
                    cells[(2, 2)] = self.sign
                    return None

        super(MediumAI, self).make_move()
        # displayBoard()


class User:
    def __init__(self, sign):
        self.sign = sign

    def make_move(self):
        while True:
            move = tuple(map(int, input('Enter the coordinates: ').split()))
            if move[0] > 3 or move[1] > 3:
                print("Coordinates should be from 1 to 3!")
                continue
            elif cells[move] != ' ':
                print("This cell is occupied! Choose another one!")
                continue

            cells[move] = self.sign
            displayBoard()
            break


rCommands = ['user', 'easy', 'medium', 'hard']


def take_command():
    global rCommands
    while True:
        command = input('Input command: ').split()
        if command[0] == 'exit':
            exit()

        if command[0] == 'start':
            if len(command) != 3 and (command[1] not in rCommands) or (command[2] not in rCommands):
                print("Bad parameters!")
            else:
                return command[1:]


def displayBoard() -> None:
    print(f"---------\n"
          f"| {cells[(1, 3)]} {cells[(2, 3)]} {cells[(3, 3)]} |\n"
          f"| {cells[(1, 2)]} {cells[(2, 2)]} {cells[(3, 2)]} |\n"
          f"| {cells[(1, 1)]} {cells[(2, 1)]} {cells[(3, 1)]} |\n"
          f"---------")


def checkGameStatus():
    global c

    if c >= 8:
        print("Draw")
    else:
        c += 1
        x = y = None
        # Horizontal Checks
        if cells[(1, 3)] == cells[(2, 3)] == cells[(3, 3)]:
            x, y = 1, 3
        elif cells[(1, 2)] == cells[(2, 2)] == cells[(3, 2)]:
            x, y = 1, 2
        elif cells[(1, 1)] == cells[(2, 1)] == cells[(3, 1)]:
            x, y = 1, 1
        # Vertical Checks
        elif cells[(1, 3)] == cells[(1, 2)] == cells[(1, 1)]:
            x, y = 1, 3
        elif cells[(2, 3)] == cells[(2, 2)] == cells[(2, 1)]:
            x, y = 2, 3
        elif cells[(3, 3)] == cells[(3, 2)] == cells[(3, 1)]:
            x, y = 3, 3
        # Diagonal Checks
        elif cells[(1, 3)] == cells[(2, 2)] == cells[(3, 1)]:
            x, y = 1, 3
        elif cells[(1, 1)] == cells[(2, 2)] == cells[(3, 3)]:
            x, y = 1, 1

        if x and y is not None and cells[(x, y)] != ' ':
            print(f"{cells[(x, y)]} wins")
        else:
            return False

    return True


if __name__ == '__main__':
    while True:
        main()
