import pygame as pg
import commons as c
from pygame.locals import *
import states as s
import entities as en
import anim_module as an
import random
import combocheck as combo
import images as img
import zoom_module as zoom
import hs_module
import poof_module as poof
import fader as f

timer = pg.time.Clock()
pg.init()
c.screen = pg.display.set_mode([c.screen_w, c.screen_h], SHOWN)
pg.display.set_caption('GEMFALL')
icon_image = img.diamond_5
icon_image.set_colorkey((255, 0, 255))
pg.display.set_icon(icon_image)

start_time = 0
s.game_state = s.GameState.ANIMATING
s.play_state = s.PlayState.LOCKED
s.menu_state = s.MenuState.MAIN


class gem:

    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t
        self.image = img.diamonds[self.t]
        self.alive = True
        self.color = c.COLORS[self.t]
        self.active = False
        self.moving = False
        self.dropping = False

    def blank(self):
        # make dropping type random between 1000 and 2000
        self.t = 1000 + random.randint(1, 1000)
        self.image = img.empty
        self.active = False
        self.moving = False

    def update(self):
        if self.t != 42 and self.t < 1000:
            self.color = c.COLORS[self.t]
            self.image = img.diamonds[self.t]
        else:
            self.color = (255, 255, 255, 0)
            self.image = img.empty
            check_board()

        if self.active:
            self.color = (255, 255, 255, 255)

        if not self.alive:
            self.image = img.empty
            self.color = (0, 0, 0)
            check_board()

    def clear(self):
        self.image = None
        self.x = None
        self.y = None
        self.t = None
        self.color = None
        self.active = None
        self.moving = None


def newgem(x, y):
    return gem(int(x * c.block_w), int(y * c.block_h), random.randint(0, c.types - 1))


def board_dict(v):
    for lines in c.board:
        for piece in lines:
            print(piece.__dict__)
    v += 1
    return v


def draw_board(count, delta):

    if count > 254 or count < 1:
        delta = -delta
    count += delta
    if img.tausta is None:
        pg.draw.rect(c.screen, (80, 80, 100), c.board_outer_rect, 10, 10, 10, 10, 10)
        pg.draw.rect(c.screen, (100, 100, 120), c.board_rect)
    else:
        c.screen.blit(img.tausta, (c.board_outer_rect[0], c.board_outer_rect[1]))
    for by in range(len(c.board)):
        for bx in range(len(c.board[by])):
            block_x = c.board_rect[0] + c.board[by][bx].x
            block_y = c.board_rect[1] + c.board[by][bx].y
            if c.board[by][bx].image is False:
                pg.draw.rect(c.screen, c.board[by][bx].color, (block_x, block_y, c.block_w, c.block_h), 0, 5, 5, 5, 5)
                pg.draw.rect(c.screen, (30, 30, 30), (block_x, block_y, c.block_w, c.block_h), 3, 3, 3, 3, 3)
                pg.draw.rect(c.screen, (50, 50, 50), (block_x, block_y, c.block_w, c.block_h), 1, 3, 3, 3, 3)
            else:
                actual_w = c.board[by][bx].image.get_width()
                if actual_w is not c.block_w:
                    scaled = pg.transform.smoothscale_by(c.board[by][bx].image, c.block_w/actual_w/1.05)
                    c.board[by][bx].image = scaled
                c.screen.blit(c.board[by][bx].image, (block_x, block_y))

            if c.board[by][bx].active:
                pg.draw.rect(c.screen, (count, count, count), (block_x, block_y, c.block_w, c.block_h), 5)
            if c.board[by][bx].moving:
                pg.draw.rect(c.screen, (count, 0, 0), (block_x, block_y, c.block_w, c.block_h), 5)

    return count, delta


def set_move_mode():

    if en.player.move is not False:
        (pmx, pmy) = en.player.move
        x = en.player.x
        y = en.player.y

        if (x, y) == en.player.move:
            en.player.moving = False
            en.player.move = False
            return False
        if x - 1 == pmx or x + 1 == pmx or x == pmx:
            if y - 1 == pmy or y + 1 == pmy or y == pmy:
                s.play_state = s.PlayState.LOCKED
                s.game_state = s.GameState.ANIMATING
                an.tgem_list.append(an.t_gem(spos=(y, x), epos=(pmy, pmx), stype=1))
                en.player.move = False
                en.player.moving = False
                return False
        en.player.moving = False
        return True
    else:
        return True


