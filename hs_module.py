import pygame as pg
import pygame.gfxdraw
import os
import commons as c
import images as img

xRES = c.screen_w
yRES = c.screen_h
timer = pygame.time.Clock()
pg.init()

running = True
font = img.hs_font
HOME_DIR = os.getcwd()

high_scores = []
new_score = None
input_text = ""
finished_typing = False
typing_name = False


def load_scores():

    global high_scores

    if len(high_scores) < 1:
        handle = open(f"{HOME_DIR}/gemfall_highscores.txt", "r")
        for line in handle:
            high_scores.append(line.rstrip())
        return True
    return False


def check_score(highscore):

    global high_scores, new_score, finished_typing
    new_score = "NO"

    for e in range(0, len(high_scores)-1):
        user, score = high_scores[e].split(" ")
        if highscore >= int(score):
            finished_typing = False
            new_score = e
            return True
    return False


def fix_scores(index, user, highscore):

    global high_scores

    for e in range(0, len(high_scores)-1):
        if e == index:
            high_scores.insert(index, f"{user} {highscore}")
            high_scores.pop()
            return True
    return False


def save_scores():
    global high_scores
    try:
        handle = open(f"{HOME_DIR}/gemfall_highscores.txt", "w")
        for score in high_scores:
            handle.write(score + "\n")
        return True
    except OSError:
        print("Could not open/read highscore file")
        return False


def blend_fill(screen, fade_to):
    color = fade_to
    screen.fill((color, color, color), None, special_flags=pygame.BLEND_RGBA_SUB)


def draw_input(color):

    global input_text

    size_surf = font.render("MMMMMMMMMM", True, (0, 0, 0))
    font_w = size_surf.get_width()
    font_h = size_surf.get_height()
    rect_w = font_w + 20
    rect_h = font_h + 20
    text_surface = font.render(input_text, True, (255, 255, 255))
    alpha_surface = pg.Surface((rect_w, rect_h))
    outer_rect = pg.Rect(0, 0, rect_w, rect_h)
    input_rect = pg.Rect(5, 5, rect_w - 10, rect_h - 10)
    pg.draw.rect(alpha_surface, (255, 255, 255), outer_rect)
    pg.draw.rect(alpha_surface, color, input_rect)
    alpha_surface.set_alpha(160)
    input_x = xRES / 2 - text_surface.get_width() / 2
    blit_x = xRES / 2 - alpha_surface.get_width() / 2
    blit_y = yRES - alpha_surface.get_height() / 2 - 200
    font_surface = font.render("Please enter your name:", True, (255, 255, 255))
    text_blit_x = xRES / 2 - font_surface.get_width() / 2
    c.screen.blit(font_surface, (text_blit_x, blit_y - 50))
    c.screen.blit(alpha_surface, (blit_x, blit_y))
    c.screen.blit(text_surface, (input_x, blit_y + 8))


def scores(fontname, fsize):

    global high_scores

    hs_font = pygame.font.Font(f"{HOME_DIR}/assets/{fontname}", int(round(fsize*1.2)))
    score_font = pygame.font.Font(f"{HOME_DIR}/assets/{fontname}", fsize)
    hstext = "HALL OF FAME"
    hsblit = hs_font.render(hstext, True, (255, 255, 255))
    hsize = hs_font.size(hstext)
    c.screen.blit(hsblit, (xRES/2-hsize[0]/2, yRES/10))
    maxlen = len(high_scores)

    if maxlen > 10:
        maxlen = 10

    for i in range(0, maxlen):
        user, score = high_scores[i].split(" ")
        usize = score_font.size(user)
        ssize = score_font.size(score)
        userblit = score_font.render(user, True, (255, 255, 255))
        scoreblit = score_font.render(score, True, (255, 255, 255))
        c.screen.blit(userblit, (xRES / 2 - 175, yRES / 10 + 50 + (usize[1] + 30 * i)))
        c.screen.blit(scoreblit, (xRES / 2 + (175 - ssize[0]), yRES / 10 + 50 + (ssize[1] + 30 * i)))
