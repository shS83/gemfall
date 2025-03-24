from copy import copy
import commons as c
import random


class Tgem:

    def __init__(self, spos=None, epos=None, stype=0):

        self.gem1 = c.board[spos[0]][spos[1]]
        self.gem2 = c.board[epos[0]][epos[1]]
        self.tgem1 = copy(self.gem1)
        self.tgem2 = copy(self.gem2)
        self.spos = spos
        self.epos = epos
        self.stype = stype
        self.g1delta_x = 0
        self.g1delta_y = 0
        self.g1dif_x = 0
        self.g1dif_y = 0
        self.g2delta_x = 0
        self.g2delta_y = 0
        self.g2dif_x = 0
        self.g2dif_y = 0
        self.totaldif = 0
        self.finished = False

        if self.tgem1.alive:
            self.g1dif_x = self.tgem2.x - self.tgem1.x
            self.g1dif_y = self.tgem2.y - self.tgem1.y
        if self.tgem2.alive:
            self.g2dif_x = self.tgem1.x - self.tgem2.x
            self.g2dif_y = self.tgem1.y - self.tgem2.y

        if abs(self.g1dif_x) > 0:
            self.g1delta_x = self.g1dif_x / abs(self.g1dif_x) * 2
        else:
            self.g1delta_x = 0
        if abs(self.g1dif_y) > 0:
            self.g1delta_y = self.g1dif_y / abs(self.g1dif_y) * 2
        else:
            self.g1delta_y = 0
        if abs(self.g2dif_x) > 0:
            self.g2delta_x = self.g2dif_x / abs(self.g2dif_x) * 2
        else:
            self.g2delta_x = 0
        if abs(self.g2dif_y) > 0:
            self.g2delta_y = self.g2dif_y / abs(self.g2dif_y) * 2
        else:
            self.g2delta_y = 0

        self.totaldif = self.g1dif_x + self.g1dif_y + self.g2dif_x + self.g2dif_y

    def update(self):
        answer = False

        if self.tgem2 is not None:
            if self.g1delta_x != 0 or self.g1delta_y != 0:
                self.gem1.x += self.g1delta_x
                self.gem1.y += self.g1delta_y

                if self.gem1.x == self.tgem2.x and self.gem1.y == self.tgem2.y:
                    if self.stype == 0:
                        sy, sx = self.spos
                        ey, ex = self.epos
                        c.board[ey][ex] = copy(self.gem1)
                        c.board[sy][sx].x = sx * c.block_w
                        c.board[sy][sx].y = sy * c.block_h
                        c.board[sy][sx].t = 1000 + random.randint(1, 1000)
                        c.board[sy][sx].alive = False
                        c.board[sy][sx].dropping = False
                        c.board[ey][ex].dropping = False

                        for vy in range(ey, c.blocks[1]):
                            c.board[vy][ex].dropping = False

                    self.finished = True
                    self.destroy_t2()
                    answer = 3

        if self.tgem1 is not None:
            if self.g2delta_x != 0 or self.g2delta_y != 0 and self.stype == 1:
                self.gem2.x += self.g2delta_x
                self.gem2.y += self.g2delta_y
                if self.gem2.x == self.tgem1.x and self.gem2.y == self.tgem1.y:
                    sy, sx = self.spos
                    ey, ex = self.epos
                    c.board[ey][ex] = copy(self.gem1)
                    c.board[sy][sx] = copy(self.gem2)
                    c.board[ey][ex].dropping = False
                    c.board[sy][sx].dropping = False
                    self.finished = True
                    self.destroy_t1()
                    answer = 3

        return answer

    def destroy_t1(self):
        self.g2delta_x = 0
        self.g2delta_y = 0
        self.g2dif_x = 0
        self.g2dif_y = 0
        self.tgem1 = None

    def destroy_t2(self):
        self.g1delta_x = 0
        self.g1delta_y = 0
        self.g1dif_x = 0
        self.g1dif_y = 0
        self.tgem2 = None

tgem_list = []

def process_tgem():
    answer = False

    for item in tgem_list:
        answer = item.update()
        if item.tgem1 is None and item.tgem2 is None:
            tgem_list.remove(item)
            return 3

    return answer
