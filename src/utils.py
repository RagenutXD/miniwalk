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
