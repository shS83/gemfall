import pygame as pg
import os

pg.init()

ASSET_DIR = os.getcwd() + '/assets'

empty = pg.image.load(f'{ASSET_DIR}/tyhja.png')
logo = pg.image.load(f'{ASSET_DIR}/gemfall_logo.png')
new_hs_text = pg.image.load(f'{ASSET_DIR}/highscore_text.png')
diamond_1 = pg.image.load(f'{ASSET_DIR}/harmaa_timantti.png')
diamond_2 = pg.image.load(f'{ASSET_DIR}/indigo_timantti.png')
diamond_3 = pg.image.load(f'{ASSET_DIR}/keltanen_timantti.png')
diamond_4 = pg.image.load(f'{ASSET_DIR}/oranssi_timantti.png')
diamond_5 = pg.image.load(f'{ASSET_DIR}/punanen_timantti.png')
diamond_6 = pg.image.load(f'{ASSET_DIR}/sininen_timantti.png')
diamond_7 = pg.image.load(f'{ASSET_DIR}/syaani_timantti.png')
diamond_8 = pg.image.load(f'{ASSET_DIR}/vihree_timantti.png')
diamonds = [diamond_1, diamond_2, diamond_3, diamond_4, diamond_5, diamond_6, diamond_7, diamond_8]
tausta = pg.image.load(f'{ASSET_DIR}/pelitausta_2.png')

font = pg.font.Font(f'{ASSET_DIR}/Emmett__.ttf', 18)
die_font = pg.font.Font(f'{ASSET_DIR}/Emmett__.ttf', 100)
hs_font = font
