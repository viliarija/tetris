import os
import keyboard
from time import sleep
from random import randint


def random():
    blocks = [Blocks.s_block,
              Blocks.t_block,
              Blocks.j_block,
              Blocks.i_block,
              Blocks.z_block,
              Blocks.l_block,
              Blocks.o_block]

    return blocks[randint(0, 6)]


class Canvas:
    block_matrix = list()
    description = list()
    next_block = list()
    game_over = False
    update_speed = 8
    paused = False
    block = list()
    fixed = list()
    rotation = 0
    cleared = 0
    level = 1
    score = 0
    row = 0

    def touching(self, next_pos, down):
        if True in [(e in self.fixed or e['y'] > 19) for e in next_pos]:
            if down:
                for piece in self.block[self.rotation]:
                    if piece['y'] > 0:
                        self.fixed.append(piece)
                    else:
                        self.end()

                self.rowing()
                self.new()
            else:
                return True

        self.description = self.side()

    def rowing(self):
        screen = [['  ' for j in range(10)] for i in range(20)]
        for piece in self.fixed:
            screen[piece['y']][piece['x']] = '0'
        if ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'] in screen:
            rows = [i for i, x in enumerate(screen) if x == ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']]
            cleared = len(rows)
            for row in rows:
                for piece in reversed(self.fixed):
                    if piece['y'] == row:
                        self.fixed.remove(piece)

                for piece in reversed(self.fixed):
                    if piece['y'] < row:
                        piece['y'] += 1

            self.cleared += cleared

            if cleared < 4:
                self.score += (200 * (cleared - 1) + 100) * self.level
            else:
                self.score += 800 * self.level

            if self.cleared % 10 == 0:
                self.level += 1

            self.update_speed -= 0.2

    def move(self, direction):

        if direction == 'down':
            next_pos = [({'x': e['x'], 'y': (e['y'] + 1)}) for e in self.block[self.rotation]]
            if not self.touching(next_pos, True):
                for rotation in self.block:
                    for block in rotation:
                        block['y'] += 1

        if direction == 'right':
            next_pos = [({'x': (e['x'] + 1), 'y': e['y']}) for e in self.block[self.rotation]]
            check = [(piece['x'] < 9) for piece in self.block[self.rotation]]

            if False not in check:
                if not self.touching(next_pos, False):
                    for rotation in self.block:
                        for block in rotation:
                            block['x'] += 1

        if direction == 'left':
            next_pos = [({'x': (e['x'] - 1), 'y': e['y']}) for e in self.block[self.rotation]]
            check = [(piece['x'] > 0) for piece in self.block[self.rotation]]

            if False not in check:
                if not self.touching(next_pos, False):
                    for rotation in self.block:
                        for block in rotation:
                            block['x'] -= 1

    def new(self):
        self.block = [[], [], [], []]
        block = self.next_block
        self.block_matrix = block

        for rotation_num, rotation in enumerate(block):
            for row_num, row in enumerate(reversed(rotation)):
                for piece_num, piece in enumerate(row):
                    if piece != 0:
                        self.block[rotation_num].append({'x': (4 + piece_num), 'y': (-1 - row_num)})

        self.next_block = random()

        while True:
            check = list()

            for piece in self.block[self.rotation]:
                if piece['y'] <= 0:
                    check.append(False)
                else:
                    check.append(False)

            if False not in check:
                self.move('down')
            else:
                break

    def rotate(self):

        block = [e['x'] for e in (self.block[self.rotation + 1] if (self.rotation < 3) else self.block[0])]

        if False in [(-1 < e < 10) for e in block]:

            if False in [(10 < e) for e in block]:
                if self.rotation == 3:
                    self.move('left')
                    self.move('left')
                else:
                    self.move('left')

            if False in [(-1 < e) for e in block]:
                if self.rotation == 1:
                    self.move('right')
                    self.move('right')
                else:
                    self.move('right')

        if self.rotation < 3:
            self.rotation += 1
        else:
            self.rotation = 0

    def side(self):
        description = []
        block_text = list()
        for row in self.next_block[0]:
            text = ''
            for piece in row:
                if piece == 1:
                    text += '[]'
                else:
                    text += '  '
            block_text.append(text)

        description.append('Next')
        description.append('╔══════════╗')
        if len(block_text) == 3:
            description.append('║' + (' ' * 10) + '║')

        for row in block_text:
            row_text = '║' + row.center(10) + '║'
            description.append(row_text)

        description.append('╚══════════╝')

        description.append('Score')
        description.append(str(self.score))
        description.append('')

        description.append('Cleared')
        description.append(str(self.cleared))
        description.append('')

        description.append('Level')
        description.append(str(self.level))
        description.append('')

        for i in range(len(description)):
            description[i] = description[i].center(12)

        return description

    def load(self):
        self.next_block = random()
        self.description = self.side()
        self.new()

    def display(self):
        screen = [['  ' for j in range(10)] for i in range(20)]
        description = self.description

        for piece in self.block[self.rotation]:
            if 0 <= piece['y'] <= 19:
                screen[piece['y']][piece['x']] = '[]'

        for piece in self.fixed:
            screen[piece['y']][piece['x']] = '[]'

        print('╔' + ('═' * 20) + '╦' + ('═' * 12) + '╗')
        count = 0
        for x in screen:
            print('║', end='')
            for pixel in x:
                print(pixel, end='')
            print('║', end='')
            if count < 16:
                print(description[count], end='║\n')
            else:
                print(' '*11, '║')

            count += 1

        print('╚' + ('═' * 20) + '╩' + ('═' * 12) + '╝')

    def tick(self):
        if not self.paused:
            os.system('clear')

            if keyboard.is_pressed('p'):
                sleep(0.05)
                self.pause()

            if keyboard.is_pressed('down'):
                self.move('down')

            if keyboard.is_pressed('right'):
                self.move('right')

            if keyboard.is_pressed('left'):
                self.move('left')

            if keyboard.is_pressed('up'):
                self.rotate()

            self.display()

        sleep(0.05)

    def update(self):
        while True:
            if not self.paused:
                self.move('down')
            sleep(self.update_speed / 10)

    def end(self):

        self.game_over = True
        text = 'GAME OVER'
        description = self.description

        while self.game_over:
            os.system('clear')
            print('╔' + ('═' * 20) + '╦' + ('═' * 12) + '╗')

            for i in range(20):
                if i == 9:
                    print('║' + text.center(20), end='║')
                else:
                    print('║' + ' '*20 + '║', end='')

                if i < 16:
                    print(description[i], end='║\n')
                else:
                    print(' ' * 11, '║')

            print('╚' + ('═' * 20) + '╩' + ('═' * 12) + '╝')
            print("To restart press 'r'")
            if keyboard.is_pressed('r'):
                self.reset()
            sleep(0.05)

    def pause(self):
        self.paused = True
        text = 'PAUSED'
        description = self.description

        while self.paused:
            os.system('clear')
            print('╔' + ('═' * 20) + '╦' + ('═' * 12) + '╗')

            for i in range(20):
                if i == 9:
                    print('║' + text.center(20), end='║')
                else:
                    print('║' + ' '*20 + '║', end='')

                if i < 16:
                    print(description[i], end='║\n')
                else:
                    print(' ' * 11, '║')

            print('╚' + ('═' * 20) + '╩' + ('═' * 12) + '╝')
            print("To unpause press 'p'")

            sleep(0.05)
            if keyboard.is_pressed('p'):
                sleep(0.05)
                self.paused = False

    def reset(self):
        self.block = [[], [], [], []]
        self.block_matrix = list()
        self.description = list()
        self.next_block = list()
        self.game_over = False
        self.update_speed = 8
        self.fixed = list()
        self.rotation = 0
        self.cleared = 0
        self.level = 1
        self.score = 0
        self.row = 0

        self.load()


class Blocks:
    s_block = [
        [[0, 1, 1],
         [1, 1, 0],
         [0, 0, 0]],

        [[0, 1, 0],
         [0, 1, 1],
         [0, 0, 1]],

        [[0, 0, 0],
         [0, 1, 1],
         [1, 1, 0]],

        [[1, 0, 0],
         [1, 1, 0],
         [0, 1, 0]]
    ]

    z_block = [
        [[1, 1, 0],
         [0, 1, 1],
         [0, 0, 0]],

        [[0, 0, 1],
         [0, 1, 1],
         [0, 1, 0]],

        [[0, 0, 0],
         [1, 1, 0],
         [0, 1, 1]],

        [[0, 1, 0],
         [1, 1, 0],
         [1, 0, 0]]
    ]

    t_block = [
        [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]],

        [[0, 1, 0],
         [0, 1, 1],
         [0, 1, 0]],

        [[0, 0, 0],
         [1, 1, 1],
         [0, 1, 0]],

        [[0, 1, 0],
         [1, 1, 0],
         [0, 1, 0]]
    ]

    o_block = [
        [[0, 0, 0],
         [0, 1, 1],
         [0, 1, 1]],

        [[0, 0, 0],
         [0, 1, 1],
         [0, 1, 1]],

        [[0, 0, 0],
         [0, 1, 1],
         [0, 1, 1]],

        [[0, 0, 0],
         [0, 1, 1],
         [0, 1, 1]]
    ]

    l_block = [
        [[0, 0, 1],
         [1, 1, 1],
         [0, 0, 0]],

        [[0, 1, 0],
         [0, 1, 0],
         [0, 1, 1]],

        [[0, 0, 0],
         [1, 1, 1],
         [1, 0, 0]],

        [[1, 1, 0],
         [0, 1, 0],
         [0, 1, 0]]
    ]

    j_block = [
        [[1, 0, 0],
         [1, 1, 1],
         [0, 0, 0]],

        [[0, 1, 1],
         [0, 1, 0],
         [0, 1, 0]],

        [[0, 0, 0],
         [1, 1, 1],
         [0, 0, 1]],

        [[0, 1, 0],
         [0, 1, 0],
         [1, 1, 0]]
    ]

    i_block = [
        [[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],

        [[0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0]],

        [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0]],

        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]],
    ]
