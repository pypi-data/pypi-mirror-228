from __future__ import annotations
import scpup.utils
import scpup.abc
from typing import overload
from typing import Literal

__all__ = [
  "PlayerIdType",
  "EauPlayer"
]

PlayerIdType = Literal["p1", "p2", "p3", "p4"]

class PlayerMeta(type):
  _instances = {}

  @overload
  def __call__(cls, iid: int): ...
  @overload
  def __call__(cls, pid: str): ...
  def __call__(cls, pid_iid: int|str): # type: ignore
    if isinstance(pid_iid, int):
      return next((p for p in cls._instances.values() if p.iid == pid_iid), None)
    else:
      if pid_iid not in cls._instances:
        instance = super().__call__(pid_iid)
        cls._instances[pid_iid] = instance
      return cls._instances[pid_iid]
  

class EauPlayer(scpup.abc.EauNamedGroup, metaclass=PlayerMeta):
  __slots__ = (
    "pid",
    "iid"
  )

  def __init__(self, player_id: PlayerIdType) -> None:
    super().__init__()
    self.pid = player_id
    self.iid: int | None = None

  def add(self, sprite) -> None: 
    if len(self) > 0:
      super().add("cached", list(self.__s)[0])
      scpup.abc.group.EauGroup.empty(self)
    super().add("current", sprite)

  def update(self) -> None:
    super().update("current")

  def draw(self, surface) -> None:
    sprites = self.sprites("current")
    self.draw_internal(surface, sprites)

  def assign_ctrl(self, ctrl):
    self.iid = ctrl.iid
    ctrl.pid = self.pid

  def unassign_ctrl(self):
    ctrl = scpup.utils.ctrl.Ctrl(self.iid)
    if ctrl is not None:
      ctrl.pid = None
    self.iid = None

