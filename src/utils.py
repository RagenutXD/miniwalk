import pygame, os

ASSET_PATH = 'assets/'

def load_image(path):
    img = pygame.image.load(ASSET_PATH+path).convert_alpha()
    return img

def load_images(path):
    imgs = []
    for file in os.listdir(ASSET_PATH+path):
        imgs.append(load_image(path+'/'+file)) 
    return imgs

def log_warn(msg):
    print('[WARNING]:', msg) 

def file_name_fmt(date:str):
    # 2026-10-16T04:17:34.793352+00:00
    print(date)
    fmt_str = ''

    for c in date:
        if c == '.': continue
        if c == '+': break
        fmt_str += c

    return fmt_str
        
