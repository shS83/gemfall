from enum import Enum


class GameState(Enum):
    MENU = 0
    PLAYING = 1
    ANIMATING = 2
    HS_TYPING = 3
    HIGH_SCORES = 4
    FADING = 5
    GAME_OVER = 6
    ENDGAME = 7


class MenuState(Enum):
    MAIN = 0
    LEVEL_SELECT = 1
    SETTINGS = 2
    CREDITS = 3


class PlayState(Enum):
    MOVING = 0
    SELECTED = 1
    LOCKED = 2
    GAME_OVER = 3


class EndState(Enum):
    NORMAL = 0
    ENDGAME = 1


game_state = GameState.ANIMATING
menu_state = MenuState.MAIN
play_state = PlayState.LOCKED
end_state = EndState.NORMAL
