from itertools import groupby, chain
import random
import entities as en
import poof_module as poof
import commons as c

# def hyper_for_type(arr, n):
#     arr2 = arr.copy()
#     for y2, row in enumerate(arr):
#         for x2, col in enumerate(row):
#             arr2[y2][x2] = arr[y2][x2].t
#     grouped = (list(g) for _, g in groupby(enumerate(arr2), lambda t: t[1]))
#     return [(g[0][0], g[-1][0] + 1) for g in grouped if len(g) >= n]


def hyper(arr, n):
    grouped = (list(g) for _, g in groupby(enumerate(arr), lambda t: t[1]))
    return [(g[0][0], g[-1][0] + 1) for g in grouped if len(g) >= n]


def check_x(tab, n):
    a_list = []
    for y in range(0, len(tab)):
        a_list.append(hyper(tab[y], n))
    return a_list


def check_y(tab, n):
    rows = map(list, zip(*tab))
    grouped_rows = list(chain(*[list(g) for k, g in groupby(rows)]))
    return [hyper(rivi, n) for rivi in grouped_rows]


# def check_x_type(tab, n):
#     a_list = []
#     for y in range(0, len(tab)):
#         a_list.append(hyper_for_type(tab[y], n))
#     return a_list


# def check_y_type(tab, n):
#     rows = map(list, zip(*tab))
#     grouped_rows = list(chain(*[list(g) for k, g in groupby(rows)]))
#     return [hyper_for_type(rivi, n) for rivi in grouped_rows]


def check_xcoord(tab, todo):
    toreturn = []
    for y in range(0, len(tab)):
        if len(todo[y]) > 0:
            toreturn.append([[y, todo[y][0][0]], [y, todo[y][0][1]]])
    return toreturn


def check_ycoord(tab, todo):
    toreturn = []
    for y in range(0, len(tab)):
        if len(todo[y]) > 0:
            toreturn.append([[todo[y][0][0], y], [todo[y][0][1], y]])
    return toreturn


# def blank_xplace(tab, procx):
#     board2 = tab.copy()
#     for y in range(0, len(board2)):
#         for x in range(0, len(board2[y])):
#             for p in range(0, len(procx)):
#                 if y == procx[p][0][1]:  # procx [item] [start / end] [index x = 0, y = 1]
#                     start = procx[p][0][0]
#                     end = procx[p][1][0]
#                     times = end - start
#                     board2[y] = board2[y][:start] + [-1]*times + board2[y][start+times:]
#     return board2
#
#
# def blank_yplace(tab, procy):
#     board2 = tab.copy()
#     for p in range(len(procy)):
#         x_val = procy[p][0][0]
#         y_start = procy[p][0][1]
#         y_end = procy[p][1][1]
#         for t in range(y_end - y_start):
#             # print(f'x {x_val} and y {y_start+t} will become -1')
#             # if board2[y_start+t][x_val].t != 42:
#             #     board2[y_start+t][x_val] = -1
#             board2[y_start+t][x_val].alive = False
#             board2[y_start+t][x_val].t = 1000 + random.randint(1, 1000)
#     return board2
#

def kill_xplace(tab, procx):
    board2 = tab.copy()
    for y in range(0, len(board2)):
        for x in range(0, len(board2[y])):
            for p in range(0, len(procx)):
                if y == procx[p][0][1]:  # procx [item] [start / end] [index x = 0, y = 1]
                    start = procx[p][0][0]
                    end = procx[p][1][0]
                    for n in range(end - start):
                        board2[y][start+n].alive = False
                        board2[y][start+n].t = 1000 + random.randint(1, 1000)

    return board2


def kill_yplace(tab, procy):
    board2 = tab.copy()
    for p in range(len(procy)):
        x_val = procy[p][0][0]
        y_start = procy[p][0][1]
        y_end = procy[p][1][1]
        for t in range(y_end - y_start):
            # print(f'x {x_val} and y {y_start+t} will become -1')
            board2[y_start+t][x_val].alive = False
            # temp fix 20.6.
            board2[y_start+t][x_val].t = 1000 + random.randint(1, 1000)
    return board2


