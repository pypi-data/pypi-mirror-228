from .nbhandlers import commands
from .wh40kcards import wh40k_cards

wh40k_cards.load()

__type__ = "plugin"
__charactor__ = None
__name__ = "wh40k"
__cname__ = "帝皇的炮灰"
__nbhandler__ = nbhandlers
__nbcommands__ = commands
__description__ = "WH40K 模式是以设定 战锤40K(Warhammer 40,000: Fire Warrior) 为背景的 TRPG 跑团模式."