delta_time = 0.0
gravity = 650
screen_w = 1024
screen_h = 768
screen = None

COLORS = (100, 100, 100), (200, 0, 255), (255, 255, 0),\
         (255, 200, 0), (255, 0, 0),  (0, 0, 255), \
         (225, 225, 255), (0, 255, 0)

blocks = (8, 8)
types = len(COLORS)
board = []
board_w = 400
board_h = 400
block_w = int(round(board_w / blocks[0]))
block_h = int(round(board_h / blocks[1]))
board_l = int(round(screen_w / 2 - board_w / 2))
board_t = int(round(screen_h / 2 - board_h / 2)) + 50
board_rect = (board_l, board_t, board_w, board_h)
border = 50
board_outer_rect = (board_l - border, board_t - border, board_w + border * 2, board_h + border * 2)
