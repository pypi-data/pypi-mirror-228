from __future__ import annotations
from ..utils.loader import load_image
import pygame

__all__ = [
  "EauAnimatedSprite",
  "EauSprite",
  "EauMaskedSprite"
]

class EauSprite:
  __slots__ = (
    "__g",
    "image",
    "rect"
  )

  @classmethod
  def using(cls, surface: pygame.Surface, **rectargs) -> EauSprite:
    instance = cls()
    instance.image = surface
    instance.rect = surface.get_rect(**rectargs)
    return instance

  def __init__(self, *paths: str, **rectargs) -> None:
    self.__g = {}
    if len(paths) > 0:
      self.image, self.rect = load_image(*paths, **rectargs)

  def add(self, *groups) -> None:
    for g in groups:
      if hasattr(g, "_spritegroup") and g not in self.__g:
        g.add_internal(self)
        self.add_internal(g)
  
  def remove(self, *groups) -> None:
    for g in groups:
      if g in self.__g:
        g.remove_internal(self)
        self.remove_internal(g)

  def add_internal(self, group):
    self.__g[group] = 0

  def remove_internal(self, group) -> None:
    del self.__g[group]
  
  def update(self, *_, **__) -> None:
    pass

  def kill(self) -> None:
    for g in self.__g:
      g.remove_internal(self)
    self.__g.clear()

  def groups(self) -> list:
    return list(self.__g)
  
  def alive(self) -> bool:
    return bool(self.__g)
  

class EauMaskedSprite(EauSprite):
  __slots__ = (
    "mask",
  )

  @classmethod
  def using(cls, surface: pygame.Surface, **rectargs) -> EauMaskedSprite:
    instance = EauMaskedSprite.using(surface, **rectargs)
    instance.mask = pygame.mask.from_surface(surface)
    return instance


  def __init__(self, *paths: str, **rectargs) -> None:
    super().__init__(*paths, **rectargs)
    if self.image:
      self.mask = pygame.mask.from_surface(self.image)


class EauAnimatedSprite(EauSprite):
  __slots__ = (
    "frames"
  )

  def __init__(self, *paths: str, frames=1, **rectargs) -> None:
    super().__init__(*paths, **rectargs)
    self.frames = frames