# def do_processing(table, n):
#     xaxis = check_x(table, n)
#     yaxis = check_y(table, n)
#     xlist = check_ycoord(table, xaxis)
#     ylist = check_xcoord(table, yaxis)
#     table = blank_xplace(table, xlist)
#     table = blank_yplace(table, ylist)
#     return table
#

def process_another(table, table2, n):
    xaxis = check_x(table, n)
    yaxis = check_y(table, n)
    xlist = check_ycoord(table, xaxis)
    ylist = check_xcoord(table, yaxis)

    for item in xlist:

        start = item[0][0]
        end = item[1][0]
        y = item[1][1]
        x_count = end - start
        if en.player.alive and not en.player.locked:
            en.player.score += x_count
        for x in range(start, end):
            add_smoke(y, x)

    for item in ylist:

        start = item[0][1]
        end = item[1][1]
        x = item[0][0]
        y_count = end - start
        if en.player.alive and not en.player.locked:
            en.player.score += y_count
        for y in range(start, end):
            add_smoke(y, x)

    table2 = kill_xplace(table2, xlist)
    table2 = kill_yplace(table2, ylist)
    return table2


def add_smoke(i, j):

    poof.add_smoke(c.board_rect[0] + c.board[i][j].x + c.block_w / 2, c.board_rect[1] + c.board[i][j].y + c.block_h / 2,
                   50, c.board[i][j].color)


#
# def count_score(table):
#     for line in table:
#         for piece in line:
#             if not piece.alive and not piece.dropping and en.player.alive:
#                 en.player.score += 1
#     return True

# def do_processing_with_type(table, n):
#     xaxis = check_x_type(table, n)
#     yaxis = check_y_type(table, n)
#     xlist = check_ycoord(table, xaxis)
#     ylist = check_xcoord(table, yaxis)
#     table = blank_xplace(table, xlist)
#     table = blank_yplace(table, ylist)
#     return table


def clone_with_type(arr):
    t2 = []
    l2 = []
    for r in arr:
        for v in r:
            l2.append(v.t)
        t2.append(l2.copy())
        l2.clear()
    return t2


class test:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.t = random.randint(1, 5)
        self.alive = True


def main():

    bsize = 4
    board_of_types = [[test() for _ in range(bsize)] for _ in range(bsize)]

    # copy board to temp

    tmp = clone_with_type(board_of_types)
    print(*tmp, sep='\n')

    # mark all matching as killed

    board_of_types = process_another(tmp, board_of_types, 3)
    for li in board_of_types:
        for it in li:
            print(it.alive, end=', ')
        print()


    board_of_directors = [[0, 1, 2, 3, 4, 5, 6, 7],
                          [1, 2, 2, 1, 2, 1, 2, 2],
                          [0, 2, 2, 3, 3, 4, 4, 4],
                          [6, 6, 2, 6, 6, 2, 6, 4],
                          [7, 8, 7, 8, 7, 8, 7, 4],
                          [9, 1, 1, 1, 7, 8, 7, 4],
                          [0, 0, 1, 0, 0, 1, 0, 1],
                          [3, 3, 4, 4, 5, 5, 6, 6]]

    skateboard = [[0, 1, 2, 3, 4, 5, 6, 7],
                  [1, 2, 5, 1, 2, 1, 2, 2],
                  [0, 2, 2, 3, 3, 4, 7, 4],
                  [6, 6, 1, 6, 5, 2, 6, 1],
                  [7, 8, 6, 6, 6, 8, 7, 4],
                  [9, 1, 5, 6, 7, 8, 7, 4],
                  [0, 0, 1, 0, 0, 1, 0, 1],
                  [3, 3, 4, 4, 5, 5, 6, 6]]

    boarder = [[0, 1, 0, 1],
               [1, 1, 1, 0],
               [0, 1, 0, 1],
               [1, 0, 0, 0]]

    # mark all 'num' or more hit as -1
    num = 3

    # board_of_directors = do_processing(board_of_directors, num)
    # skateboard = do_processing(skateboard, num)
    # boarder = do_processing(boarder, num)

    # for line in board_of_directors:
    #     print(line)
    #
    # print()
    #
    # for line in skateboard:
    #     print(line)
    #
    # print()
    #
    # for line in boarder:
    #     print(line)


if __name__ == '__main__':
    main()