def check_for_dead():

    for y, li in enumerate(c.board):
        for x, piece in enumerate(li):
            if not piece.alive and not piece.dropping:
                if y > 0:
                    s.play_state = s.PlayState.LOCKED
                    s.game_state = s.GameState.ANIMATING

                    to_do = an.t_gem(spos=(y-1, x), epos=(y, x), stype=0)

                    if id(to_do) not in [id(item) for item in an.tgem_list]:
                        an.tgem_list.append(to_do)
                    piece.dropping = True

                elif y < 1:
                    s.play_state = s.PlayState.MOVING
                    c.board[y][x] = newgem(x, y)
                    check_board()

    check_anim_queue()


def check_board():

    # check combos using combocheck

    tmp = combo.clone_with_type(c.board)
    combo.process_another(tmp, c.board, 3)

    # count score

    check_for_dead()

    return True


def check_player(player):

    # check player position against board limits

    if player.x < 0:
        player.x = 0
    elif player.x > c.blocks[0]-1:
        player.x = c.blocks[0]-1
    if player.y < 0:
        player.y = 0
    elif player.y > c.blocks[1]-1:
        player.y = c.blocks[1]-1

    # clear active and moving checks

    for i in range(len(c.board)):
        for j in range(len(c.board[i])):
            c.board[i][j].active = False
            if not player.moving:
                c.board[i][j].moving = False

    c.board[player.y][player.x].active = True
    if player.moving:
        if player.move is not False:
            pass
        else:
            c.board[player.y][player.x].moving = True
            player.move = (player.x, player.y)

    if not player.alive:
        s.play_state = s.PlayState.GAME_OVER

    return True


def check_anim_queue():
    for item in an.tgem_list:
        if item.finished or item.totaldif == 0:
            an.tgem_list.remove(item)


def view_high_scores():
    hs_module.scores('Emmett__.ttf', 24)
    ng_textsurf = img.font.render('press spacebar for new game...', True, (255, 255, 255))
    c.screen.blit(ng_textsurf, (c.screen_w/2 - ng_textsurf.get_width() / 2, c.screen_h - 100))


def view_hs_input():
    hs_module.finished_typing = False
    hs_module.typing_name = True
    hs_module.draw_input((10, 10, 10))
    c.screen.blit(img.new_hs_text, (c.screen_w/2 - img.new_hs_text.get_width() / 2, 300))


def new_game():

    global start_time

    hs_module.finished_typing = False
    hs_module.typing_name = False
    start_time = pg.time.get_ticks()
    an.tgem_list.clear()
    en.player = en.playerobj()
    s.play_state = s.PlayState.LOCKED
    s.end_state = s.EndState.NORMAL

    # populate board

    if len(c.board) < 1:
        for ay in range(0, c.blocks[1]):
            line = []
            for ax in range(0, c.blocks[0]):
                line.append(gem(int(ax * c.block_w), int(ay * c.block_h), random.randint(0, c.types - 1)))
            c.board.append(line)
    else:
        for line in c.board:
            for item in line:
                item.alive = False
                item.t = 1000 + random.randint(1, 1000)

    c.board[0][0].active = True
    en.player.locked = True
    if s.game_state != s.GameState.FADING:
        begin_zoom()
    return True


def begin_zoom():
    s.game_state = s.GameState.ANIMATING
    font_surface = img.die_font.render('BEGIN', True, (255, 255, 255))
    zoom.zoomed = False
    zoom.add_zoomer(font_surface, c.screen_w / 2, c.screen_h / 2, 1.02, 0.75, rot_start=-300, sca_start=0.1,
                    sca_max=2.0, opacity_delta=-1, opa_min=0.01, persistent=False)


def end_zoom():
    s.game_state = s.GameState.ANIMATING
    font_surface = img.die_font.render('YOU DIED', True, (255, 0, 0))
    zoom.zoomed = False
    zoom.add_zoomer(font_surface, c.screen_w / 2, c.screen_h / 2, 1.01, 1.00, sca_max=2.0, opacity_delta=-1,
                    opa_min=0.01, persistent=False)


def dim():

    dimmer = pg.Surface((c.screen_w, c.screen_h))
    dimmer.set_alpha(100)
    c.screen.blit(dimmer, (0, 0))


def game_over():

    en.player.locked = True

    if len(zoom.zoomers) < 1 and s.end_state == s.EndState.NORMAL:
        s.game_state = s.GameState.ANIMATING
        hs_module.load_scores()
        hs_module.check_score(en.player.score)
        s.end_state = s.EndState.ENDGAME
        end_zoom()

    if zoom.zoomed and s.end_state == s.EndState.ENDGAME:
        if hs_module.new_score == 'NO':
            s.game_state = s.GameState.HIGH_SCORES
        elif hs_module.new_score is not None:
            s.game_state = s.GameState.HS_TYPING

    return True


