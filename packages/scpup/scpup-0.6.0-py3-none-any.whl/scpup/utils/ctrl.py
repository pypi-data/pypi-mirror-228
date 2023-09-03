from __future__ import annotations

import pygame
from enum import IntEnum, auto
from abc import abstractmethod, ABCMeta
from typing import overload, final

__all__ = [
  "Actions",
  "Ctrl",
]

@final
class Actions(IntEnum):
  START = auto()
  SELECT = auto()
  GUIDE = auto()
  A = auto()
  B = auto()
  X = auto()
  Y = auto()
  LB = auto()
  RB = auto()
  LT = auto()
  RT = auto()
  LS = auto()
  RS = auto()
  L_UP = auto()
  L_RIGHT = auto()
  L_DOWN = auto()
  L_LEFT = auto()
  R_UP = auto()
  R_RIGHT = auto()
  R_DOWN = auto()
  R_LEFT = auto()
  DPAD_UP = auto()
  DPAD_RIGHT = auto()
  DPAD_DOWN = auto()
  DPAD_LEFT = auto()


class CtrlMappingMeta(ABCMeta):
  _instances_ = {}

  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances_:
      instance = super().__call__(*args, **kwargs)
      cls._instances_[cls] = instance
    return cls._instances_[cls]


class CtrlMapping(metaclass=CtrlMappingMeta):
  __slots__ = ()

  @classmethod
  def get(cls, name: str) -> XboxCtrlMapping | PS4CtrlMapping | PS5CtrlMapping | None:
    if name in ["Xbox Series X Controller", "Xbox One Series X Controller"]:
      return XboxCtrlMapping()
    elif name in ["PS4 Controller", "DualSense Wireless Controller"]:
      return PS4CtrlMapping()
    elif name in ["Sony Interactive Entertainment Wireless Controller"]:
      return PS5CtrlMapping()
    raise ValueError(f"Controller not defined: '{name}'")

  @abstractmethod
  def __getitem__(self, key: int) -> Actions:
    ...


@final
class XboxCtrlMapping(CtrlMapping):
  __slots__ = ()
  def __getitem__(self, key: int) -> Actions:
    if key < 0 or key > 10:
      raise KeyError(f'No mapping for button {key}')
    elif key == 0:
      return Actions.A
    elif key == 1:
      return Actions.B
    elif key == 2:
      return Actions.X
    elif key == 3:
      return Actions.Y
    elif key == 4:
      return Actions.LB
    elif key == 5:
      return Actions.RB
    elif key == 6:
      return Actions.SELECT
    elif key == 7:
      return Actions.START
    elif key == 8:
      return Actions.LS
    elif key == 9:
      return Actions.RS
    elif key == 10:
      return Actions.GUIDE
    raise TypeError('Unexpected Error')
    

@final
class PS4CtrlMapping(CtrlMapping):
  __slots__ = ()
  def __getitem__(self, key: int) -> Actions:
    if key < 0 or key > 14:
      raise KeyError(f'No mapping for button {key}')
    elif key == 0:
      return Actions.A
    elif key == 1:
      return Actions.B
    elif key == 2:
      return Actions.X
    elif key == 3:
      return Actions.Y
    elif key == 4:
      return Actions.SELECT
    elif key == 5:
      return Actions.GUIDE
    elif key == 6:
      return Actions.START
    elif key == 7:
      return Actions.LS
    elif key == 8:
      return Actions.RS
    elif key == 9:
      return Actions.LB
    elif key == 10:
      return Actions.RB
    elif key == 11:
      return Actions.DPAD_UP
    elif key == 12:
      return Actions.DPAD_DOWN
    elif key == 13:
      return Actions.DPAD_LEFT
    elif key == 14:
      return Actions.DPAD_RIGHT
    raise TypeError('Unexpected Error')
    

@final
class PS5CtrlMapping(CtrlMapping):
  __slots__ = ()
  def __getitem__(self, key: int) -> Actions:
    if key < 0 or key > 12:
      raise KeyError(f'No mapping for button {key}')
    elif key == 0:
      return Actions.A
    elif key == 1:
      return Actions.B
    elif key == 2:
      return Actions.X
    elif key == 3:
      return Actions.Y
    elif key == 4:
      return Actions.LB
    elif key == 5:
      return Actions.RB
    elif key == 6:
      return Actions.LT
    elif key == 7:
      return Actions.RT
    elif key == 8:
      return Actions.SELECT
    elif key == 9:
      return Actions.START
    elif key == 10:
      return Actions.GUIDE
    elif key == 11:
      return Actions.LS
    elif key == 12:
      return Actions.RS
    raise TypeError('Unexpected Error')


class CtrlMeta(type):
  _instances: dict[int, Ctrl] = {}

  @overload 
  def __call__(cls, iid: int) -> Ctrl | None: ...
  @overload 
  def __call__(cls, joystick: pygame.joystick.JoystickType) -> Ctrl: ...
  def __call__(cls, val: pygame.joystick.JoystickType | int) -> Ctrl | None: # type: ignore
    if isinstance(val, int):
      return next((ctrl for iid, ctrl in cls._instances.items() if iid == val), None)
    iid = val.get_instance_id()
    if iid not in cls._instances:
      instance = super().__call__(val)
      cls._instances[iid] = instance
    return cls._instances[iid]


@final
class Ctrl(metaclass=CtrlMeta):
  __slots__ = (
    "pid",
    "joystick",
    "mapping",
  )

  def __init__(self, joystick: pygame.joystick.JoystickType) -> None:
    self.pid: str | None = None
    self.mapping = CtrlMapping.get(joystick.get_name())
    self.joystick = joystick

  @property
  def iid(self) -> int:
    return self.joystick.get_instance_id()