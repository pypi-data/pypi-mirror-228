import pygame
from abc import ABCMeta
from typing import final


__all__ = [
  "DisplayService"
]


class EauServiceMeta(ABCMeta):
  _instances_ = {}

  def __call__(cls, *args, **kwds):
    if cls not in cls._instances_:
      instance = super().__call__(*args, **kwds)
      cls._instances_[cls] = instance
    return cls._instances_[cls]


class EauService(metaclass=EauServiceMeta):
  __slots__ = ()


@final
class DisplayService(EauService):
  __slots__ = (
    "_display",
    "background"
  )

  def __init__(self) -> None:
    self._display = pygame.display.set_mode((1920, 1080), pygame.NOFRAME | pygame.FULLSCREEN)
    bg = pygame.Surface(self._display.get_size())
    bg.fill(pygame.Color(105, 50, 168, 186))
    self.background = bg.convert_alpha()

  @property
  def size(self):
    return self._display.get_size()
  
  def draw(self, groups: tuple):
    for group in groups:
      group.draw(self._display)
    pygame.display.flip()

  def clear(self, groups: tuple):
    for group in groups:
      group.clear(self._display, self.background)

  def update(self, groups: tuple, *args, **kwargs):
    for group in groups:
      group.update(*args, display_rect=self.size, **kwargs)