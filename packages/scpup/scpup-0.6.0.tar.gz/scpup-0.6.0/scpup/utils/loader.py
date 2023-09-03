import os
import pygame

__all__ = [
  "load_image",
  "load_sound"
]

BASE_PATH = os.path.join(os.getcwd(), "assets")

def load_image(*paths: str, alpha = True, **rectargs) -> tuple[pygame.Surface, pygame.Rect]:
  path = os.path.join(BASE_PATH, *paths)
  if not os.path.exists(path):
    raise ValueError(f"Path: '{path}' does not exist")
  image = pygame.image.load(path)
  if alpha:
    image = image.convert_alpha()
  else:
    image = image.convert()
  rect = image.get_rect(**rectargs)
  return image, rect

def load_sound(*paths: str):
  path = os.path.join(BASE_PATH, *paths)
  sound = pygame.mixer.Sound(path)
  return sound