def main():

    global start_time

    count = 1
    delta = 1
    time_left = en.player.time

    new_game()

    f.faders.append(f.fader(delta=-1, a_cap=100))
    s.game_state = s.GameState.FADING

    running = True

    while running:

        now = pg.time.get_ticks()

        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

                # DEBUG NONSENSE START

                # if event.key == K_b:
                #     for item in an.tgem_list:
                #         print(f'vars {vars(item)}')
                #         print(f'id {id(item)}')
                #
                # if event.key == K_k:
                #     en.player.alive = False
                #
                # if event.key == K_p:
                #     print(f'gamestate {s.game_state}')
                #     print(f'playstate {s.play_state}')
                #     print(f'zoomed {zoom.zoomed}')
                #     print(f'zoomers {len(zoom.zoomers)}')
                #     print(f'an tgem list size {len(an.tgem_list)}')
                #     print(f'process tgem {an.process_tgem()}')
                #
                #
                # if event.key == K_d:
                #     board_dict(0)

                # DEBUG NONSENSE END

                if s.game_state == s.GameState.HS_TYPING:
                    if event.key == K_SPACE:
                        pass
                    elif event.key == K_RETURN:
                        if hs_module.input_text != '':
                            en.player.name = hs_module.input_text
                            hs_module.fix_scores(hs_module.new_score, en.player.name, en.player.score)
                            hs_module.save_scores()
                        hs_module.finished_typing = True
                        hs_module.typing_name = False
                        hs_module.new_score = 'NO'
                        s.game_state = s.GameState.HIGH_SCORES
                    elif event.key == K_BACKSPACE:
                        hs_module.input_text = hs_module.input_text[:-1]

                    else:
                        if len(hs_module.input_text) < 10:
                            hs_module.input_text += event.unicode

                if en.player.alive and not en.player.locked:
                    if event.key == K_LEFT:
                        en.player.x -= 1

                    elif event.key == K_RIGHT:
                        en.player.x += 1

                    elif event.key == K_UP:
                        en.player.y -= 1

                    elif event.key == K_DOWN:
                        en.player.y += 1

                    elif event.key == K_SPACE and s.play_state != s.PlayState.LOCKED:
                        if set_move_mode():
                            en.player.moving = not en.player.moving

                if s.game_state == s.GameState.HIGH_SCORES and s.play_state == s.PlayState.GAME_OVER:
                    if event.key == K_SPACE:
                        hs_module.new_score = None
                        hs_module.input_text = ''
                        time_left = en.player.time
                        new_game()

        for row in c.board:
            for block in row:
                block.update()

        if en.player.alive and not en.player.locked:
            if time_left > 0:
                time_left = round(en.player.time - (now - start_time) / 1000)
            else:
                time_left = 0
                en.player.alive = False

        c.screen.fill((40, 40, 60))
        c.screen.blit(img.logo, (175, 10))
        c.screen.blit(img.font.render(f'TIME: {time_left}', True, 'white'), (30, 30))
        c.screen.blit(img.font.render(f'SCORE: {en.player.score}', True, 'white'), (30, 60))

        count, delta = draw_board(count, delta)

        if s.play_state == s.PlayState.GAME_OVER:
            game_over()
        else:
            check_player(en.player)

        if s.game_state == s.GameState.HS_TYPING:
            dim()
            view_hs_input()

        if s.game_state == s.GameState.HIGH_SCORES:
            dim()
            view_high_scores()

        poof.spriteGroup.update(c.screen)
        poof.spriteGroup.draw(c.screen)

        if s.game_state == s.GameState.FADING:
            f.process_faders()
            if len(f.faders) < 1:
                s.game_state = s.GameState.ANIMATING
                s.play_state = s.PlayState.LOCKED
                zoom.zoomed = False
                begin_zoom()

        if s.game_state == s.GameState.ANIMATING:

            if an.process_tgem() == 3 and s.play_state != s.PlayState.GAME_OVER:
                s.play_state = s.PlayState.MOVING
                check_board()
                check_anim_queue()

            if zoom.zoomed and s.play_state == s.PlayState.LOCKED:
                s.play_state = s.PlayState.MOVING
                if en.player.locked:
                    check_board()
                    start_time = pg.time.get_ticks()
                    en.player.locked = False

            if not zoom.zoomed or len(zoom.zoomers) > 0:
                dim()
                zoom.blit_zoomers(c.screen)

        pg.display.flip()
        c.delta_time = 0.001 * timer.tick(144)


if __name__ == '__main__':
    main()
    pg.quit()
