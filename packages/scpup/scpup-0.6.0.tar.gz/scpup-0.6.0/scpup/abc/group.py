from __future__ import annotations
from typing import Iterator
import scpup.utils

__all__ = [
  "EauGroup",
  "EauNamedGroup"
]


class EauGroup:
  _spritegroup = True

  __slots__ = (
    "__s",
    "_lostsprites"
  )

  def __init__(self) -> None:
    self.__s = {}
    self._lostsprites = []

  def __bool__(self) -> bool:
      return len(self) > 0

  def __len__(self) -> int:
      return len(self.__s)

  def __iter__(self) -> Iterator:
      return iter(self.sprites())

  def __contains__(self, sprite) -> bool:
      return sprite in self.__s

  def add_internal(self, sprite) -> None:
    self.__s[sprite] = 0

  def remove_internal(self, sprite) -> None:
    lost_rect = self.__s[sprite]
    if lost_rect:
      self._lostsprites.append(lost_rect)
    del self.__s[sprite]
  
  def sprites(self) -> list:
    return list(self.__s)

  def add(self, *sprites) -> None:
    for sprite in sprites:
      if not sprite in self.__s:
        self.add_internal(sprite)
        sprite.add_internal(self)

  def remove(self, *sprites) -> None:
    for sprite in sprites:
      if sprite in self.__s:
        self.remove_internal(sprite)
        sprite.remove_internal(self)

  def update(self, *args, **kwargs) -> None:
    for sprite in self.sprites():
      sprite.update(*args, **kwargs)

  def draw(self, surface) -> None:
    sprites = self.sprites()
    self.draw_internal(surface, sprites)

  def draw_internal(self, surface, sprites):
    if hasattr(surface, "blits"):
      self.__s.update(
        zip(sprites, surface.blits((spr.image, spr.rect) for spr in sprites))
      )
    else:
      for spr in sprites:
        self.__s[spr] = surface.blit(spr.image, spr.rect)
    self._lostsprites = []

  def clear(self, surface, bg) -> None:
    for lost_clear_rect in self._lostsprites:
      surface.blit(bg, lost_clear_rect, lost_clear_rect)
    for clear_rect in self.__s.values():
      if clear_rect:
        surface.blit(bg, clear_rect, clear_rect)

  def empty(self) -> None:
    for sprite in self.__s:
      self.remove_internal(sprite)
      sprite.remove_internal(self)


class EauNamedGroup(EauGroup):
  __slots__ = (
    "__n",
  )

  def __init__(self) -> None:
    super().__init__()
    self.__n = {}

  def __getitem__(self, key: str):
    if key in self.__n:
      return self.__n[key]
    raise KeyError(f"No group named '{key}'")

  def add(self, name: str, *sprites) -> None:
    super().add(*sprites)
    self.__n[name] = (self.__n[name] if name in self.__n else []) + list(sprites)

  def remove(self, *sprites) -> None:
    super().remove(*sprites)
    for sprite in sprites:
      for s_list in self.__n.values():
        if sprite in s_list:
          del s_list[s_list.index(sprite)]
          break

  def empty(self) -> None:
    super().empty()
    self.__n.clear()

  def sprites(self, name: str | None = None) -> list:
    return super().sprites() if name is None else self.__n[name] if name in self.__n else []
  
  def update(self, name=None, *args, **kwargs) -> None:
    for sprite in self.sprites(name):
      sprite.update(*args, **kwargs)


# TODO: Fix this class...
# class EauAnimationGroup(EauNamedGroup):
#   __slots__ = (
#     "action"
#   )

#   def __init__(self) -> None:
#     super().__init__()
#     self.action = None

#   def set_current(self, sprite):
#     EauGroup.empty(self)
#     EauGroup.add(self, sprite)

#   def do(self, action: scpup.utils.Actions):
#     if action in self.__n:
#       self.set_current(self.__n[action][0])
      
