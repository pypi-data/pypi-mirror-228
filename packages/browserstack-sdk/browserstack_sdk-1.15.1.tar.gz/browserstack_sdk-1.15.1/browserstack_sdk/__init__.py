# coding: UTF-8
import sys
bstack11ll111l_opy_ = sys.version_info [0] == 2
bstack1lll1lll_opy_ = 2048
bstack11l11lll1_opy_ = 7
def bstack1l1ll111_opy_ (bstack11l1l11l1_opy_):
    global bstack1l1ll1l1_opy_
    stringNr = ord (bstack11l1l11l1_opy_ [-1])
    bstack1lllllll1_opy_ = bstack11l1l11l1_opy_ [:-1]
    bstack11l1l11_opy_ = stringNr % len (bstack1lllllll1_opy_)
    bstack1ll11l1_opy_ = bstack1lllllll1_opy_ [:bstack11l1l11_opy_] + bstack1lllllll1_opy_ [bstack11l1l11_opy_:]
    if bstack11ll111l_opy_:
        bstack1l11111l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1lll_opy_ - (bstack1lll11_opy_ + stringNr) % bstack11l11lll1_opy_) for bstack1lll11_opy_, char in enumerate (bstack1ll11l1_opy_)])
    else:
        bstack1l11111l1_opy_ = str () .join ([chr (ord (char) - bstack1lll1lll_opy_ - (bstack1lll11_opy_ + stringNr) % bstack11l11lll1_opy_) for bstack1lll11_opy_, char in enumerate (bstack1ll11l1_opy_)])
    return eval (bstack1l11111l1_opy_)
import atexit
import os
import signal
import sys
import time
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
from multiprocessing import Pool
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack1l1111l1l_opy_ = {
	bstack1l1ll111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࠀ"): bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࠩࠁ"),
  bstack1l1ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩࠂ"): bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡫ࡦࡻࠪࠃ"),
  bstack1l1ll111_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࠄ"): bstack1l1ll111_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࠅ"),
  bstack1l1ll111_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪࠆ"): bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫࠇ"),
  bstack1l1ll111_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪࠈ"): bstack1l1ll111_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࠧࠉ"),
  bstack1l1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪࠊ"): bstack1l1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧࠋ"),
  bstack1l1ll111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࠌ"): bstack1l1ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨࠍ"),
  bstack1l1ll111_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪࠎ"): bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩࠪࠏ"),
  bstack1l1ll111_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫࠐ"): bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡶࡳࡱ࡫ࠧࠑ"),
  bstack1l1ll111_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ࠒ"): bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ࠓ"),
  bstack1l1ll111_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠔ"): bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠕ"),
  bstack1l1ll111_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫࠖ"): bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡼࡩࡥࡧࡲࠫࠗ"),
  bstack1l1ll111_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭࠘"): bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭࠙"),
  bstack1l1ll111_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩࠚ"): bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩࠛ"),
  bstack1l1ll111_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩࠜ"): bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩࠝ"),
  bstack1l1ll111_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨࠞ"): bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨࠟ"),
  bstack1l1ll111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࠠ"): bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࠡ"),
  bstack1l1ll111_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩࠢ"): bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩࠣ"),
  bstack1l1ll111_opy_ (u"ࠬ࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪࠤ"): bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪࠥ"),
  bstack1l1ll111_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧࠦ"): bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧࠧ"),
  bstack1l1ll111_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡶࠫࠨ"): bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡳࡪࡋࡦࡻࡶࠫࠩ"),
  bstack1l1ll111_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭ࠪ"): bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭ࠫ"),
  bstack1l1ll111_opy_ (u"࠭ࡨࡰࡵࡷࡷࠬࠬ"): bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡨࡰࡵࡷࡷࠬ࠭"),
  bstack1l1ll111_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩ࠮"): bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡩࡧࡦࡩࡨࡦࠩ࠯"),
  bstack1l1ll111_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫ࠰"): bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫ࠱"),
  bstack1l1ll111_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࠲"): bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࠳"),
  bstack1l1ll111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࠴"): bstack1l1ll111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ࠵"),
  bstack1l1ll111_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭࠶"): bstack1l1ll111_opy_ (u"ࠪࡶࡪࡧ࡬ࡠ࡯ࡲࡦ࡮ࡲࡥࠨ࠷"),
  bstack1l1ll111_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ࠸"): bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ࠹"),
  bstack1l1ll111_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭࠺"): bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭࠻"),
  bstack1l1ll111_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩ࠼"): bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩ࠽"),
  bstack1l1ll111_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩ࠾"): bstack1l1ll111_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬ࠿"),
  bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧࡀ"): bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧࡁ"),
  bstack1l1ll111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧࡂ"): bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡱࡸࡶࡨ࡫ࠧࡃ"),
  bstack1l1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࡄ"): bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࡅ"),
  bstack1l1ll111_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ࡆ"): bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ࡇ"),
}
bstack1l111111_opy_ = [
  bstack1l1ll111_opy_ (u"࠭࡯ࡴࠩࡈ"),
  bstack1l1ll111_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࡉ"),
  bstack1l1ll111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࡊ"),
  bstack1l1ll111_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࡋ"),
  bstack1l1ll111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧࡌ"),
  bstack1l1ll111_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨࡍ"),
  bstack1l1ll111_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬࡎ"),
]
bstack1l1l11_opy_ = {
  bstack1l1ll111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࡏ"): [bstack1l1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨࡐ"), bstack1l1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡤࡔࡁࡎࡇࠪࡑ")],
  bstack1l1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࡒ"): bstack1l1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ࡓ"),
  bstack1l1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࡔ"): bstack1l1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠨࡕ"),
  bstack1l1ll111_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫࡖ"): bstack1l1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠬࡗ"),
  bstack1l1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࡘ"): bstack1l1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕ࡙ࠫ"),
  bstack1l1ll111_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯࡚ࠪ"): bstack1l1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡆࡘࡁࡍࡎࡈࡐࡘࡥࡐࡆࡔࡢࡔࡑࡇࡔࡇࡑࡕࡑ࡛ࠬ"),
  bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ࡜"): bstack1l1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࠫ࡝"),
  bstack1l1ll111_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫ࡞"): bstack1l1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠬ࡟"),
  bstack1l1ll111_opy_ (u"ࠩࡤࡴࡵ࠭ࡠ"): [bstack1l1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡔࡕࡥࡉࡅࠩࡡ"), bstack1l1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧࡢ")],
  bstack1l1ll111_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧࡣ"): bstack1l1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࡤࡊࡅࡃࡗࡊࠫࡤ"),
  bstack1l1ll111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫࡥ"): bstack1l1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫࡦ")
}
bstack1ll1111l_opy_ = {
  bstack1l1ll111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࡧ"): [bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬࡨ"), bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࡩ")],
  bstack1l1ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࡪ"): [bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩ࡫"), bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ࡬")],
  bstack1l1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡭"): bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡮"),
  bstack1l1ll111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࡯"): bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨࡰ"),
  bstack1l1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡱ"): bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡲ"),
  bstack1l1ll111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧࡳ"): [bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫࡴ"), bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࡵ")],
  bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࡶ"): bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩࡷ"),
  bstack1l1ll111_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡸ"): bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡹ"),
  bstack1l1ll111_opy_ (u"ࠧࡢࡲࡳࠫࡺ"): bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫࡻ"),
  bstack1l1ll111_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡼ"): bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡽ"),
  bstack1l1ll111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡾ"): bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡿ")
}
bstack1ll111ll_opy_ = {
  bstack1l1ll111_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩࢀ"): bstack1l1ll111_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫࢁ"),
  bstack1l1ll111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࢂ"): [bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࢃ"), bstack1l1ll111_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࢄ")],
  bstack1l1ll111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢅ"): bstack1l1ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢆ"),
  bstack1l1ll111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪࢇ"): bstack1l1ll111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ࢈"),
  bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ࢉ"): [bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪࢊ"), bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩࢋ")],
  bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢌ"): bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࢍ"),
  bstack1l1ll111_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪࢎ"): bstack1l1ll111_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬ࢏"),
  bstack1l1ll111_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࢐"): [bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࢑"), bstack1l1ll111_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ࢒")],
  bstack1l1ll111_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࢓"): [bstack1l1ll111_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭࢔"), bstack1l1ll111_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭࢕")]
}
bstack11ll1l1_opy_ = [
  bstack1l1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭࢖"),
  bstack1l1ll111_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫࢗ"),
  bstack1l1ll111_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ࢘"),
  bstack1l1ll111_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶ࢙ࠪ"),
  bstack1l1ll111_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࢚࠭"),
  bstack1l1ll111_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻ࢛ࠪ"),
  bstack1l1ll111_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ࢜"),
  bstack1l1ll111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ࢝"),
  bstack1l1ll111_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭࢞"),
  bstack1l1ll111_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ࢟"),
  bstack1l1ll111_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢠ"),
  bstack1l1ll111_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬࢡ"),
]
bstack11l1llll1_opy_ = [
  bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢢ"),
  bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢣ"),
  bstack1l1ll111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢤ"),
  bstack1l1ll111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࢥ"),
  bstack1l1ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢦ"),
  bstack1l1ll111_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢧ"),
  bstack1l1ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧࢨ"),
  bstack1l1ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩࢩ"),
  bstack1l1ll111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩࢪ"),
  bstack1l1ll111_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬࢫ")
]
bstack1ll1111l1_opy_ = [
  bstack1l1ll111_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ࢬ"),
  bstack1l1ll111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࢭ"),
  bstack1l1ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࢮ"),
  bstack1l1ll111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢯ"),
  bstack1l1ll111_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼࠫࢰ"),
  bstack1l1ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩࢱ"),
  bstack1l1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨࠩࢲ"),
  bstack1l1ll111_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ࢳ"),
  bstack1l1ll111_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࢴ"),
  bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࢵ"),
  bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢶ"),
  bstack1l1ll111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫࢷ"),
  bstack1l1ll111_opy_ (u"࠭࡯ࡴࠩࢸ"),
  bstack1l1ll111_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࢹ"),
  bstack1l1ll111_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧࢺ"),
  bstack1l1ll111_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫࢻ"),
  bstack1l1ll111_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰࠪࢼ"),
  bstack1l1ll111_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ࢽ"),
  bstack1l1ll111_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ࠭ࢾ"),
  bstack1l1ll111_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪࢿ"),
  bstack1l1ll111_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬࣀ"),
  bstack1l1ll111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬࣁ"),
  bstack1l1ll111_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨࣂ"),
  bstack1l1ll111_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧࣃ"),
  bstack1l1ll111_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬࣄ"),
  bstack1l1ll111_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࣅ"),
  bstack1l1ll111_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪࣆ"),
  bstack1l1ll111_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨࣇ"),
  bstack1l1ll111_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬࣈ"),
  bstack1l1ll111_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭ࣉ"),
  bstack1l1ll111_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐࠬ࣊"),
  bstack1l1ll111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋"),
  bstack1l1ll111_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷࠬ࣌"),
  bstack1l1ll111_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬ࣍"),
  bstack1l1ll111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࣎"),
  bstack1l1ll111_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࣏"),
  bstack1l1ll111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࣐࠭"),
  bstack1l1ll111_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪ࣑ࠫ"),
  bstack1l1ll111_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵ࣒ࠪ"),
  bstack1l1ll111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴ࣓ࠩ"),
  bstack1l1ll111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨࣔ"),
  bstack1l1ll111_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩࣕ"),
  bstack1l1ll111_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧࣖ"),
  bstack1l1ll111_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧࣗ"),
  bstack1l1ll111_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨࣘ"),
  bstack1l1ll111_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣙ"),
  bstack1l1ll111_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪࣚ"),
  bstack1l1ll111_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ࣛ"),
  bstack1l1ll111_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫࣜ"),
  bstack1l1ll111_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪࣝ"),
  bstack1l1ll111_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪࣞ"),
  bstack1l1ll111_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫࣟ"),
  bstack1l1ll111_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬ࣠"),
  bstack1l1ll111_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ࣡"),
  bstack1l1ll111_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫ࣢"),
  bstack1l1ll111_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࣣࠧ"),
  bstack1l1ll111_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪࣤ"),
  bstack1l1ll111_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧࣥ"),
  bstack1l1ll111_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨࣦ"),
  bstack1l1ll111_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬࣧ"),
  bstack1l1ll111_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬࣨ"),
  bstack1l1ll111_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࣩࠧ"),
  bstack1l1ll111_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧ࣪"),
  bstack1l1ll111_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨ࣫"),
  bstack1l1ll111_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨ࣬"),
  bstack1l1ll111_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪ࣭ࠪ"),
  bstack1l1ll111_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸ࣮ࠬ"),
  bstack1l1ll111_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࣯"),
  bstack1l1ll111_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࣰࠪ"),
  bstack1l1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸࣱ࠭"),
  bstack1l1ll111_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࣲࠫ"),
  bstack1l1ll111_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ࣳ"),
  bstack1l1ll111_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪࣴ"),
  bstack1l1ll111_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬࣵ"),
  bstack1l1ll111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࣶࠬ"),
  bstack1l1ll111_opy_ (u"࠭ࡩࡦࠩࣷ"),
  bstack1l1ll111_opy_ (u"ࠧࡦࡦࡪࡩࠬࣸ"),
  bstack1l1ll111_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨࣹ"),
  bstack1l1ll111_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨࣺ"),
  bstack1l1ll111_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬࣻ"),
  bstack1l1ll111_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬࣼ"),
  bstack1l1ll111_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫࣽ"),
  bstack1l1ll111_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩࣾ"),
  bstack1l1ll111_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪࣿ"),
  bstack1l1ll111_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࠬऀ"),
  bstack1l1ll111_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦࠩँ"),
  bstack1l1ll111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪं"),
  bstack1l1ll111_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ः"),
  bstack1l1ll111_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࠭ऄ"),
  bstack1l1ll111_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩअ"),
  bstack1l1ll111_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧआ"),
  bstack1l1ll111_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩइ"),
  bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪई"),
  bstack1l1ll111_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨउ"),
  bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ऊ"),
  bstack1l1ll111_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩऋ"),
  bstack1l1ll111_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬऌ"),
  bstack1l1ll111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫऍ"),
  bstack1l1ll111_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫऎ"),
  bstack1l1ll111_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ए"),
  bstack1l1ll111_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨऐ"),
  bstack1l1ll111_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ऑ"),
  bstack1l1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ"),
  bstack1l1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨओ"),
  bstack1l1ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭औ"),
  bstack1l1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪक"),
  bstack1l1ll111_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬख"),
  bstack1l1ll111_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩग"),
  bstack1l1ll111_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭घ"),
  bstack1l1ll111_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨङ")
]
bstack1ll1111ll_opy_ = {
  bstack1l1ll111_opy_ (u"࠭ࡶࠨच"): bstack1l1ll111_opy_ (u"ࠧࡷࠩछ"),
  bstack1l1ll111_opy_ (u"ࠨࡨࠪज"): bstack1l1ll111_opy_ (u"ࠩࡩࠫझ"),
  bstack1l1ll111_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩञ"): bstack1l1ll111_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪट"),
  bstack1l1ll111_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫठ"): bstack1l1ll111_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬड"),
  bstack1l1ll111_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫढ"): bstack1l1ll111_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬण"),
  bstack1l1ll111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬत"): bstack1l1ll111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭थ"),
  bstack1l1ll111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧद"): bstack1l1ll111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨध"),
  bstack1l1ll111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩन"): bstack1l1ll111_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऩ"),
  bstack1l1ll111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫप"): bstack1l1ll111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬफ"),
  bstack1l1ll111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫब"): bstack1l1ll111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬभ"),
  bstack1l1ll111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭म"): bstack1l1ll111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧय"),
  bstack1l1ll111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨर"): bstack1l1ll111_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऱ"),
  bstack1l1ll111_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫल"): bstack1l1ll111_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬळ"),
  bstack1l1ll111_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬऴ"): bstack1l1ll111_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧव"),
  bstack1l1ll111_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨश"): bstack1l1ll111_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩष"),
  bstack1l1ll111_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬस"): bstack1l1ll111_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ह"),
  bstack1l1ll111_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫऺ"): bstack1l1ll111_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧऻ"),
  bstack1l1ll111_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫़ࠧ"): bstack1l1ll111_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩऽ"),
  bstack1l1ll111_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪा"): bstack1l1ll111_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫि"),
  bstack1l1ll111_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪी"): bstack1l1ll111_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫु"),
  bstack1l1ll111_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ू"): bstack1l1ll111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧृ"),
}
bstack1ll11l111_opy_ = bstack1l1ll111_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧॄ")
bstack1ll1_opy_ = bstack1l1ll111_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪॅ")
bstack1l11111l_opy_ = bstack1l1ll111_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬॆ")
bstack11l11l11l_opy_ = {
  bstack1l1ll111_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫे"): 50,
  bstack1l1ll111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩै"): 40,
  bstack1l1ll111_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬॉ"): 30,
  bstack1l1ll111_opy_ (u"ࠬ࡯࡮ࡧࡱࠪॊ"): 20,
  bstack1l1ll111_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬो"): 10
}
bstack1lll111l1_opy_ = bstack11l11l11l_opy_[bstack1l1ll111_opy_ (u"ࠧࡪࡰࡩࡳࠬौ")]
bstack1l111l1l_opy_ = bstack1l1ll111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵्ࠧ")
bstack111l1lll_opy_ = bstack1l1ll111_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧॎ")
bstack1l1ll1ll1_opy_ = bstack1l1ll111_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩॏ")
bstack1l11l11l1_opy_ = bstack1l1ll111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪॐ")
bstack11l1l1111_opy_ = [bstack1l1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭॑"), bstack1l1ll111_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ॒࠭")]
bstack1l11l1ll1_opy_ = [bstack1l1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॓"), bstack1l1ll111_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॔")]
bstack11l11111_opy_ = [
  bstack1l1ll111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪॕ"),
  bstack1l1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬॖ"),
  bstack1l1ll111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨॗ"),
  bstack1l1ll111_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩक़"),
  bstack1l1ll111_opy_ (u"࠭ࡡࡱࡲࠪख़"),
  bstack1l1ll111_opy_ (u"ࠧࡶࡦ࡬ࡨࠬग़"),
  bstack1l1ll111_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪज़"),
  bstack1l1ll111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩड़"),
  bstack1l1ll111_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨढ़"),
  bstack1l1ll111_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩफ़"),
  bstack1l1ll111_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭य़"), bstack1l1ll111_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩॠ"),
  bstack1l1ll111_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪॡ"),
  bstack1l1ll111_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧॢ"),
  bstack1l1ll111_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭ॣ"),
  bstack1l1ll111_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭।"),
  bstack1l1ll111_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬ॥"),
  bstack1l1ll111_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ०"), bstack1l1ll111_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪ१"), bstack1l1ll111_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩ२"), bstack1l1ll111_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩ३"), bstack1l1ll111_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫ४"),
  bstack1l1ll111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨ५"),
  bstack1l1ll111_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨ६"),
  bstack1l1ll111_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧ७"), bstack1l1ll111_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪ८"),
  bstack1l1ll111_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬ९"),
  bstack1l1ll111_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩ॰"),
  bstack1l1ll111_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨॱ"),
  bstack1l1ll111_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫॲ"),
  bstack1l1ll111_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩॳ"),
  bstack1l1ll111_opy_ (u"ࠬࡧࡶࡥࠩॴ"), bstack1l1ll111_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩॵ"), bstack1l1ll111_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩॶ"), bstack1l1ll111_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩॷ"),
  bstack1l1ll111_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧॸ"), bstack1l1ll111_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩॹ"), bstack1l1ll111_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧॺ"),
  bstack1l1ll111_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧॻ"), bstack1l1ll111_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫॼ"),
  bstack1l1ll111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩॽ"), bstack1l1ll111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫॾ"), bstack1l1ll111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧॿ"), bstack1l1ll111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬঀ"), bstack1l1ll111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨঁ"),
  bstack1l1ll111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨং"), bstack1l1ll111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪঃ"),
  bstack1l1ll111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩ঄"),
  bstack1l1ll111_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭অ"),
  bstack1l1ll111_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨআ"), bstack1l1ll111_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫই"), bstack1l1ll111_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩঈ"), bstack1l1ll111_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨউ"),
  bstack1l1ll111_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫঊ"),
  bstack1l1ll111_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩঋ"), bstack1l1ll111_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨঌ"),
  bstack1l1ll111_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩ঍"),
  bstack1l1ll111_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬ঎"),
  bstack1l1ll111_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭এ"),
  bstack1l1ll111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঐ"),
  bstack1l1ll111_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧ঑"),
  bstack1l1ll111_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭঒"),
  bstack1l1ll111_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩও"),
  bstack1l1ll111_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨঔ"),
  bstack1l1ll111_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧক"),
  bstack1l1ll111_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨখ"),
  bstack1l1ll111_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭গ"),
  bstack1l1ll111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬঘ"),
  bstack1l1ll111_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫঙ"),
  bstack1l1ll111_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨচ"),
  bstack1l1ll111_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧছ"),
  bstack1l1ll111_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧজ"),
  bstack1l1ll111_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫঝ"),
  bstack1l1ll111_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩঞ"), bstack1l1ll111_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪট"), bstack1l1ll111_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪঠ"),
  bstack1l1ll111_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬড"),
  bstack1l1ll111_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭ঢ"),
  bstack1l1ll111_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬণ"),
  bstack1l1ll111_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭ত"),
  bstack1l1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩথ"),
  bstack1l1ll111_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮ࠪদ"),
  bstack1l1ll111_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪধ"), bstack1l1ll111_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧন"), bstack1l1ll111_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬ঩"),
  bstack1l1ll111_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪপ"),
  bstack1l1ll111_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬফ"),
  bstack1l1ll111_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧব"),
  bstack1l1ll111_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ভ"),
  bstack1l1ll111_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪম"), bstack1l1ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧয"),
  bstack1l1ll111_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬর"), bstack1l1ll111_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧ঱"),
  bstack1l1ll111_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫল"),
  bstack1l1ll111_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫ঳"),
  bstack1l1ll111_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩ঴"), bstack1l1ll111_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫ঵"), bstack1l1ll111_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬশ"), bstack1l1ll111_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠩষ"),
  bstack1l1ll111_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪস"),
  bstack1l1ll111_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬহ"),
  bstack1l1ll111_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨ঺"),
  bstack1l1ll111_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭঻"),
  bstack1l1ll111_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪ়ࠫ"),
  bstack1l1ll111_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪঽ"),
  bstack1l1ll111_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪা"), bstack1l1ll111_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫি"),
  bstack1l1ll111_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧী"),
  bstack1l1ll111_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬু"),
  bstack1l1ll111_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧূ"),
  bstack1l1ll111_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৃ"),
  bstack1l1ll111_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪৄ"),
  bstack1l1ll111_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬ৅"),
  bstack1l1ll111_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶࠫ৆"),
  bstack1l1ll111_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬে"),
  bstack1l1ll111_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸࠬৈ"),
  bstack1l1ll111_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫ৉"),
  bstack1l1ll111_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬ৊"),
  bstack1l1ll111_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧো"),
  bstack1l1ll111_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨৌ"),
  bstack1l1ll111_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩ্ࠬ"),
  bstack1l1ll111_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭ৎ"),
  bstack1l1ll111_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨ৏"),
  bstack1l1ll111_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧ৐"),
  bstack1l1ll111_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨ৑"),
  bstack1l1ll111_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬ৒"),
  bstack1l1ll111_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨ৓"),
  bstack1l1ll111_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭৔"),
  bstack1l1ll111_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ৕"), bstack1l1ll111_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬ৖"),
  bstack1l1ll111_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪৗ"), bstack1l1ll111_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨ৘"),
  bstack1l1ll111_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭৙"),
  bstack1l1ll111_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬ৚"),
  bstack1l1ll111_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬ৛"),
  bstack1l1ll111_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨড়"), bstack1l1ll111_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨঢ়"),
  bstack1l1ll111_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩ৞"),
  bstack1l1ll111_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬয়"),
  bstack1l1ll111_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨৠ"),
  bstack1l1ll111_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪৡ"),
  bstack1l1ll111_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬৢ"),
  bstack1l1ll111_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧৣ"),
  bstack1l1ll111_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪ৤"),
  bstack1l1ll111_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬ৥"),
  bstack1l1ll111_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩ০"),
  bstack1l1ll111_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧ১"), bstack1l1ll111_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭২"),
  bstack1l1ll111_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪ৩")
]
bstack1l1ll11_opy_ = bstack1l1ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪ৪")
bstack1lllll_opy_ = [bstack1l1ll111_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪ৫"), bstack1l1ll111_opy_ (u"࠭࠮ࡢࡣࡥࠫ৬"), bstack1l1ll111_opy_ (u"ࠧ࠯࡫ࡳࡥࠬ৭")]
bstack1l1l1l111_opy_ = [bstack1l1ll111_opy_ (u"ࠨ࡫ࡧࠫ৮"), bstack1l1ll111_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৯"), bstack1l1ll111_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ৰ"), bstack1l1ll111_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪৱ")]
bstack1ll111_opy_ = {
  bstack1l1ll111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ৲"): bstack1l1ll111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৳"),
  bstack1l1ll111_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ৴"): bstack1l1ll111_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭৵"),
  bstack1l1ll111_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৶"): bstack1l1ll111_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৷"),
  bstack1l1ll111_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৸"): bstack1l1ll111_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৹"),
  bstack1l1ll111_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭৺"): bstack1l1ll111_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ৻")
}
bstack111ll1l_opy_ = [
  bstack1l1ll111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ৼ"),
  bstack1l1ll111_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ৽"),
  bstack1l1ll111_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৾"),
  bstack1l1ll111_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ৿"),
  bstack1l1ll111_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭਀"),
]
bstack11lll1l1_opy_ = bstack11l1llll1_opy_ + bstack1ll1111l1_opy_ + bstack11l11111_opy_
bstack1l1l11lll_opy_ = [
  bstack1l1ll111_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫਁ"),
  bstack1l1ll111_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨਂ"),
  bstack1l1ll111_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧਃ"),
  bstack1l1ll111_opy_ (u"ࠩࡡ࠵࠵࠴ࠧ਄"),
  bstack1l1ll111_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩਅ"),
  bstack1l1ll111_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪਆ"),
  bstack1l1ll111_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫਇ"),
  bstack1l1ll111_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩਈ")
]
bstack1111ll1l_opy_ = bstack1l1ll111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀࠫਉ")
bstack11l11l11_opy_ = bstack1l1ll111_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧਊ")
bstack11lll11_opy_ = [ bstack1l1ll111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ਋") ]
bstack111l1l11_opy_ = [ bstack1l1ll111_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ਌") ]
bstack1ll1lll_opy_ = [ bstack1l1ll111_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ਍") ]
bstack11l11l1l_opy_ = bstack1l1ll111_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧ਎")
bstack1l1l11ll1_opy_ = bstack1l1ll111_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩਏ")
bstack111ll1111_opy_ = bstack1l1ll111_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫਐ")
bstack1l1ll1ll_opy_ = bstack1l1ll111_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ਑")
bstack111lllll_opy_ = [
  bstack1l1ll111_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭਒"),
  bstack1l1ll111_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪਓ"),
  bstack1l1ll111_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬਔ"),
  bstack1l1ll111_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫਕ"),
  bstack1l1ll111_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪਖ"),
  bstack1l1ll111_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨਗ"),
  bstack1l1ll111_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨਘ"),
  bstack1l1ll111_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫਙ"),
  bstack1l1ll111_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬਚ"),
  bstack1l1ll111_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਛ"),
  bstack1l1ll111_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭ਜ"),
  bstack1l1ll111_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬਝ"),
  bstack1l1ll111_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪਞ"),
  bstack1l1ll111_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩਟ"),
  bstack1l1ll111_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ਠ"),
  bstack1l1ll111_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪਡ"),
  bstack1l1ll111_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧਢ"),
  bstack1l1ll111_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਣ"),
  bstack1l1ll111_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧਤ"),
  bstack1l1ll111_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ਥ"),
  bstack1l1ll111_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧਦ"),
]
bstack1l1111ll1_opy_ = bstack1l1ll111_opy_ (u"ࠩ࠱࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠵ࠧਧ")
def bstack1l11l11l_opy_():
  global CONFIG
  headers = {
        bstack1l1ll111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩਨ"): bstack1l1ll111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ਩"),
      }
  proxies = bstack1lll1111l_opy_(CONFIG, bstack1l11111l_opy_)
  try:
    response = requests.get(bstack1l11111l_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1ll1l11ll_opy_ = response.json()[bstack1l1ll111_opy_ (u"ࠬ࡮ࡵࡣࡵࠪਪ")]
      logger.debug(bstack11llll1ll_opy_.format(response.json()))
      return bstack1ll1l11ll_opy_
    else:
      logger.debug(bstack1111l1l_opy_.format(bstack1l1ll111_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧਫ")))
  except Exception as e:
    logger.debug(bstack1111l1l_opy_.format(e))
def bstack1llllll1l_opy_(hub_url):
  global CONFIG
  url = bstack1l1ll111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤਬ")+  hub_url + bstack1l1ll111_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣਭ")
  headers = {
        bstack1l1ll111_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨਮ"): bstack1l1ll111_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ਯ"),
      }
  proxies = bstack1lll1111l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11ll1l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1l111ll1l_opy_.format(hub_url, e))
def bstack1l111lll_opy_():
  try:
    global bstack11lll111l_opy_
    bstack1ll1l11ll_opy_ = bstack1l11l11l_opy_()
    bstack11ll11_opy_ = []
    results = []
    for bstack1llll1_opy_ in bstack1ll1l11ll_opy_:
      bstack11ll11_opy_.append(bstack1lll11l1_opy_(target=bstack1llllll1l_opy_,args=(bstack1llll1_opy_,)))
    for t in bstack11ll11_opy_:
      t.start()
    for t in bstack11ll11_opy_:
      results.append(t.join())
    bstack1ll1l1111_opy_ = {}
    for item in results:
      hub_url = item[bstack1l1ll111_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬਰ")]
      latency = item[bstack1l1ll111_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭਱")]
      bstack1ll1l1111_opy_[hub_url] = latency
    bstack1l1l1lll1_opy_ = min(bstack1ll1l1111_opy_, key= lambda x: bstack1ll1l1111_opy_[x])
    bstack11lll111l_opy_ = bstack1l1l1lll1_opy_
    logger.debug(bstack1l1111l_opy_.format(bstack1l1l1lll1_opy_))
  except Exception as e:
    logger.debug(bstack11l111ll1_opy_.format(e))
bstack1ll111lll_opy_ = bstack1l1ll111_opy_ (u"࠭ࡓࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡲࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠼ࠣࡿࢂ࠭ਲ")
bstack11_opy_ = bstack1l1ll111_opy_ (u"ࠧࡄࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡷࡪࡺࡵࡱࠣࠪਲ਼")
bstack11l111l_opy_ = bstack1l1ll111_opy_ (u"ࠨࡒࡤࡶࡸ࡫ࡤࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠪ਴")
bstack111l1l11l_opy_ = bstack1l1ll111_opy_ (u"ࠩࡖࡥࡳ࡯ࡴࡪࡼࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧਵ")
bstack1lllll1l_opy_ = bstack1l1ll111_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢ࡫ࡹࡧࠦࡵࡳ࡮࠽ࠤࢀࢃࠧਸ਼")
bstack1l11llll_opy_ = bstack1l1ll111_opy_ (u"ࠫࡘ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࡽࢀࠫ਷")
bstack1llll_opy_ = bstack1l1ll111_opy_ (u"ࠬࡘࡥࡤࡧ࡬ࡺࡪࡪࠠࡪࡰࡷࡩࡷࡸࡵࡱࡶ࠯ࠤࡪࡾࡩࡵ࡫ࡱ࡫ࠬਸ")
bstack1l1ll11l1_opy_ = bstack1l1ll111_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࡣࠫਹ")
bstack1l1l111l_opy_ = bstack1l1ll111_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡣࡱࡨࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࡤࠬ਺")
bstack11l1l111_opy_ = bstack1l1ll111_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡄࡴࡵ࡯ࡵ࡮ࡎ࡬ࡦࡷࡧࡲࡺࠢࡳࡥࡨࡱࡡࡨࡧ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠱ࡦࡶࡰࡪࡷࡰࡰ࡮ࡨࡲࡢࡴࡼࡤࠬ਻")
bstack111l1111l_opy_ = bstack1l1ll111_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵ࠮ࠣࡴࡦࡨ࡯ࡵࠢࡤࡲࡩࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࡭࡫ࡥࡶࡦࡸࡹࠡࡲࡤࡧࡰࡧࡧࡦࡵࠣࡸࡴࠦࡲࡶࡰࠣࡶࡴࡨ࡯ࡵࠢࡷࡩࡸࡺࡳࠡ࡫ࡱࠤࡵࡧࡲࡢ࡮࡯ࡩࡱ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡲࡰࡤࡲࡸ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠮ࡲࡤࡦࡴࡺࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠮ࡵࡨࡰࡪࡴࡩࡶ࡯࡯࡭ࡧࡸࡡࡳࡻࡣ਼ࠫ")
bstack1l1llll11_opy_ = bstack1l1ll111_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡧ࡫ࡨࡢࡸࡨࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡦࡪ࡮ࡡࡷࡧࡣࠫ਽")
bstack111l11l1_opy_ = bstack1l1ll111_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡧࡰࡱ࡫ࡸࡱ࠲ࡩ࡬ࡪࡧࡱࡸࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡆࡶࡰࡪࡷࡰ࠱ࡕࡿࡴࡩࡱࡱ࠱ࡈࡲࡩࡦࡰࡷࡤࠬਾ")
bstack11l1l11ll_opy_ = bstack1l1ll111_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡦࠧਿ")
bstack11ll1l11_opy_ = bstack1l1ll111_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡩ࡭ࡳࡪࠠࡦ࡫ࡷ࡬ࡪࡸࠠࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡲࡶࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡹࡧ࡬࡭ࠢࡷ࡬ࡪࠦࡲࡦ࡮ࡨࡺࡦࡴࡴࠡࡲࡤࡧࡰࡧࡧࡦࡵࠣࡹࡸ࡯࡮ࡨࠢࡳ࡭ࡵࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷ࠳࠭ੀ")
bstack11ll111l1_opy_ = bstack1l1ll111_opy_ (u"ࠧࡉࡣࡱࡨࡱ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡱࡵࡳࡦࠩੁ")
bstack11ll11l1_opy_ = bstack1l1ll111_opy_ (u"ࠨࡃ࡯ࡰࠥࡪ࡯࡯ࡧࠤࠫੂ")
bstack1l1l1l1l_opy_ = bstack1l1ll111_opy_ (u"ࠩࡆࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴࠡࡣࡷࠤࡦࡴࡹࠡࡲࡤࡶࡪࡴࡴࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡴ࡬ࠠࠣࡽࢀࠦ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡥ࡯ࡹࡩ࡫ࠠࡢࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰ࠴ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡧ࡭࡭ࠢࡩ࡭ࡱ࡫ࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࡹ࠮ࠨ੃")
bstack1l111l1l1_opy_ = bstack1l1ll111_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡶࡪࡪࡥ࡯ࡶ࡬ࡥࡱࡹࠠ࡯ࡱࡷࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡢࡦࡧࠤࡹ࡮ࡥ࡮ࠢ࡬ࡲࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࠦࡡࡴࠢࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧࠦࡡ࡯ࡦࠣࠦࡦࡩࡣࡦࡵࡶࡏࡪࡿࠢࠡࡱࡵࠤࡸ࡫ࡴࠡࡶ࡫ࡩࡲࠦࡡࡴࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵ࠽ࠤࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊࠨࠠࡢࡰࡧࠤࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠣࠩ੄")
bstack1l1l11l_opy_ = bstack1l1ll111_opy_ (u"ࠫࡒࡧ࡬ࡧࡱࡵࡱࡪࡪࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠿ࠨࡻࡾࠤࠪ੅")
bstack1l1l1l1ll_opy_ = bstack1l1ll111_opy_ (u"ࠬࡋ࡮ࡤࡱࡸࡲࡹ࡫ࡲࡦࡦࠣࡩࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡸࡴࠥ࠳ࠠࡼࡿࠪ੆")
bstack1l1l1ll11_opy_ = bstack1l1ll111_opy_ (u"࠭ࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱ࠭ੇ")
bstack11l111l1_opy_ = bstack1l1ll111_opy_ (u"ࠧࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡎࡲࡧࡦࡲࠧੈ")
bstack11ll1lll_opy_ = bstack1l1ll111_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱࠦࡩࡴࠢࡱࡳࡼࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠡࠨ੉")
bstack1l111l1_opy_ = bstack1l1ll111_opy_ (u"ࠩࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥࡹࡴࡢࡴࡷࠤࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡐࡴࡩࡡ࡭࠼ࠣࡿࢂ࠭੊")
bstack11ll11l1l_opy_ = bstack1l1ll111_opy_ (u"ࠪࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡲ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡼ࡯ࡴࡩࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࢀࢃࠧੋ")
bstack1111ll_opy_ = bstack1l1ll111_opy_ (u"࡚ࠫࡶࡤࡢࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡾࢁࠬੌ")
bstack111l1llll_opy_ = bstack1l1ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡷࡳࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀ੍ࠫ")
bstack1l1lll1l1_opy_ = bstack1l1ll111_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࠠࡢࡰࠣࡥࡵࡶࡲࡰࡲࡵ࡭ࡦࡺࡥࠡࡈ࡚ࠤ࠭ࡸ࡯ࡣࡱࡷ࠳ࡵࡧࡢࡰࡶࠬࠤ࡮ࡴࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠱ࠦࡳ࡬࡫ࡳࠤࡹ࡮ࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡰ࡫ࡹࠡ࡫ࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡮࡬ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡵ࡬ࡱࡵࡲࡥࠡࡲࡼࡸ࡭ࡵ࡮ࠡࡵࡦࡶ࡮ࡶࡴࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡤࡲࡾࠦࡆࡘ࠰ࠪ੎")
bstack1111l_opy_ = bstack1l1ll111_opy_ (u"ࠧࡔࡧࡷࡸ࡮ࡴࡧࠡࡪࡷࡸࡵࡖࡲࡰࡺࡼ࠳࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤࡴࡴࠠࡤࡷࡵࡶࡪࡴࡴ࡭ࡻࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡰࡨࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࠥ࠮ࡻࡾࠫ࠯ࠤࡵࡲࡥࡢࡵࡨࠤࡺࡶࡧࡳࡣࡧࡩࠥࡺ࡯ࠡࡕࡨࡰࡪࡴࡩࡶ࡯ࡁࡁ࠹࠴࠰࠯࠲ࠣࡳࡷࠦࡲࡦࡨࡨࡶࠥࡺ࡯ࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡶࡩࡱ࡫࡮ࡪࡷࡰ࠳ࡷࡻ࡮࠮ࡶࡨࡷࡹࡹ࠭ࡣࡧ࡫࡭ࡳࡪ࠭ࡱࡴࡲࡼࡾࠩࡰࡺࡶ࡫ࡳࡳࠦࡦࡰࡴࠣࡥࠥࡽ࡯ࡳ࡭ࡤࡶࡴࡻ࡮ࡥ࠰ࠪ੏")
bstack1ll11ll1l_opy_ = bstack1l1ll111_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡾࡳ࡬ࠡࡨ࡬ࡰࡪ࠴࠮ࠨ੐")
bstack111lll1ll_opy_ = bstack1l1ll111_opy_ (u"ࠩࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡩࡨࡲࡪࡸࡡࡵࡧࡧࠤࡹ࡮ࡥࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪࠧࠧੑ")
bstack1ll1ll1l1_opy_ = bstack1l1ll111_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦ࠰ࠣࡿࢂ࠭੒")
bstack111l11l1l_opy_ = bstack1l1ll111_opy_ (u"ࠫࡊࡾࡰࡦࡥࡷࡩࡩࠦࡡࡵࠢ࡯ࡩࡦࡹࡴࠡ࠳ࠣ࡭ࡳࡶࡵࡵ࠮ࠣࡶࡪࡩࡥࡪࡸࡨࡨࠥ࠶ࠧ੓")
bstack11lll1_opy_ = bstack1l1ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡩࡻࡲࡪࡰࡪࠤࡆࡶࡰࠡࡷࡳࡰࡴࡧࡤ࠯ࠢࡾࢁࠬ੔")
bstack1l1llllll_opy_ = bstack1l1ll111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡱࡵࡡࡥࠢࡄࡴࡵ࠴ࠠࡊࡰࡹࡥࡱ࡯ࡤࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫ࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡻࡾ࠰ࠪ੕")
bstack1lllll1l1_opy_ = bstack1l1ll111_opy_ (u"ࠧࡌࡧࡼࡷࠥࡩࡡ࡯ࡰࡲࡸࠥࡩ࡯࠮ࡧࡻ࡭ࡸࡺࠠࡢࡵࠣࡥࡵࡶࠠࡷࡣ࡯ࡹࡪࡹࠬࠡࡷࡶࡩࠥࡧ࡮ࡺࠢࡲࡲࡪࠦࡰࡳࡱࡳࡩࡷࡺࡹࠡࡨࡵࡳࡲࠦࡻࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡶࡡࡵࡪ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡩࡵࡴࡶࡲࡱࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀࢀ࠰ࠥࡵ࡮࡭ࡻࠣࠦࡵࡧࡴࡩࠤࠣࡥࡳࡪࠠࠣࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠦࠥࡩࡡ࡯ࠢࡦࡳ࠲࡫ࡸࡪࡵࡷࠤࡹࡵࡧࡦࡶ࡫ࡩࡷ࠴ࠧ੖")
bstack111ll11l1_opy_ = bstack1l1ll111_opy_ (u"ࠨ࡝ࡌࡲࡻࡧ࡬ࡪࡦࠣࡥࡵࡶࠠࡱࡴࡲࡴࡪࡸࡴࡺ࡟ࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠣࡥࡷ࡫ࠠࡼ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡰࡢࡶ࡫ࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡣࡶࡵࡷࡳࡲࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁࢁ࠳ࠦࡆࡰࡴࠣࡱࡴࡸࡥࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡳࡰࡪࡧࡳࡦࠢࡹ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱࡲ࡬ࡹࡲ࠵ࡳࡦࡶ࠰ࡹࡵ࠳ࡴࡦࡵࡷࡷ࠴ࡹࡰࡦࡥ࡬ࡪࡾ࠳ࡡࡱࡲࠪ੗")
bstack111111l1_opy_ = bstack1l1ll111_opy_ (u"ࠩ࡞ࡍࡳࡼࡡ࡭࡫ࡧࠤࡦࡶࡰࠡࡲࡵࡳࡵ࡫ࡲࡵࡻࡠࠤࡘࡻࡰࡱࡱࡵࡸࡪࡪࠠࡷࡣ࡯ࡹࡪࡹࠠࡰࡨࠣࡥࡵࡶࠠࡢࡴࡨࠤࡴ࡬ࠠࡼ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡰࡢࡶ࡫ࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡣࡶࡵࡷࡳࡲࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁࢁ࠳ࠦࡆࡰࡴࠣࡱࡴࡸࡥࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡳࡰࡪࡧࡳࡦࠢࡹ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱࡲ࡬ࡹࡲ࠵ࡳࡦࡶ࠰ࡹࡵ࠳ࡴࡦࡵࡷࡷ࠴ࡹࡰࡦࡥ࡬ࡪࡾ࠳ࡡࡱࡲࠪ੘")
bstack11l1ll111_opy_ = bstack1l1ll111_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡦࡶࡰࠡ࡫ࡧࠤࢀࢃࠠࡧࡱࡵࠤ࡭ࡧࡳࡩࠢ࠽ࠤࢀࢃ࠮ࠨਖ਼")
bstack1ll1llll1_opy_ = bstack1l1ll111_opy_ (u"ࠫࡆࡶࡰࠡࡗࡳࡰࡴࡧࡤࡦࡦࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺ࠰ࠣࡍࡉࠦ࠺ࠡࡽࢀࠫਗ਼")
bstack111llll1_opy_ = bstack1l1ll111_opy_ (u"࡛ࠬࡳࡪࡰࡪࠤࡆࡶࡰࠡ࠼ࠣࡿࢂ࠴ࠧਜ਼")
bstack1lll1l111_opy_ = bstack1l1ll111_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲࠦࡩࡴࠢࡱࡳࡹࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡳࡷࠦࡶࡢࡰ࡬ࡰࡱࡧࠠࡱࡻࡷ࡬ࡴࡴࠠࡵࡧࡶࡸࡸ࠲ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡰࡢࡴࡤࡰࡱ࡫࡬ࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠥࡃࠠ࠲ࠩੜ")
bstack111l1l1ll_opy_ = bstack1l1ll111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࡀࠠࡼࡿࠪ੝")
bstack111llll_opy_ = bstack1l1ll111_opy_ (u"ࠨࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡨࡲ࡯ࡴࡧࠣࡦࡷࡵࡷࡴࡧࡵ࠾ࠥࢁࡽࠨਫ਼")
bstack1ll1l1ll1_opy_ = bstack1l1ll111_opy_ (u"ࠩࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥ࡭ࡥࡵࠢࡵࡩࡦࡹ࡯࡯ࠢࡩࡳࡷࠦࡢࡦࡪࡤࡺࡪࠦࡦࡦࡣࡷࡹࡷ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥ࠯ࠢࡾࢁࠬ੟")
bstack11lll1lll_opy_ = bstack1l1ll111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢࡤࡴ࡮ࠦࡣࡢ࡮࡯࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ੠")
bstack11111ll1_opy_ = bstack1l1ll111_opy_ (u"࡚ࠫࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡪࡲࡻࠥࡨࡵࡪ࡮ࡧࠤ࡚ࡘࡌ࠭ࠢࡤࡷࠥࡨࡵࡪ࡮ࡧࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡷࡶࡩࡩ࠴ࠧ੡")
bstack1111l11_opy_ = bstack1l1ll111_opy_ (u"࡙ࠬࡥࡳࡸࡨࡶࠥࡹࡩࡥࡧࠣࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠮ࡻࡾࠫࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡷࡦࡳࡥࠡࡣࡶࠤࡨࡲࡩࡦࡰࡷࠤࡸ࡯ࡤࡦࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩ࠭ࢁࡽࠪࠩ੢")
bstack1l1l111l1_opy_ = bstack1l1ll111_opy_ (u"࠭ࡖࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡳࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡪࡡࡴࡪࡥࡳࡦࡸࡤ࠻ࠢࡾࢁࠬ੣")
bstack1ll1l111_opy_ = bstack1l1ll111_opy_ (u"ࠧࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡥࡨࡩࡥࡴࡵࠣࡥࠥࡶࡲࡪࡸࡤࡸࡪࠦࡤࡰ࡯ࡤ࡭ࡳࡀࠠࡼࡿࠣ࠲࡙ࠥࡥࡵࠢࡷ࡬ࡪࠦࡦࡰ࡮࡯ࡳࡼ࡯࡮ࡨࠢࡦࡳࡳ࡬ࡩࡨࠢ࡬ࡲࠥࡿ࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨ࠾ࠥࡢ࡮࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰࠱ࠥࡢ࡮ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰ࠿ࠦࡴࡳࡷࡨࠤࡡࡴ࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰ࠫ੤")
bstack1l11lllll_opy_ = bstack1l1ll111_opy_ (u"ࠨࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࡤ࡫ࡲࡳࡱࡵࠤ࠿ࠦࡻࡾࠩ੥")
bstack1l111l1ll_opy_ = bstack1l1ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡࡤࡱࡵࡲࡩࡵࡷࡧࡩࡤ࡫ࡶࡦࡰࡷࠤ࡫ࡵࡲࠡࡕࡇࡏࡘ࡫ࡴࡶࡲࠣࡿࢂࠨ੦")
bstack111ll1l1_opy_ = bstack1l1ll111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥ࡯ࡦࡢࡥࡲࡶ࡬ࡪࡶࡸࡨࡪࡥࡥࡷࡧࡱࡸࠥ࡬࡯ࡳࠢࡖࡈࡐ࡚ࡥࡴࡶࡄࡸࡹ࡫࡭ࡱࡶࡨࡨࠥࢁࡽࠣ੧")
bstack1l111_opy_ = bstack1l1ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡰࡧࡣࡦࡳࡰ࡭࡫ࡷࡹࡩ࡫࡟ࡦࡸࡨࡲࡹࠦࡦࡰࡴࠣࡗࡉࡑࡔࡦࡵࡷࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠠࡼࡿࠥ੨")
bstack1ll1l_opy_ = bstack1l1ll111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡵࡩࡤࡸࡥࡲࡷࡨࡷࡹࠦࡻࡾࠤ੩")
bstack11ll1_opy_ = bstack1l1ll111_opy_ (u"ࠨࡐࡐࡕࡗࠤࡊࡼࡥ࡯ࡶࠣࡿࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡ࠼ࠣࡿࢂࠨ੪")
bstack11l111_opy_ = bstack1l1ll111_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦࡰࡳࡱࡻࡽࠥࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫ੫")
bstack11llll1ll_opy_ = bstack1l1ll111_opy_ (u"ࠨࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡪࡷࡵ࡭ࠡ࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠥࢁࡽࠨ੬")
bstack1111l1l_opy_ = bstack1l1ll111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥ࠵࡮ࡦࡺࡷࡣ࡭ࡻࡢࡴ࠼ࠣࡿࢂ࠭੭")
bstack1l1111l_opy_ = bstack1l1ll111_opy_ (u"ࠪࡒࡪࡧࡲࡦࡵࡷࠤ࡭ࡻࡢࠡࡣ࡯ࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡹ࠺ࠡࡽࢀࠫ੮")
bstack11l111ll1_opy_ = bstack1l1ll111_opy_ (u"ࠫࡊࡘࡒࡐࡔࠣࡍࡓࠦࡁࡍࡎࡒࡇࡆ࡚ࡅࠡࡊࡘࡆࠥࢁࡽࠨ੯")
bstack11ll1l_opy_ = bstack1l1ll111_opy_ (u"ࠬࡒࡡࡵࡧࡱࡧࡾࠦ࡯ࡧࠢ࡫ࡹࡧࡀࠠࡼࡿࠣ࡭ࡸࡀࠠࡼࡿࠪੰ")
bstack1l111ll1l_opy_ = bstack1l1ll111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢ࡯ࡥࡹ࡫࡮ࡤࡻࠣࡪࡴࡸࠠࡼࡿࠣ࡬ࡺࡨ࠺ࠡࡽࢀࠫੱ")
bstack111l111ll_opy_ = bstack1l1ll111_opy_ (u"ࠧࡉࡷࡥࠤࡺࡸ࡬ࠡࡥ࡫ࡥࡳ࡭ࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢࡲࡴࡹ࡯࡭ࡢ࡮ࠣ࡬ࡺࡨ࠺ࠡࡽࢀࠫੲ")
bstack11llll1l1_opy_ = bstack1l1ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡴࡶࡴࡪ࡯ࡤࡰࠥ࡮ࡵࡣࠢࡸࡶࡱࡀࠠࡼࡿࠪੳ")
bstack11lllllll_opy_ = bstack1l1ll111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡰ࡮ࡹࡴࡴ࠼ࠣࡿࢂ࠭ੴ")
bstack11lll_opy_ = bstack1l1ll111_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴ࠼ࠣࡿࢂ࠭ੵ")
bstack1ll11llll_opy_ = bstack1l1ll111_opy_ (u"࡚ࠫࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡰࡢࡥࠣࡪ࡮ࡲࡥࠡࡽࢀ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࡻࡾࠩ੶")
bstack1ll1l1l_opy_ = bstack1l1ll111_opy_ (u"ࠬࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠥࠦࡩࡧࠪࡳࡥ࡬࡫ࠠ࠾࠿ࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠥࢁ࡜࡯ࠢࠣࠤࡹࡸࡹࡼ࡞ࡱࠤࡨࡵ࡮ࡴࡶࠣࡪࡸࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪ࡟ࠫ࡫ࡹ࡜ࠨࠫ࠾ࡠࡳࠦࠠࠡࠢࠣࡪࡸ࠴ࡡࡱࡲࡨࡲࡩࡌࡩ࡭ࡧࡖࡽࡳࡩࠨࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬࠱ࠦࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡱࡡ࡬ࡲࡩ࡫ࡸࠪࠢ࠮ࠤࠧࡀࠢࠡ࠭ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࠪࡤࡻࡦ࡯ࡴࠡࡰࡨࡻࡕࡧࡧࡦ࠴࠱ࡩࡻࡧ࡬ࡶࡣࡷࡩ࠭ࠨࠨࠪࠢࡀࡂࠥࢁࡽࠣ࠮ࠣࡠࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤࢀࡠࠬ࠯ࠩࠪ࡝ࠥ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩࠨ࡝ࠪࠢ࠮ࠤࠧ࠲࡜࡝ࡰࠥ࠭ࡡࡴࠠࠡࠢࠣࢁࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠬ੷")
bstack1_opy_ = bstack1l1ll111_opy_ (u"࠭࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࡢ࡮࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࡜࡯ࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࠡࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻ࡝ࡰࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࡥࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠤࡼࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࡽࡡ࠮࡟ࡲࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࡠࡳࠦࠠࡾࠫ࡟ࡲࢂࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬ੸")
from ._version import __version__
bstack111lll1_opy_ = None
CONFIG = {}
bstack1l11l1l_opy_ = {}
bstack1llll1111_opy_ = {}
bstack1l11ll1l1_opy_ = None
bstack1l1llll_opy_ = None
bstack1ll111l_opy_ = None
bstack11l111ll_opy_ = -1
bstack11lll1111_opy_ = bstack1lll111l1_opy_
bstack1llll11_opy_ = 1
bstack1ll_opy_ = False
bstack11l1l1l_opy_ = False
bstack1l1l1_opy_ = bstack1l1ll111_opy_ (u"ࠧࠨ੹")
bstack11lllll11_opy_ = bstack1l1ll111_opy_ (u"ࠨࠩ੺")
bstack1l111l11l_opy_ = False
bstack1l11l1ll_opy_ = True
bstack1l1l1llll_opy_ = bstack1l1ll111_opy_ (u"ࠩࠪ੻")
bstack1lll1ll11_opy_ = []
bstack11lll111l_opy_ = bstack1l1ll111_opy_ (u"ࠪࠫ੼")
bstack1llll1l1l_opy_ = False
bstack11ll1l111_opy_ = None
bstack1lll1lll1_opy_ = None
bstack11l1l_opy_ = -1
bstack1lll111l_opy_ = os.path.join(os.path.expanduser(bstack1l1ll111_opy_ (u"ࠫࢃ࠭੽")), bstack1l1ll111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ੾"), bstack1l1ll111_opy_ (u"࠭࠮ࡳࡱࡥࡳࡹ࠳ࡲࡦࡲࡲࡶࡹ࠳ࡨࡦ࡮ࡳࡩࡷ࠴ࡪࡴࡱࡱࠫ੿"))
bstack1l1lll111_opy_ = []
bstack11111_opy_ = False
bstack1llll111_opy_ = False
bstack1lll111_opy_ = None
bstack1111lll1l_opy_ = None
bstack1l111llll_opy_ = None
bstack1111l111_opy_ = None
bstack1lll11ll_opy_ = None
bstack1lll11l1l_opy_ = None
bstack11l1111l1_opy_ = None
bstack11l1l1ll1_opy_ = None
bstack1lll11111_opy_ = None
bstack11l11l111_opy_ = None
bstack1l1lll1l_opy_ = None
bstack11l1l1_opy_ = None
bstack1l111111l_opy_ = None
bstack1l11l1_opy_ = None
bstack1l1ll1lll_opy_ = None
bstack1l11l111_opy_ = None
bstack1lllll1_opy_ = None
bstack111lllll1_opy_ = None
bstack11l1l1l1_opy_ = bstack1l1ll111_opy_ (u"ࠢࠣ઀")
class bstack1lll11l1_opy_(threading.Thread):
  def run(self):
    self.exc = None
    try:
      self.ret = self._target(*self._args, **self._kwargs)
    except Exception as e:
      self.exc = e
  def join(self, timeout=None):
    super(bstack1lll11l1_opy_, self).join(timeout)
    if self.exc:
      raise self.exc
    return self.ret
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack11lll1111_opy_,
                    format=bstack1l1ll111_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ઁ"),
                    datefmt=bstack1l1ll111_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫં"))
def bstack1l1111lll_opy_():
  global CONFIG
  global bstack11lll1111_opy_
  if bstack1l1ll111_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬઃ") in CONFIG:
    bstack11lll1111_opy_ = bstack11l11l11l_opy_[CONFIG[bstack1l1ll111_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭઄")]]
    logging.getLogger().setLevel(bstack11lll1111_opy_)
def bstack1l1ll111l_opy_():
  global CONFIG
  global bstack11111_opy_
  bstack1l11l1lll_opy_ = bstack11ll11ll1_opy_(CONFIG)
  if(bstack1l1ll111_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧઅ") in bstack1l11l1lll_opy_ and str(bstack1l11l1lll_opy_[bstack1l1ll111_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨઆ")]).lower() == bstack1l1ll111_opy_ (u"ࠧࡵࡴࡸࡩࠬઇ")):
    bstack11111_opy_ = True
def bstack1ll1ll11l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l1l1l11_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11l1111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1l1ll111_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧઈ") == args[i].lower() or bstack1l1ll111_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥઉ") == args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1l1llll_opy_
      bstack1l1l1llll_opy_ += bstack1l1ll111_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨઊ") + path
      return path
  return None
bstack11l1ll1l_opy_ = re.compile(bstack1l1ll111_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢઋ"))
def bstack1l1l11l1_opy_(loader, node):
    value = loader.construct_scalar(node)
    for group in bstack11l1ll1l_opy_.findall(value):
        if group is not None and os.environ.get(group) is not None:
          value = value.replace(bstack1l1ll111_opy_ (u"ࠧࠪࡻࠣઌ") + group + bstack1l1ll111_opy_ (u"ࠨࡽࠣઍ"), os.environ.get(group))
    return value
def bstack111lll_opy_():
  bstack1111lllll_opy_ = bstack11l1111_opy_()
  if bstack1111lllll_opy_ and os.path.exists(os.path.abspath(bstack1111lllll_opy_)):
    fileName = bstack1111lllll_opy_
  if bstack1l1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ઎") in os.environ and os.path.exists(os.path.abspath(os.environ[bstack1l1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬએ")])) and not bstack1l1ll111_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫઐ") in locals():
    fileName = os.environ[bstack1l1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧઑ")]
  if bstack1l1ll111_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࠭઒") in locals():
    bstack11111l11_opy_ = os.path.abspath(fileName)
  else:
    bstack11111l11_opy_ = bstack1l1ll111_opy_ (u"ࠬ࠭ઓ")
  bstack1l1lllll_opy_ = os.getcwd()
  bstack111lll11l_opy_ = bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩઔ")
  bstack1l11llll1_opy_ = bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫક")
  while (not os.path.exists(bstack11111l11_opy_)) and bstack1l1lllll_opy_ != bstack1l1ll111_opy_ (u"ࠣࠤખ"):
    bstack11111l11_opy_ = os.path.join(bstack1l1lllll_opy_, bstack111lll11l_opy_)
    if not os.path.exists(bstack11111l11_opy_):
      bstack11111l11_opy_ = os.path.join(bstack1l1lllll_opy_, bstack1l11llll1_opy_)
    if bstack1l1lllll_opy_ != os.path.dirname(bstack1l1lllll_opy_):
      bstack1l1lllll_opy_ = os.path.dirname(bstack1l1lllll_opy_)
    else:
      bstack1l1lllll_opy_ = bstack1l1ll111_opy_ (u"ࠤࠥગ")
  if not os.path.exists(bstack11111l11_opy_):
    bstack11lll1l11_opy_(
      bstack1l1l1l1l_opy_.format(os.getcwd()))
  try:
    with open(bstack11111l11_opy_, bstack1l1ll111_opy_ (u"ࠪࡶࠬઘ")) as stream:
        yaml.add_implicit_resolver(bstack1l1ll111_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧઙ"), bstack11l1ll1l_opy_)
        yaml.add_constructor(bstack1l1ll111_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨચ"), bstack1l1l11l1_opy_)
        config = yaml.load(stream, yaml.FullLoader)
        return config
  except:
    with open(bstack11111l11_opy_, bstack1l1ll111_opy_ (u"࠭ࡲࠨછ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11lll1l11_opy_(bstack1l1l11l_opy_.format(str(exc)))
def bstack1l1l_opy_(config):
  bstack111ll11ll_opy_ = bstack1l11ll_opy_(config)
  for option in list(bstack111ll11ll_opy_):
    if option.lower() in bstack1ll1111ll_opy_ and option != bstack1ll1111ll_opy_[option.lower()]:
      bstack111ll11ll_opy_[bstack1ll1111ll_opy_[option.lower()]] = bstack111ll11ll_opy_[option]
      del bstack111ll11ll_opy_[option]
  return config
def bstack1ll11lll1_opy_():
  global bstack1llll1111_opy_
  for key, bstack111l1l111_opy_ in bstack1l1l11_opy_.items():
    if isinstance(bstack111l1l111_opy_, list):
      for var in bstack111l1l111_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1llll1111_opy_[key] = os.environ[var]
          break
    elif bstack111l1l111_opy_ in os.environ and os.environ[bstack111l1l111_opy_] and str(os.environ[bstack111l1l111_opy_]).strip():
      bstack1llll1111_opy_[key] = os.environ[bstack111l1l111_opy_]
  if bstack1l1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩજ") in os.environ:
    bstack1llll1111_opy_[bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬઝ")] = {}
    bstack1llll1111_opy_[bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ઞ")][bstack1l1ll111_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬટ")] = os.environ[bstack1l1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ઠ")]
def bstack1l1ll1l_opy_():
  global bstack1l11l1l_opy_
  global bstack1l1l1llll_opy_
  for idx, val in enumerate(sys.argv):
    if idx<len(sys.argv) and bstack1l1ll111_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨડ").lower() == val.lower():
      bstack1l11l1l_opy_[bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪઢ")] = {}
      bstack1l11l1l_opy_[bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫણ")][bstack1l1ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪત")] = sys.argv[idx+1]
      del sys.argv[idx:idx+2]
      break
  for key, bstack1l1ll1l11_opy_ in bstack1ll1111l_opy_.items():
    if isinstance(bstack1l1ll1l11_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l1ll1l11_opy_:
          if idx<len(sys.argv) and bstack1l1ll111_opy_ (u"ࠩ࠰࠱ࠬથ") + var.lower() == val.lower() and not key in bstack1l11l1l_opy_:
            bstack1l11l1l_opy_[key] = sys.argv[idx+1]
            bstack1l1l1llll_opy_ += bstack1l1ll111_opy_ (u"ࠪࠤ࠲࠳ࠧદ") + var + bstack1l1ll111_opy_ (u"ࠫࠥ࠭ધ") + sys.argv[idx+1]
            del sys.argv[idx:idx+2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx<len(sys.argv) and bstack1l1ll111_opy_ (u"ࠬ࠳࠭ࠨન") + bstack1l1ll1l11_opy_.lower() == val.lower() and not key in bstack1l11l1l_opy_:
          bstack1l11l1l_opy_[key] = sys.argv[idx+1]
          bstack1l1l1llll_opy_ += bstack1l1ll111_opy_ (u"࠭ࠠ࠮࠯ࠪ઩") + bstack1l1ll1l11_opy_ + bstack1l1ll111_opy_ (u"ࠧࠡࠩપ") + sys.argv[idx+1]
          del sys.argv[idx:idx+2]
def bstack1111_opy_(config):
  bstack1ll11l11_opy_ = config.keys()
  for bstack111_opy_, bstackl_opy_ in bstack1l1111l1l_opy_.items():
    if bstackl_opy_ in bstack1ll11l11_opy_:
      config[bstack111_opy_] = config[bstackl_opy_]
      del config[bstackl_opy_]
  for bstack111_opy_, bstackl_opy_ in bstack1ll111ll_opy_.items():
    if isinstance(bstackl_opy_, list):
      for bstack111l1111_opy_ in bstackl_opy_:
        if bstack111l1111_opy_ in bstack1ll11l11_opy_:
          config[bstack111_opy_] = config[bstack111l1111_opy_]
          del config[bstack111l1111_opy_]
          break
    elif bstackl_opy_ in bstack1ll11l11_opy_:
        config[bstack111_opy_] = config[bstackl_opy_]
        del config[bstackl_opy_]
  for bstack111l1111_opy_ in list(config):
    for bstack11l1ll11_opy_ in bstack11lll1l1_opy_:
      if bstack111l1111_opy_.lower() == bstack11l1ll11_opy_.lower() and bstack111l1111_opy_ != bstack11l1ll11_opy_:
        config[bstack11l1ll11_opy_] = config[bstack111l1111_opy_]
        del config[bstack111l1111_opy_]
  bstack1l11ll1ll_opy_ = []
  if bstack1l1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫફ") in config:
    bstack1l11ll1ll_opy_ = config[bstack1l1ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬબ")]
  for platform in bstack1l11ll1ll_opy_:
    for bstack111l1111_opy_ in list(platform):
      for bstack11l1ll11_opy_ in bstack11lll1l1_opy_:
        if bstack111l1111_opy_.lower() == bstack11l1ll11_opy_.lower() and bstack111l1111_opy_ != bstack11l1ll11_opy_:
          platform[bstack11l1ll11_opy_] = platform[bstack111l1111_opy_]
          del platform[bstack111l1111_opy_]
  for bstack111_opy_, bstackl_opy_ in bstack1ll111ll_opy_.items():
    for platform in bstack1l11ll1ll_opy_:
      if isinstance(bstackl_opy_, list):
        for bstack111l1111_opy_ in bstackl_opy_:
          if bstack111l1111_opy_ in platform:
            platform[bstack111_opy_] = platform[bstack111l1111_opy_]
            del platform[bstack111l1111_opy_]
            break
      elif bstackl_opy_ in platform:
        platform[bstack111_opy_] = platform[bstackl_opy_]
        del platform[bstackl_opy_]
  for bstack11ll1llll_opy_ in bstack1ll111_opy_:
    if bstack11ll1llll_opy_ in config:
      if not bstack1ll111_opy_[bstack11ll1llll_opy_] in config:
        config[bstack1ll111_opy_[bstack11ll1llll_opy_]] = {}
      config[bstack1ll111_opy_[bstack11ll1llll_opy_]].update(config[bstack11ll1llll_opy_])
      del config[bstack11ll1llll_opy_]
  for platform in bstack1l11ll1ll_opy_:
    for bstack11ll1llll_opy_ in bstack1ll111_opy_:
      if bstack11ll1llll_opy_ in list(platform):
        if not bstack1ll111_opy_[bstack11ll1llll_opy_] in platform:
          platform[bstack1ll111_opy_[bstack11ll1llll_opy_]] = {}
        platform[bstack1ll111_opy_[bstack11ll1llll_opy_]].update(platform[bstack11ll1llll_opy_])
        del platform[bstack11ll1llll_opy_]
  config = bstack1l1l_opy_(config)
  return config
def bstack1l1l11l1l_opy_(config):
  global bstack11lllll11_opy_
  if bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧભ") in config and str(config[bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨમ")]).lower() != bstack1l1ll111_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫય"):
    if not bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪર") in config:
      config[bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ઱")] = {}
    if not bstack1l1ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪલ") in config[bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ળ")]:
      bstack11ll1111_opy_ = datetime.datetime.now()
      bstack1lll1ll1l_opy_ = bstack11ll1111_opy_.strftime(bstack1l1ll111_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧ઴"))
      hostname = socket.gethostname()
      bstack1ll1ll11_opy_ = bstack1l1ll111_opy_ (u"ࠫࠬવ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1l1ll111_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧશ").format(bstack1lll1ll1l_opy_, hostname, bstack1ll1ll11_opy_)
      config[bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪષ")][bstack1l1ll111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩસ")] = identifier
    bstack11lllll11_opy_ = config[bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬહ")][bstack1l1ll111_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ઺")]
  return config
def bstack11lll1ll_opy_():
  if (
    isinstance(os.getenv(bstack1l1ll111_opy_ (u"ࠪࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠨ઻")), str) and len(os.getenv(bstack1l1ll111_opy_ (u"ࠫࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍ઼ࠩ"))) > 0
  ) or (
    isinstance(os.getenv(bstack1l1ll111_opy_ (u"ࠬࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠫઽ")), str) and len(os.getenv(bstack1l1ll111_opy_ (u"࠭ࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠬા"))) > 0
  ):
    return os.getenv(bstack1l1ll111_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗ࠭િ"), 0)
  if str(os.getenv(bstack1l1ll111_opy_ (u"ࠨࡅࡌࠫી"))).lower() == bstack1l1ll111_opy_ (u"ࠩࡷࡶࡺ࡫ࠧુ") and str(os.getenv(bstack1l1ll111_opy_ (u"ࠪࡇࡎࡘࡃࡍࡇࡆࡍࠬૂ"))).lower() == bstack1l1ll111_opy_ (u"ࠫࡹࡸࡵࡦࠩૃ"):
    return os.getenv(bstack1l1ll111_opy_ (u"ࠬࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠨૄ"), 0)
  if str(os.getenv(bstack1l1ll111_opy_ (u"࠭ࡃࡊࠩૅ"))).lower() == bstack1l1ll111_opy_ (u"ࠧࡵࡴࡸࡩࠬ૆") and str(os.getenv(bstack1l1ll111_opy_ (u"ࠨࡖࡕࡅ࡛ࡏࡓࠨે"))).lower() == bstack1l1ll111_opy_ (u"ࠩࡷࡶࡺ࡫ࠧૈ"):
    return os.getenv(bstack1l1ll111_opy_ (u"ࠪࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠩૉ"), 0)
  if str(os.getenv(bstack1l1ll111_opy_ (u"ࠫࡈࡏࠧ૊"))).lower() == bstack1l1ll111_opy_ (u"ࠬࡺࡲࡶࡧࠪો") and str(os.getenv(bstack1l1ll111_opy_ (u"࠭ࡃࡊࡡࡑࡅࡒࡋࠧૌ"))).lower() == bstack1l1ll111_opy_ (u"ࠧࡤࡱࡧࡩࡸ࡮ࡩࡱ્ࠩ"):
    return 0 # bstack11111111_opy_ bstack1l111ll1_opy_ not set build number env
  if os.getenv(bstack1l1ll111_opy_ (u"ࠨࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠫ૎")) and os.getenv(bstack1l1ll111_opy_ (u"ࠩࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠬ૏")):
    return os.getenv(bstack1l1ll111_opy_ (u"ࠪࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠬૐ"), 0)
  if str(os.getenv(bstack1l1ll111_opy_ (u"ࠫࡈࡏࠧ૑"))).lower() == bstack1l1ll111_opy_ (u"ࠬࡺࡲࡶࡧࠪ૒") and str(os.getenv(bstack1l1ll111_opy_ (u"࠭ࡄࡓࡑࡑࡉࠬ૓"))).lower() == bstack1l1ll111_opy_ (u"ࠧࡵࡴࡸࡩࠬ૔"):
    return os.getenv(bstack1l1ll111_opy_ (u"ࠨࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗ࠭૕"), 0)
  if str(os.getenv(bstack1l1ll111_opy_ (u"ࠩࡆࡍࠬ૖"))).lower() == bstack1l1ll111_opy_ (u"ࠪࡸࡷࡻࡥࠨ૗") and str(os.getenv(bstack1l1ll111_opy_ (u"ࠫࡘࡋࡍࡂࡒࡋࡓࡗࡋࠧ૘"))).lower() == bstack1l1ll111_opy_ (u"ࠬࡺࡲࡶࡧࠪ૙"):
    return os.getenv(bstack1l1ll111_opy_ (u"࠭ࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠩ૚"), 0)
  if str(os.getenv(bstack1l1ll111_opy_ (u"ࠧࡄࡋࠪ૛"))).lower() == bstack1l1ll111_opy_ (u"ࠨࡶࡵࡹࡪ࠭૜") and str(os.getenv(bstack1l1ll111_opy_ (u"ࠩࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠬ૝"))).lower() == bstack1l1ll111_opy_ (u"ࠪࡸࡷࡻࡥࠨ૞"):
    return os.getenv(bstack1l1ll111_opy_ (u"ࠫࡈࡏ࡟ࡋࡑࡅࡣࡎࡊࠧ૟"), 0)
  if str(os.getenv(bstack1l1ll111_opy_ (u"ࠬࡉࡉࠨૠ"))).lower() == bstack1l1ll111_opy_ (u"࠭ࡴࡳࡷࡨࠫૡ") and str(os.getenv(bstack1l1ll111_opy_ (u"ࠧࡃࡗࡌࡐࡉࡑࡉࡕࡇࠪૢ"))).lower() == bstack1l1ll111_opy_ (u"ࠨࡶࡵࡹࡪ࠭ૣ"):
    return os.getenv(bstack1l1ll111_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫ૤"), 0)
  if str(os.getenv(bstack1l1ll111_opy_ (u"ࠪࡘࡋࡥࡂࡖࡋࡏࡈࠬ૥"))).lower() == bstack1l1ll111_opy_ (u"ࠫࡹࡸࡵࡦࠩ૦"):
    return os.getenv(bstack1l1ll111_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠬ૧"), 0)
  return -1
def bstack1l11l1l1l_opy_(bstack1llllll1_opy_):
  global CONFIG
  if not bstack1l1ll111_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨ૨") in CONFIG[bstack1l1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૩")]:
    return
  CONFIG[bstack1l1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૪")] = CONFIG[bstack1l1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૫")].replace(
    bstack1l1ll111_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬ૬"),
    str(bstack1llllll1_opy_)
  )
def bstack11l11l1_opy_():
  global CONFIG
  if not bstack1l1ll111_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪ૭") in CONFIG[bstack1l1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૮")]:
    return
  bstack11ll1111_opy_ = datetime.datetime.now()
  bstack1lll1ll1l_opy_ = bstack11ll1111_opy_.strftime(bstack1l1ll111_opy_ (u"࠭ࠥࡥ࠯ࠨࡦ࠲ࠫࡈ࠻ࠧࡐࠫ૯"))
  CONFIG[bstack1l1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૰")] = CONFIG[bstack1l1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૱")].replace(
    bstack1l1ll111_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨ૲"),
    bstack1lll1ll1l_opy_
  )
def bstack1111llll_opy_():
  global CONFIG
  if bstack1l1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૳") in CONFIG and not bool(CONFIG[bstack1l1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૴")]):
    del CONFIG[bstack1l1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૵")]
    return
  if not bstack1l1ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૶") in CONFIG:
    CONFIG[bstack1l1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૷")] = bstack1l1ll111_opy_ (u"ࠨࠥࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫ૸")
  if bstack1l1ll111_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨૹ") in CONFIG[bstack1l1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬૺ")]:
    bstack11l11l1_opy_()
    os.environ[bstack1l1ll111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨૻ")] = CONFIG[bstack1l1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧૼ")]
  if not bstack1l1ll111_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨ૽") in CONFIG[bstack1l1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૾")]:
    return
  bstack1llllll1_opy_ = bstack1l1ll111_opy_ (u"ࠨࠩ૿")
  bstack11l11ll_opy_ = bstack11lll1ll_opy_()
  if bstack11l11ll_opy_ != -1:
    bstack1llllll1_opy_ = bstack1l1ll111_opy_ (u"ࠩࡆࡍࠥ࠭଀") + str(bstack11l11ll_opy_)
  if bstack1llllll1_opy_ == bstack1l1ll111_opy_ (u"ࠪࠫଁ"):
    bstack1lll1_opy_ = bstack11111l1_opy_(CONFIG[bstack1l1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧଂ")])
    if bstack1lll1_opy_ != -1:
      bstack1llllll1_opy_ = str(bstack1lll1_opy_)
  if bstack1llllll1_opy_:
    bstack1l11l1l1l_opy_(bstack1llllll1_opy_)
    os.environ[bstack1l1ll111_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩଃ")] = CONFIG[bstack1l1ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ଄")]
def bstack11l1ll1_opy_(bstack11l1lllll_opy_, bstack11lll111_opy_, path):
  bstack1ll1ll_opy_ = {
    bstack1l1ll111_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫଅ"): bstack11lll111_opy_
  }
  if os.path.exists(path):
    bstack11l11llll_opy_ = json.load(open(path, bstack1l1ll111_opy_ (u"ࠨࡴࡥࠫଆ")))
  else:
    bstack11l11llll_opy_ = {}
  bstack11l11llll_opy_[bstack11l1lllll_opy_] = bstack1ll1ll_opy_
  with open(path, bstack1l1ll111_opy_ (u"ࠤࡺ࠯ࠧଇ")) as outfile:
    json.dump(bstack11l11llll_opy_, outfile)
def bstack11111l1_opy_(bstack11l1lllll_opy_):
  bstack11l1lllll_opy_ = str(bstack11l1lllll_opy_)
  bstack1ll11l1l1_opy_ = os.path.join(os.path.expanduser(bstack1l1ll111_opy_ (u"ࠪࢂࠬଈ")), bstack1l1ll111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫଉ"))
  try:
    if not os.path.exists(bstack1ll11l1l1_opy_):
      os.makedirs(bstack1ll11l1l1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l1ll111_opy_ (u"ࠬࢄࠧଊ")), bstack1l1ll111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ଋ"), bstack1l1ll111_opy_ (u"ࠧ࠯ࡤࡸ࡭ࡱࡪ࠭࡯ࡣࡰࡩ࠲ࡩࡡࡤࡪࡨ࠲࡯ࡹ࡯࡯ࠩଌ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l1ll111_opy_ (u"ࠨࡹࠪ଍")):
        pass
      with open(file_path, bstack1l1ll111_opy_ (u"ࠤࡺ࠯ࠧ଎")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l1ll111_opy_ (u"ࠪࡶࠬଏ")) as bstack1l11l1l11_opy_:
      bstack111l1ll11_opy_ = json.load(bstack1l11l1l11_opy_)
    if bstack11l1lllll_opy_ in bstack111l1ll11_opy_:
      bstack11l11lll_opy_ = bstack111l1ll11_opy_[bstack11l1lllll_opy_][bstack1l1ll111_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨଐ")]
      bstack11l1lll11_opy_ = int(bstack11l11lll_opy_) + 1
      bstack11l1ll1_opy_(bstack11l1lllll_opy_, bstack11l1lll11_opy_, file_path)
      return bstack11l1lll11_opy_
    else:
      bstack11l1ll1_opy_(bstack11l1lllll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack111l1l1ll_opy_.format(str(e)))
    return -1
def bstack1111l1ll_opy_(config):
  if not config[bstack1l1ll111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ଑")] or not config[bstack1l1ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ଒")]:
    return True
  else:
    return False
def bstack11l1l1lll_opy_(config):
  if bstack1l1ll111_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ଓ") in config:
    del(config[bstack1l1ll111_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧଔ")])
    return False
  if bstack1l1l1l11_opy_() < version.parse(bstack1l1ll111_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨକ")):
    return False
  if bstack1l1l1l11_opy_() >= version.parse(bstack1l1ll111_opy_ (u"ࠪ࠸࠳࠷࠮࠶ࠩଖ")):
    return True
  if bstack1l1ll111_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫଗ") in config and config[bstack1l1ll111_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬଘ")] == False:
    return False
  else:
    return True
def bstack1l1111l1_opy_(config, index = 0):
  global bstack1l111l11l_opy_
  bstack1l1lll1ll_opy_ = {}
  caps = bstack11l1llll1_opy_ + bstack11ll1l1_opy_
  if bstack1l111l11l_opy_:
    caps += bstack11l11111_opy_
  for key in config:
    if key in caps + [bstack1l1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଙ")]:
      continue
    bstack1l1lll1ll_opy_[key] = config[key]
  if bstack1l1ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଚ") in config:
    for bstack1ll11111l_opy_ in config[bstack1l1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଛ")][index]:
      if bstack1ll11111l_opy_ in caps + [bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧଜ"), bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫଝ")]:
        continue
      bstack1l1lll1ll_opy_[bstack1ll11111l_opy_] = config[bstack1l1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଞ")][index][bstack1ll11111l_opy_]
  bstack1l1lll1ll_opy_[bstack1l1ll111_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧଟ")] = socket.gethostname()
  if bstack1l1ll111_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧଠ") in bstack1l1lll1ll_opy_:
    del(bstack1l1lll1ll_opy_[bstack1l1ll111_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨଡ")])
  return bstack1l1lll1ll_opy_
def bstack1lllll111_opy_(config):
  global bstack1l111l11l_opy_
  bstack111ll11l_opy_ = {}
  caps = bstack11ll1l1_opy_
  if bstack1l111l11l_opy_:
    caps+= bstack11l11111_opy_
  for key in caps:
    if key in config:
      bstack111ll11l_opy_[key] = config[key]
  return bstack111ll11l_opy_
def bstack1ll111ll1_opy_(bstack1l1lll1ll_opy_, bstack111ll11l_opy_):
  bstack1l11lll11_opy_ = {}
  for key in bstack1l1lll1ll_opy_.keys():
    if key in bstack1l1111l1l_opy_:
      bstack1l11lll11_opy_[bstack1l1111l1l_opy_[key]] = bstack1l1lll1ll_opy_[key]
    else:
      bstack1l11lll11_opy_[key] = bstack1l1lll1ll_opy_[key]
  for key in bstack111ll11l_opy_:
    if key in bstack1l1111l1l_opy_:
      bstack1l11lll11_opy_[bstack1l1111l1l_opy_[key]] = bstack111ll11l_opy_[key]
    else:
      bstack1l11lll11_opy_[key] = bstack111ll11l_opy_[key]
  return bstack1l11lll11_opy_
def bstack11llll11l_opy_(config, index = 0):
  global bstack1l111l11l_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack111ll11l_opy_ = bstack1lllll111_opy_(config)
  bstack1lll1l1ll_opy_ = bstack11ll1l1_opy_
  bstack1lll1l1ll_opy_ += bstack111ll1l_opy_
  if bstack1l111l11l_opy_:
    bstack1lll1l1ll_opy_ += bstack11l11111_opy_
  if bstack1l1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଢ") in config:
    if bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧଣ") in config[bstack1l1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ତ")][index]:
      caps[bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଥ")] = config[bstack1l1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଦ")][index][bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫଧ")]
    if bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨନ") in config[bstack1l1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ଩")][index]:
      caps[bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪପ")] = str(config[bstack1l1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଫ")][index][bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬବ")])
    bstack1l11l111l_opy_ = {}
    for bstack111111_opy_ in bstack1lll1l1ll_opy_:
      if bstack111111_opy_ in config[bstack1l1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଭ")][index]:
        if bstack111111_opy_ == bstack1l1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨମ"):
          bstack1l11l111l_opy_[bstack111111_opy_] = str(config[bstack1l1ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଯ")][index][bstack111111_opy_] * 1.0)
        else:
          bstack1l11l111l_opy_[bstack111111_opy_] = config[bstack1l1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫର")][index][bstack111111_opy_]
        del(config[bstack1l1ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ଱")][index][bstack111111_opy_])
    bstack111ll11l_opy_ = update(bstack111ll11l_opy_, bstack1l11l111l_opy_)
  bstack1l1lll1ll_opy_ = bstack1l1111l1_opy_(config, index)
  for bstack111l1111_opy_ in bstack11ll1l1_opy_ + [bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଲ"), bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬଳ")]:
    if bstack111l1111_opy_ in bstack1l1lll1ll_opy_:
      bstack111ll11l_opy_[bstack111l1111_opy_] = bstack1l1lll1ll_opy_[bstack111l1111_opy_]
      del(bstack1l1lll1ll_opy_[bstack111l1111_opy_])
  if bstack11l1l1lll_opy_(config):
    bstack1l1lll1ll_opy_[bstack1l1ll111_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ଴")] = True
    caps.update(bstack111ll11l_opy_)
    caps[bstack1l1ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧଵ")] = bstack1l1lll1ll_opy_
  else:
    bstack1l1lll1ll_opy_[bstack1l1ll111_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧଶ")] = False
    caps.update(bstack1ll111ll1_opy_(bstack1l1lll1ll_opy_, bstack111ll11l_opy_))
    if bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ଷ") in caps:
      caps[bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪସ")] = caps[bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨହ")]
      del(caps[bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ଺")])
    if bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭଻") in caps:
      caps[bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ଼")] = caps[bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨଽ")]
      del(caps[bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩା")])
  return caps
def bstack11l111l1l_opy_():
  global bstack11lll111l_opy_
  if bstack1l1l1l11_opy_() <= version.parse(bstack1l1ll111_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩି")):
    if bstack11lll111l_opy_ != bstack1l1ll111_opy_ (u"ࠪࠫୀ"):
      return bstack1l1ll111_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧୁ") + bstack11lll111l_opy_ + bstack1l1ll111_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤୂ")
    return bstack1ll1_opy_
  if  bstack11lll111l_opy_ != bstack1l1ll111_opy_ (u"࠭ࠧୃ"):
    return bstack1l1ll111_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤୄ") + bstack11lll111l_opy_ + bstack1l1ll111_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤ୅")
  return bstack1ll11l111_opy_
def bstack111llll1l_opy_(options):
  return hasattr(options, bstack1l1ll111_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪ୆"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l1ll11ll_opy_(options, bstack11l111lll_opy_):
  for bstack11llllll_opy_ in bstack11l111lll_opy_:
    if bstack11llllll_opy_ in [bstack1l1ll111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨେ"), bstack1l1ll111_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨୈ")]:
      next
    if bstack11llllll_opy_ in options._experimental_options:
      options._experimental_options[bstack11llllll_opy_]= update(options._experimental_options[bstack11llllll_opy_], bstack11l111lll_opy_[bstack11llllll_opy_])
    else:
      options.add_experimental_option(bstack11llllll_opy_, bstack11l111lll_opy_[bstack11llllll_opy_])
  if bstack1l1ll111_opy_ (u"ࠬࡧࡲࡨࡵࠪ୉") in bstack11l111lll_opy_:
    for arg in bstack11l111lll_opy_[bstack1l1ll111_opy_ (u"࠭ࡡࡳࡩࡶࠫ୊")]:
      options.add_argument(arg)
    del(bstack11l111lll_opy_[bstack1l1ll111_opy_ (u"ࠧࡢࡴࡪࡷࠬୋ")])
  if bstack1l1ll111_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬୌ") in bstack11l111lll_opy_:
    for ext in bstack11l111lll_opy_[bstack1l1ll111_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ୍࠭")]:
      options.add_extension(ext)
    del(bstack11l111lll_opy_[bstack1l1ll111_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ୎")])
def bstack1ll1ll1ll_opy_(options, bstack1l11111_opy_):
  if bstack1l1ll111_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ୏") in bstack1l11111_opy_:
    for bstack1ll1l1l1_opy_ in bstack1l11111_opy_[bstack1l1ll111_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ୐")]:
      if bstack1ll1l1l1_opy_ in options._preferences:
        options._preferences[bstack1ll1l1l1_opy_] = update(options._preferences[bstack1ll1l1l1_opy_], bstack1l11111_opy_[bstack1l1ll111_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ୑")][bstack1ll1l1l1_opy_])
      else:
        options.set_preference(bstack1ll1l1l1_opy_, bstack1l11111_opy_[bstack1l1ll111_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭୒")][bstack1ll1l1l1_opy_])
  if bstack1l1ll111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୓") in bstack1l11111_opy_:
    for arg in bstack1l11111_opy_[bstack1l1ll111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ୔")]:
      options.add_argument(arg)
def bstack111l11lll_opy_(options, bstack1ll11l11l_opy_):
  if bstack1l1ll111_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫ୕") in bstack1ll11l11l_opy_:
    options.use_webview(bool(bstack1ll11l11l_opy_[bstack1l1ll111_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬୖ")]))
  bstack1l1ll11ll_opy_(options, bstack1ll11l11l_opy_)
def bstack1llllll11_opy_(options, bstack1lll1llll_opy_):
  for bstack11l1l111l_opy_ in bstack1lll1llll_opy_:
    if bstack11l1l111l_opy_ in [bstack1l1ll111_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩୗ"), bstack1l1ll111_opy_ (u"࠭ࡡࡳࡩࡶࠫ୘")]:
      next
    options.set_capability(bstack11l1l111l_opy_, bstack1lll1llll_opy_[bstack11l1l111l_opy_])
  if bstack1l1ll111_opy_ (u"ࠧࡢࡴࡪࡷࠬ୙") in bstack1lll1llll_opy_:
    for arg in bstack1lll1llll_opy_[bstack1l1ll111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୚")]:
      options.add_argument(arg)
  if bstack1l1ll111_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭୛") in bstack1lll1llll_opy_:
    options.use_technology_preview(bool(bstack1lll1llll_opy_[bstack1l1ll111_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧଡ଼")]))
def bstack11llll111_opy_(options, bstack111l111l_opy_):
  for bstack11111ll_opy_ in bstack111l111l_opy_:
    if bstack11111ll_opy_ in [bstack1l1ll111_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨଢ଼"), bstack1l1ll111_opy_ (u"ࠬࡧࡲࡨࡵࠪ୞")]:
      next
    options._options[bstack11111ll_opy_] = bstack111l111l_opy_[bstack11111ll_opy_]
  if bstack1l1ll111_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪୟ") in bstack111l111l_opy_:
    for bstack1l11l11ll_opy_ in bstack111l111l_opy_[bstack1l1ll111_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫୠ")]:
      options.bstack11lll1l_opy_(
          bstack1l11l11ll_opy_, bstack111l111l_opy_[bstack1l1ll111_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬୡ")][bstack1l11l11ll_opy_])
  if bstack1l1ll111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧୢ") in bstack111l111l_opy_:
    for arg in bstack111l111l_opy_[bstack1l1ll111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨୣ")]:
      options.add_argument(arg)
def bstack1111lll_opy_(options, caps):
  if not hasattr(options, bstack1l1ll111_opy_ (u"ࠫࡐࡋ࡙ࠨ୤")):
    return
  if options.KEY == bstack1l1ll111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ୥") and options.KEY in caps:
    bstack1l1ll11ll_opy_(options, caps[bstack1l1ll111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ୦")])
  elif options.KEY == bstack1l1ll111_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬ୧") and options.KEY in caps:
    bstack1ll1ll1ll_opy_(options, caps[bstack1l1ll111_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭୨")])
  elif options.KEY == bstack1l1ll111_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ୩") and options.KEY in caps:
    bstack1llllll11_opy_(options, caps[bstack1l1ll111_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫ୪")])
  elif options.KEY == bstack1l1ll111_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬ୫") and options.KEY in caps:
    bstack111l11lll_opy_(options, caps[bstack1l1ll111_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭୬")])
  elif options.KEY == bstack1l1ll111_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬ୭") and options.KEY in caps:
    bstack11llll111_opy_(options, caps[bstack1l1ll111_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭୮")])
def bstack1l1111l11_opy_(caps):
  global bstack1l111l11l_opy_
  if bstack1l111l11l_opy_:
    if bstack1ll1ll11l_opy_() < version.parse(bstack1l1ll111_opy_ (u"ࠨ࠴࠱࠷࠳࠶ࠧ୯")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1l1ll111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ୰")
    if bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨୱ") in caps:
      browser = caps[bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ୲")]
    elif bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭୳") in caps:
      browser = caps[bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ୴")]
    browser = str(browser).lower()
    if browser == bstack1l1ll111_opy_ (u"ࠧࡪࡲ࡫ࡳࡳ࡫ࠧ୵") or browser == bstack1l1ll111_opy_ (u"ࠨ࡫ࡳࡥࡩ࠭୶"):
      browser = bstack1l1ll111_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩ୷")
    if browser == bstack1l1ll111_opy_ (u"ࠪࡷࡦࡳࡳࡶࡰࡪࠫ୸"):
      browser = bstack1l1ll111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ୹")
    if browser not in [bstack1l1ll111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ୺"), bstack1l1ll111_opy_ (u"࠭ࡥࡥࡩࡨࠫ୻"), bstack1l1ll111_opy_ (u"ࠧࡪࡧࠪ୼"), bstack1l1ll111_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ୽"), bstack1l1ll111_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ୾")]:
      return None
    try:
      package = bstack1l1ll111_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡽࢀ࠲ࡴࡶࡴࡪࡱࡱࡷࠬ୿").format(browser)
      name = bstack1l1ll111_opy_ (u"ࠫࡔࡶࡴࡪࡱࡱࡷࠬ஀")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack111llll1l_opy_(options):
        return None
      for bstack111l1111_opy_ in caps.keys():
        options.set_capability(bstack111l1111_opy_, caps[bstack111l1111_opy_])
      bstack1111lll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1lll11l11_opy_(options, bstack1ll11l_opy_):
  if not bstack111llll1l_opy_(options):
    return
  for bstack111l1111_opy_ in bstack1ll11l_opy_.keys():
    if bstack111l1111_opy_ in bstack111ll1l_opy_:
      next
    if bstack111l1111_opy_ in options._caps and type(options._caps[bstack111l1111_opy_]) in [dict, list]:
      options._caps[bstack111l1111_opy_] = update(options._caps[bstack111l1111_opy_], bstack1ll11l_opy_[bstack111l1111_opy_])
    else:
      options.set_capability(bstack111l1111_opy_, bstack1ll11l_opy_[bstack111l1111_opy_])
  bstack1111lll_opy_(options, bstack1ll11l_opy_)
  if bstack1l1ll111_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡧࡩࡧࡻࡧࡨࡧࡵࡅࡩࡪࡲࡦࡵࡶࠫ஁") in options._caps:
    if options._caps[bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫஂ")] and options._caps[bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬஃ")].lower() != bstack1l1ll111_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩ஄"):
      del options._caps[bstack1l1ll111_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨஅ")]
def bstack1l1l1111_opy_(proxy_config):
  if bstack1l1ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧஆ") in proxy_config:
    proxy_config[bstack1l1ll111_opy_ (u"ࠫࡸࡹ࡬ࡑࡴࡲࡼࡾ࠭இ")] = proxy_config[bstack1l1ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩஈ")]
    del(proxy_config[bstack1l1ll111_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪஉ")])
  if bstack1l1ll111_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪஊ") in proxy_config and proxy_config[bstack1l1ll111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ஋")].lower() != bstack1l1ll111_opy_ (u"ࠩࡧ࡭ࡷ࡫ࡣࡵࠩ஌"):
    proxy_config[bstack1l1ll111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭஍")] = bstack1l1ll111_opy_ (u"ࠫࡲࡧ࡮ࡶࡣ࡯ࠫஎ")
  if bstack1l1ll111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡅࡺࡺ࡯ࡤࡱࡱࡪ࡮࡭ࡕࡳ࡮ࠪஏ") in proxy_config:
    proxy_config[bstack1l1ll111_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩஐ")] = bstack1l1ll111_opy_ (u"ࠧࡱࡣࡦࠫ஑")
  return proxy_config
def bstack11ll1ll1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l1ll111_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧஒ") in config:
    return proxy
  config[bstack1l1ll111_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨஓ")] = bstack1l1l1111_opy_(config[bstack1l1ll111_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩஔ")])
  if proxy == None:
    proxy = Proxy(config[bstack1l1ll111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪக")])
  return proxy
def bstack1l1l1l1l1_opy_(self):
  global CONFIG
  global bstack1l1lll1l_opy_
  try:
    proxy = bstack11llllll1_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1l1ll111_opy_ (u"ࠬ࠴ࡰࡢࡥࠪ஖")):
        proxies = bstack1llll1l11_opy_(proxy, bstack11l111l1l_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1_opy_ = proxies.popitem()
          if bstack1l1ll111_opy_ (u"ࠨ࠺࠰࠱ࠥ஗") in bstack1l1_opy_:
            return bstack1l1_opy_
          else:
            return bstack1l1ll111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ஘") + bstack1l1_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1l1ll111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡵࡸ࡯ࡹࡻࠣࡹࡷࡲࠠ࠻ࠢࡾࢁࠧங").format(str(e)))
  return bstack1l1lll1l_opy_(self)
def bstack111l1ll_opy_():
  global CONFIG
  return bstack1l1ll111_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬச") in CONFIG or bstack1l1ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ஛") in CONFIG
def bstack11llllll1_opy_(config):
  if not bstack111l1ll_opy_():
    return
  if config.get(bstack1l1ll111_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧஜ")):
    return config.get(bstack1l1ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ஝"))
  if config.get(bstack1l1ll111_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪஞ")):
    return config.get(bstack1l1ll111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫட"))
def bstack111lll1l_opy_(url):
  try:
      result = urlparse(url)
      return all([result.scheme, result.netloc])
  except:
      return False
def bstack111lll111_opy_(bstack1l1llll1l_opy_, bstack111ll1ll1_opy_):
  from pypac import get_pac
  from pypac import PACSession
  from pypac.parser import PACFile
  import socket
  if os.path.isfile(bstack1l1llll1l_opy_):
    with open(bstack1l1llll1l_opy_) as f:
      pac = PACFile(f.read())
  elif bstack111lll1l_opy_(bstack1l1llll1l_opy_):
    pac = get_pac(url=bstack1l1llll1l_opy_)
  else:
    raise Exception(bstack1l1ll111_opy_ (u"ࠨࡒࡤࡧࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠨ஠").format(bstack1l1llll1l_opy_))
  session = PACSession(pac)
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((bstack1l1ll111_opy_ (u"ࠤ࠻࠲࠽࠴࠸࠯࠺ࠥ஡"), 80))
    bstack1l11ll11l_opy_ = s.getsockname()[0]
    s.close()
  except:
    bstack1l11ll11l_opy_ = bstack1l1ll111_opy_ (u"ࠪ࠴࠳࠶࠮࠱࠰࠳ࠫ஢")
  proxy_url = session.get_pac().find_proxy_for_url(bstack111ll1ll1_opy_, bstack1l11ll11l_opy_)
  return proxy_url
def bstack1llll1l11_opy_(bstack1l1llll1l_opy_, bstack111ll1ll1_opy_):
  proxies = {}
  global bstack1ll1l111l_opy_
  if bstack1l1ll111_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧண") in globals():
    return bstack1ll1l111l_opy_
  try:
    proxy = bstack111lll111_opy_(bstack1l1llll1l_opy_,bstack111ll1ll1_opy_)
    if bstack1l1ll111_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧத") in proxy:
      proxies = {}
    elif bstack1l1ll111_opy_ (u"ࠨࡈࡕࡖࡓࠦ஥") in proxy or bstack1l1ll111_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨ஦") in proxy or bstack1l1ll111_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢ஧") in proxy:
      bstack1lll1l1l1_opy_ = proxy.split(bstack1l1ll111_opy_ (u"ࠤࠣࠦந"))
      if bstack1l1ll111_opy_ (u"ࠥ࠾࠴࠵ࠢன") in bstack1l1ll111_opy_ (u"ࠦࠧப").join(bstack1lll1l1l1_opy_[1:]):
        proxies = {
          bstack1l1ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ஫"): bstack1l1ll111_opy_ (u"ࠨࠢ஬").join(bstack1lll1l1l1_opy_[1:])
        }
      else:
        proxies = {
          bstack1l1ll111_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭஭") : str(bstack1lll1l1l1_opy_[0]).lower()+ bstack1l1ll111_opy_ (u"ࠣ࠼࠲࠳ࠧம") + bstack1l1ll111_opy_ (u"ࠤࠥய").join(bstack1lll1l1l1_opy_[1:])
        }
    elif bstack1l1ll111_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤர") in proxy:
      bstack1lll1l1l1_opy_ = proxy.split(bstack1l1ll111_opy_ (u"ࠦࠥࠨற"))
      if bstack1l1ll111_opy_ (u"ࠧࡀ࠯࠰ࠤல") in bstack1l1ll111_opy_ (u"ࠨࠢள").join(bstack1lll1l1l1_opy_[1:]):
        proxies = {
          bstack1l1ll111_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ழ"): bstack1l1ll111_opy_ (u"ࠣࠤவ").join(bstack1lll1l1l1_opy_[1:])
        }
      else:
        proxies = {
          bstack1l1ll111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨஶ"): bstack1l1ll111_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦஷ") + bstack1l1ll111_opy_ (u"ࠦࠧஸ").join(bstack1lll1l1l1_opy_[1:])
        }
    else:
      proxies = {
        bstack1l1ll111_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫஹ"): proxy
      }
  except Exception as e:
    logger.error(bstack1ll11llll_opy_.format(bstack1l1llll1l_opy_, str(e)))
  bstack1ll1l111l_opy_ = proxies
  return proxies
def bstack1lll1111l_opy_(config, bstack111ll1ll1_opy_):
  proxy = bstack11llllll1_opy_(config)
  proxies = {}
  if config.get(bstack1l1ll111_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ஺")) or config.get(bstack1l1ll111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ஻")):
    if proxy.endswith(bstack1l1ll111_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭஼")):
      proxies = bstack1llll1l11_opy_(proxy,bstack111ll1ll1_opy_)
    else:
      proxies = {
        bstack1l1ll111_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ஽"): proxy
      }
  return proxies
def bstack1l111ll_opy_():
  return bstack111l1ll_opy_() and bstack1l1l1l11_opy_() >= version.parse(bstack1l1ll1ll_opy_)
def bstack1l11ll_opy_(config):
  bstack111ll11ll_opy_ = {}
  if bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧா") in config:
    bstack111ll11ll_opy_ =  config[bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨி")]
  if bstack1l1ll111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫீ") in config:
    bstack111ll11ll_opy_ = config[bstack1l1ll111_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬு")]
  proxy = bstack11llllll1_opy_(config)
  if proxy:
    if proxy.endswith(bstack1l1ll111_opy_ (u"ࠧ࠯ࡲࡤࡧࠬூ")) and os.path.isfile(proxy):
      bstack111ll11ll_opy_[bstack1l1ll111_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫ௃")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1l1ll111_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ௄")):
        proxies = bstack1lll1111l_opy_(config, bstack11l111l1l_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1_opy_ = proxies.popitem()
          if bstack1l1ll111_opy_ (u"ࠥ࠾࠴࠵ࠢ௅") in bstack1l1_opy_:
            parsed_url = urlparse(bstack1l1_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1l1ll111_opy_ (u"ࠦ࠿࠵࠯ࠣெ") + bstack1l1_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack111ll11ll_opy_[bstack1l1ll111_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨே")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack111ll11ll_opy_[bstack1l1ll111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩை")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack111ll11ll_opy_[bstack1l1ll111_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ௉")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack111ll11ll_opy_[bstack1l1ll111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫொ")] = str(parsed_url.password)
  return bstack111ll11ll_opy_
def bstack11ll11ll1_opy_(config):
  if bstack1l1ll111_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧோ") in config:
    return config[bstack1l1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨௌ")]
  return {}
def bstack1lll1ll1_opy_(caps):
  global bstack11lllll11_opy_
  if bstack1l1ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷ்ࠬ") in caps:
    caps[bstack1l1ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭௎")][bstack1l1ll111_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ௏")] = True
    if bstack11lllll11_opy_:
      caps[bstack1l1ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨௐ")][bstack1l1ll111_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ௑")] = bstack11lllll11_opy_
  else:
    caps[bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧ௒")] = True
    if bstack11lllll11_opy_:
      caps[bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ௓")] = bstack11lllll11_opy_
def bstack1llll111l_opy_():
  global CONFIG
  if bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ௔") in CONFIG and CONFIG[bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ௕")]:
    bstack111ll11ll_opy_ = bstack1l11ll_opy_(CONFIG)
    bstack11ll1l1l_opy_(CONFIG[bstack1l1ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ௖")], bstack111ll11ll_opy_)
def bstack11ll1l1l_opy_(key, bstack111ll11ll_opy_):
  global bstack111lll1_opy_
  logger.info(bstack1l1l1ll11_opy_)
  try:
    bstack111lll1_opy_ = Local()
    bstack111ll1ll_opy_ = {bstack1l1ll111_opy_ (u"ࠧ࡬ࡧࡼࠫௗ"): key}
    bstack111ll1ll_opy_.update(bstack111ll11ll_opy_)
    logger.debug(bstack11ll11l1l_opy_.format(str(bstack111ll1ll_opy_)))
    bstack111lll1_opy_.start(**bstack111ll1ll_opy_)
    if bstack111lll1_opy_.isRunning():
      logger.info(bstack11ll1lll_opy_)
  except Exception as e:
    bstack11lll1l11_opy_(bstack1l111l1_opy_.format(str(e)))
def bstack1ll111l1l_opy_():
  global bstack111lll1_opy_
  if bstack111lll1_opy_.isRunning():
    logger.info(bstack11l111l1_opy_)
    bstack111lll1_opy_.stop()
  bstack111lll1_opy_ = None
def bstack1l_opy_(bstack11ll1l11l_opy_=[]):
  global CONFIG
  bstack11l_opy_ = []
  bstack11l1ll11l_opy_ = [bstack1l1ll111_opy_ (u"ࠨࡱࡶࠫ௘"), bstack1l1ll111_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ௙"), bstack1l1ll111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ௚"), bstack1l1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭௛"), bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ௜"), bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ௝")]
  try:
    for err in bstack11ll1l11l_opy_:
      bstack1lllll1ll_opy_ = {}
      for k in bstack11l1ll11l_opy_:
        val = CONFIG[bstack1l1ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ௞")][int(err[bstack1l1ll111_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ௟")])].get(k)
        if val:
          bstack1lllll1ll_opy_[k] = val
      bstack1lllll1ll_opy_[bstack1l1ll111_opy_ (u"ࠩࡷࡩࡸࡺࡳࠨ௠")] = {
        err[bstack1l1ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨ௡")]: err[bstack1l1ll111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ௢")]
      }
      bstack11l_opy_.append(bstack1lllll1ll_opy_)
  except Exception as e:
    logger.debug(bstack1l1ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧࡱࡵࡱࡦࡺࡴࡪࡰࡪࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸ࠿ࠦࠧ௣") +str(e))
  finally:
    return bstack11l_opy_
def bstack11lllll1_opy_():
  global bstack11l1l1l1_opy_
  global bstack1lll1ll11_opy_
  global bstack1l1lll111_opy_
  if bstack11l1l1l1_opy_:
    logger.warning(bstack1ll1l111_opy_.format(str(bstack11l1l1l1_opy_)))
  logger.info(bstack11ll111l1_opy_)
  global bstack111lll1_opy_
  if bstack111lll1_opy_:
    bstack1ll111l1l_opy_()
  try:
    for driver in bstack1lll1ll11_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11ll11l1_opy_)
  bstack11lll1ll1_opy_()
  if len(bstack1l1lll111_opy_) > 0:
    message = bstack1l_opy_(bstack1l1lll111_opy_)
    bstack11lll1ll1_opy_(message)
  else:
    bstack11lll1ll1_opy_()
def bstack11l1ll1ll_opy_(self, *args):
  logger.error(bstack1llll_opy_)
  bstack11lllll1_opy_()
  sys.exit(1)
def bstack11lll1l11_opy_(err):
  logger.critical(bstack1l1l1l1ll_opy_.format(str(err)))
  bstack11lll1ll1_opy_(bstack1l1l1l1ll_opy_.format(str(err)))
  atexit.unregister(bstack11lllll1_opy_)
  sys.exit(1)
def bstack1111lll1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11lll1ll1_opy_(message)
  atexit.unregister(bstack11lllll1_opy_)
  sys.exit(1)
def bstack111ll_opy_():
  global CONFIG
  global bstack1l11l1l_opy_
  global bstack1llll1111_opy_
  global bstack1l11l1ll_opy_
  CONFIG = bstack111lll_opy_()
  bstack1ll11lll1_opy_()
  bstack1l1ll1l_opy_()
  CONFIG = bstack1111_opy_(CONFIG)
  update(CONFIG, bstack1llll1111_opy_)
  update(CONFIG, bstack1l11l1l_opy_)
  CONFIG = bstack1l1l11l1l_opy_(CONFIG)
  if bstack1l1ll111_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ௤") in CONFIG and str(CONFIG[bstack1l1ll111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ௥")]).lower() == bstack1l1ll111_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ௦"):
    bstack1l11l1ll_opy_ = False
  if (bstack1l1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ௧") in CONFIG and bstack1l1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭௨") in bstack1l11l1l_opy_) or (bstack1l1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ௩") in CONFIG and bstack1l1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ௪") not in bstack1llll1111_opy_):
    if os.getenv(bstack1l1ll111_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ௫")):
      CONFIG[bstack1l1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ௬")] = os.getenv(bstack1l1ll111_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬ௭"))
    else:
      bstack1111llll_opy_()
  elif (bstack1l1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ௮") not in CONFIG and bstack1l1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ௯") in CONFIG) or (bstack1l1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ௰") in bstack1llll1111_opy_ and bstack1l1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ௱") not in bstack1l11l1l_opy_):
    del(CONFIG[bstack1l1ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ௲")])
  if bstack1111l1ll_opy_(CONFIG):
    bstack11lll1l11_opy_(bstack1l111l1l1_opy_)
  bstack11l1lll1_opy_()
  bstack11lllll1l_opy_()
  if bstack1l111l11l_opy_:
    CONFIG[bstack1l1ll111_opy_ (u"ࠧࡢࡲࡳࠫ௳")] = bstack11l11l_opy_(CONFIG)
    logger.info(bstack111llll1_opy_.format(CONFIG[bstack1l1ll111_opy_ (u"ࠨࡣࡳࡴࠬ௴")]))
def bstack11lllll1l_opy_():
  global CONFIG
  global bstack1l111l11l_opy_
  if bstack1l1ll111_opy_ (u"ࠩࡤࡴࡵ࠭௵") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1111lll1_opy_(e, bstack111l11l1_opy_)
    bstack1l111l11l_opy_ = True
def bstack11l11l_opy_(config):
  bstack11ll1l1l1_opy_ = bstack1l1ll111_opy_ (u"ࠪࠫ௶")
  app = config[bstack1l1ll111_opy_ (u"ࠫࡦࡶࡰࠨ௷")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1lllll_opy_:
      if os.path.exists(app):
        bstack11ll1l1l1_opy_ = bstack1111111_opy_(config, app)
      elif bstack1llll1lll_opy_(app):
        bstack11ll1l1l1_opy_ = app
      else:
        bstack11lll1l11_opy_(bstack1l1llllll_opy_.format(app))
    else:
      if bstack1llll1lll_opy_(app):
        bstack11ll1l1l1_opy_ = app
      elif os.path.exists(app):
        bstack11ll1l1l1_opy_ = bstack1111111_opy_(app)
      else:
        bstack11lll1l11_opy_(bstack111111l1_opy_)
  else:
    if len(app) > 2:
      bstack11lll1l11_opy_(bstack1lllll1l1_opy_)
    elif len(app) == 2:
      if bstack1l1ll111_opy_ (u"ࠬࡶࡡࡵࡪࠪ௸") in app and bstack1l1ll111_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ௹") in app:
        if os.path.exists(app[bstack1l1ll111_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ௺")]):
          bstack11ll1l1l1_opy_ = bstack1111111_opy_(config, app[bstack1l1ll111_opy_ (u"ࠨࡲࡤࡸ࡭࠭௻")], app[bstack1l1ll111_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ௼")])
        else:
          bstack11lll1l11_opy_(bstack1l1llllll_opy_.format(app))
      else:
        bstack11lll1l11_opy_(bstack1lllll1l1_opy_)
    else:
      for key in app:
        if key in bstack1l1l1l111_opy_:
          if key == bstack1l1ll111_opy_ (u"ࠪࡴࡦࡺࡨࠨ௽"):
            if os.path.exists(app[key]):
              bstack11ll1l1l1_opy_ = bstack1111111_opy_(config, app[key])
            else:
              bstack11lll1l11_opy_(bstack1l1llllll_opy_.format(app))
          else:
            bstack11ll1l1l1_opy_ = app[key]
        else:
          bstack11lll1l11_opy_(bstack111ll11l1_opy_)
  return bstack11ll1l1l1_opy_
def bstack1llll1lll_opy_(bstack11ll1l1l1_opy_):
  import re
  bstack1ll1ll111_opy_ = re.compile(bstack1l1ll111_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ௾"))
  bstack1l11l11_opy_ = re.compile(bstack1l1ll111_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭࠳ࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ௿"))
  if bstack1l1ll111_opy_ (u"࠭ࡢࡴ࠼࠲࠳ࠬఀ") in bstack11ll1l1l1_opy_ or re.fullmatch(bstack1ll1ll111_opy_, bstack11ll1l1l1_opy_) or re.fullmatch(bstack1l11l11_opy_, bstack11ll1l1l1_opy_):
    return True
  else:
    return False
def bstack1111111_opy_(config, path, bstack111l1l1l1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l1ll111_opy_ (u"ࠧࡳࡤࠪఁ")).read()).hexdigest()
  bstack111l1l1l_opy_ = bstack1llll1l1_opy_(md5_hash)
  bstack11ll1l1l1_opy_ = None
  if bstack111l1l1l_opy_:
    logger.info(bstack11l1ll111_opy_.format(bstack111l1l1l_opy_, md5_hash))
    return bstack111l1l1l_opy_
  bstack1ll1lllll_opy_ = MultipartEncoder(
    fields={
        bstack1l1ll111_opy_ (u"ࠨࡨ࡬ࡰࡪ࠭ం"): (os.path.basename(path), open(os.path.abspath(path), bstack1l1ll111_opy_ (u"ࠩࡵࡦࠬః")), bstack1l1ll111_opy_ (u"ࠪࡸࡪࡾࡴ࠰ࡲ࡯ࡥ࡮ࡴࠧఄ")),
        bstack1l1ll111_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧఅ"): bstack111l1l1l1_opy_
    }
  )
  response = requests.post(bstack1l1ll11_opy_, data=bstack1ll1lllll_opy_,
                         headers={bstack1l1ll111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫఆ"): bstack1ll1lllll_opy_.content_type}, auth=(config[bstack1l1ll111_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨఇ")], config[bstack1l1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪఈ")]))
  try:
    res = json.loads(response.text)
    bstack11ll1l1l1_opy_ = res[bstack1l1ll111_opy_ (u"ࠨࡣࡳࡴࡤࡻࡲ࡭ࠩఉ")]
    logger.info(bstack1ll1llll1_opy_.format(bstack11ll1l1l1_opy_))
    bstack1lll111ll_opy_(md5_hash, bstack11ll1l1l1_opy_)
  except ValueError as err:
    bstack11lll1l11_opy_(bstack11lll1_opy_.format(str(err)))
  return bstack11ll1l1l1_opy_
def bstack11l1lll1_opy_():
  global CONFIG
  global bstack1llll11_opy_
  bstack1l1l1111l_opy_ = 0
  bstack11ll1lll1_opy_ = 1
  if bstack1l1ll111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩఊ") in CONFIG:
    bstack11ll1lll1_opy_ = CONFIG[bstack1l1ll111_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪఋ")]
  if bstack1l1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧఌ") in CONFIG:
    bstack1l1l1111l_opy_ = len(CONFIG[bstack1l1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ఍")])
  bstack1llll11_opy_ = int(bstack11ll1lll1_opy_) * int(bstack1l1l1111l_opy_)
def bstack1llll1l1_opy_(md5_hash):
  bstack111ll11_opy_ = os.path.join(os.path.expanduser(bstack1l1ll111_opy_ (u"࠭ࡾࠨఎ")), bstack1l1ll111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧఏ"), bstack1l1ll111_opy_ (u"ࠨࡣࡳࡴ࡚ࡶ࡬ࡰࡣࡧࡑࡉ࠻ࡈࡢࡵ࡫࠲࡯ࡹ࡯࡯ࠩఐ"))
  if os.path.exists(bstack111ll11_opy_):
    bstack1l1l111_opy_ = json.load(open(bstack111ll11_opy_,bstack1l1ll111_opy_ (u"ࠩࡵࡦࠬ఑")))
    if md5_hash in bstack1l1l111_opy_:
      bstack111lll1l1_opy_ = bstack1l1l111_opy_[md5_hash]
      bstack1111llll1_opy_ = datetime.datetime.now()
      bstack1ll11l1l_opy_ = datetime.datetime.strptime(bstack111lll1l1_opy_[bstack1l1ll111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ఒ")], bstack1l1ll111_opy_ (u"ࠫࠪࡪ࠯ࠦ࡯࠲ࠩ࡞ࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓࠨఓ"))
      if (bstack1111llll1_opy_ - bstack1ll11l1l_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack111lll1l1_opy_[bstack1l1ll111_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪఔ")]):
        return None
      return bstack111lll1l1_opy_[bstack1l1ll111_opy_ (u"࠭ࡩࡥࠩక")]
  else:
    return None
def bstack1lll111ll_opy_(md5_hash, bstack11ll1l1l1_opy_):
  bstack1ll11l1l1_opy_ = os.path.join(os.path.expanduser(bstack1l1ll111_opy_ (u"ࠧࡿࠩఖ")), bstack1l1ll111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨగ"))
  if not os.path.exists(bstack1ll11l1l1_opy_):
    os.makedirs(bstack1ll11l1l1_opy_)
  bstack111ll11_opy_ = os.path.join(os.path.expanduser(bstack1l1ll111_opy_ (u"ࠩࢁࠫఘ")), bstack1l1ll111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪఙ"), bstack1l1ll111_opy_ (u"ࠫࡦࡶࡰࡖࡲ࡯ࡳࡦࡪࡍࡅ࠷ࡋࡥࡸ࡮࠮࡫ࡵࡲࡲࠬచ"))
  bstack1lll1l1l_opy_ = {
    bstack1l1ll111_opy_ (u"ࠬ࡯ࡤࠨఛ"): bstack11ll1l1l1_opy_,
    bstack1l1ll111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩజ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l1ll111_opy_ (u"ࠧࠦࡦ࠲ࠩࡲ࠵࡚ࠥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫఝ")),
    bstack1l1ll111_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ఞ"): str(__version__)
  }
  if os.path.exists(bstack111ll11_opy_):
    bstack1l1l111_opy_ = json.load(open(bstack111ll11_opy_,bstack1l1ll111_opy_ (u"ࠩࡵࡦࠬట")))
  else:
    bstack1l1l111_opy_ = {}
  bstack1l1l111_opy_[md5_hash] = bstack1lll1l1l_opy_
  with open(bstack111ll11_opy_, bstack1l1ll111_opy_ (u"ࠥࡻ࠰ࠨఠ")) as outfile:
    json.dump(bstack1l1l111_opy_, outfile)
def bstack1l11l1l1_opy_(self):
  return
def bstack111ll111_opy_(self):
  return
def bstack1l1lllll1_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1l1l1l11l_opy_(self):
  global bstack1l1l1_opy_
  global bstack1l11ll1l1_opy_
  global bstack1111lll1l_opy_
  try:
    if bstack1l1ll111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫడ") in bstack1l1l1_opy_ and self.session_id != None:
      bstack1lll1111_opy_ = bstack1l1ll111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬఢ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ణ")
      bstack1l1l1ll1l_opy_ = bstack11l1l1l1l_opy_(bstack1l1ll111_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪత"), bstack1l1ll111_opy_ (u"ࠨࠩథ"), bstack1lll1111_opy_, bstack1l1ll111_opy_ (u"ࠩ࠯ࠤࠬద").join(threading.current_thread().bstackTestErrorMessages), bstack1l1ll111_opy_ (u"ࠪࠫధ"), bstack1l1ll111_opy_ (u"ࠫࠬన"))
      if self != None:
        self.execute_script(bstack1l1l1ll1l_opy_)
  except Exception as e:
    logger.debug(bstack1l1ll111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨ఩") + str(e))
  bstack1111lll1l_opy_(self)
  self.session_id = None
def bstack1ll11ll1_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l11ll1l1_opy_
  global bstack11l111ll_opy_
  global bstack1ll111l_opy_
  global bstack1ll_opy_
  global bstack11l1l1l_opy_
  global bstack1l1l1_opy_
  global bstack1lll111_opy_
  global bstack1lll1ll11_opy_
  global bstack11l1l_opy_
  CONFIG[bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨప")] = str(bstack1l1l1_opy_) + str(__version__)
  command_executor = bstack11l111l1l_opy_()
  logger.debug(bstack1lllll1l_opy_.format(command_executor))
  proxy = bstack11ll1ll1_opy_(CONFIG, proxy)
  bstack1lll11lll_opy_ = 0 if bstack11l111ll_opy_ < 0 else bstack11l111ll_opy_
  try:
    if bstack1ll_opy_ is True:
      bstack1lll11lll_opy_ = int(multiprocessing.current_process().name)
    elif bstack11l1l1l_opy_ is True:
      bstack1lll11lll_opy_ = int(threading.current_thread().name)
  except:
    bstack1lll11lll_opy_ = 0
  bstack1ll11l_opy_ = bstack11llll11l_opy_(CONFIG, bstack1lll11lll_opy_)
  logger.debug(bstack11l111l_opy_.format(str(bstack1ll11l_opy_)))
  if bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫఫ") in CONFIG and CONFIG[bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬబ")]:
    bstack1lll1ll1_opy_(bstack1ll11l_opy_)
  if desired_capabilities:
    bstack111l11111_opy_ = bstack1111_opy_(desired_capabilities)
    bstack111l11111_opy_[bstack1l1ll111_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩభ")] = bstack11l1l1lll_opy_(CONFIG)
    bstack11l1llll_opy_ = bstack11llll11l_opy_(bstack111l11111_opy_)
    if bstack11l1llll_opy_:
      bstack1ll11l_opy_ = update(bstack11l1llll_opy_, bstack1ll11l_opy_)
    desired_capabilities = None
  if options:
    bstack1lll11l11_opy_(options, bstack1ll11l_opy_)
  if not options:
    options = bstack1l1111l11_opy_(bstack1ll11l_opy_)
  if proxy and bstack1l1l1l11_opy_() >= version.parse(bstack1l1ll111_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪమ")):
    options.proxy(proxy)
  if options and bstack1l1l1l11_opy_() >= version.parse(bstack1l1ll111_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪయ")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack1l1l1l11_opy_() < version.parse(bstack1l1ll111_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫర")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1ll11l_opy_)
  logger.info(bstack11_opy_)
  if bstack1l1l1l11_opy_() >= version.parse(bstack1l1ll111_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ఱ")):
    bstack1lll111_opy_(self, command_executor=command_executor,
          options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1l1l11_opy_() >= version.parse(bstack1l1ll111_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ల")):
    bstack1lll111_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1l1l11_opy_() >= version.parse(bstack1l1ll111_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨళ")):
    bstack1lll111_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1lll111_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  try:
    bstack1l1ll_opy_ = bstack1l1ll111_opy_ (u"ࠩࠪఴ")
    if bstack1l1l1l11_opy_() >= version.parse(bstack1l1ll111_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫవ")):
      bstack1l1ll_opy_ = self.caps.get(bstack1l1ll111_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦశ"))
    else:
      bstack1l1ll_opy_ = self.capabilities.get(bstack1l1ll111_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧష"))
    if bstack1l1ll_opy_:
      if bstack1l1l1l11_opy_() <= version.parse(bstack1l1ll111_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭స")):
        self.command_executor._url = bstack1l1ll111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣహ") + bstack11lll111l_opy_ + bstack1l1ll111_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧ఺")
      else:
        self.command_executor._url = bstack1l1ll111_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ఻") + bstack1l1ll_opy_ + bstack1l1ll111_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥ఼ࠦ")
      logger.debug(bstack111l111ll_opy_.format(bstack1l1ll_opy_))
    else:
      logger.debug(bstack11llll1l1_opy_.format(bstack1l1ll111_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧఽ")))
  except Exception as e:
    logger.debug(bstack11llll1l1_opy_.format(e))
  if bstack1l1ll111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫా") in bstack1l1l1_opy_:
    bstack1lllllll_opy_(bstack11l111ll_opy_, bstack11l1l_opy_)
  bstack1l11ll1l1_opy_ = self.session_id
  if bstack1l1ll111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ి") in bstack1l1l1_opy_:
    threading.current_thread().bstack111l111l1_opy_ = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1lll1ll11_opy_.append(self)
  if bstack1l1ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪీ") in CONFIG and bstack1l1ll111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ు") in CONFIG[bstack1l1ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬూ")][bstack1lll11lll_opy_]:
    bstack1ll111l_opy_ = CONFIG[bstack1l1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ృ")][bstack1lll11lll_opy_][bstack1l1ll111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩౄ")]
  logger.debug(bstack1l11llll_opy_.format(bstack1l11ll1l1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack11l11ll1_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1llll1l1l_opy_
      if(bstack1l1ll111_opy_ (u"ࠧ࡯࡮ࡥࡧࡻ࠲࡯ࡹࠢ౅") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1l1ll111_opy_ (u"࠭ࡾࠨె")), bstack1l1ll111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧే"), bstack1l1ll111_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪై")), bstack1l1ll111_opy_ (u"ࠩࡺࠫ౉")) as fp:
          fp.write(bstack1l1ll111_opy_ (u"ࠥࠦొ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1l1ll111_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨో")))):
          with open(args[1], bstack1l1ll111_opy_ (u"ࠬࡸࠧౌ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1l1ll111_opy_ (u"࠭ࡡࡴࡻࡱࡧࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡠࡰࡨࡻࡕࡧࡧࡦࠪࡦࡳࡳࡺࡥࡹࡶ࠯ࠤࡵࡧࡧࡦࠢࡀࠤࡻࡵࡩࡥࠢ࠳్࠭ࠬ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1ll1l1l_opy_)
            lines.insert(1, bstack1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1l1ll111_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ౎")), bstack1l1ll111_opy_ (u"ࠨࡹࠪ౏")) as bstack1l11ll1l_opy_:
              bstack1l11ll1l_opy_.writelines(lines)
        CONFIG[bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ౐")] = str(bstack1l1l1_opy_) + str(__version__)
        bstack1lll11lll_opy_ = 0 if bstack11l111ll_opy_ < 0 else bstack11l111ll_opy_
        if bstack1ll_opy_ is True:
          bstack1lll11lll_opy_ = int(threading.current_thread().getName())
        CONFIG[bstack1l1ll111_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥ౑")] = False
        CONFIG[bstack1l1ll111_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ౒")] = True
        bstack1ll11l_opy_ = bstack11llll11l_opy_(CONFIG, bstack1lll11lll_opy_)
        logger.debug(bstack11l111l_opy_.format(str(bstack1ll11l_opy_)))
        if CONFIG[bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ౓")]:
          bstack1lll1ll1_opy_(bstack1ll11l_opy_)
        if bstack1l1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ౔") in CONFIG and bstack1l1ll111_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩౕࠬ") in CONFIG[bstack1l1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶౖࠫ")][bstack1lll11lll_opy_]:
          bstack1ll111l_opy_ = CONFIG[bstack1l1ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౗")][bstack1lll11lll_opy_][bstack1l1ll111_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨౘ")]
        args.append(os.path.join(os.path.expanduser(bstack1l1ll111_opy_ (u"ࠫࢃ࠭ౙ")), bstack1l1ll111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬౚ"), bstack1l1ll111_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ౛")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll11l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1l1ll111_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ౜"))
      bstack1llll1l1l_opy_ = True
      return bstack1l11l1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1lll1l_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1l11ll1l1_opy_
    global bstack11l111ll_opy_
    global bstack1ll111l_opy_
    global bstack1ll_opy_
    global bstack1l1l1_opy_
    global bstack1lll111_opy_
    CONFIG[bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪౝ")] = str(bstack1l1l1_opy_) + str(__version__)
    bstack1lll11lll_opy_ = 0 if bstack11l111ll_opy_ < 0 else bstack11l111ll_opy_
    if bstack1ll_opy_ is True:
      bstack1lll11lll_opy_ = int(threading.current_thread().getName())
    CONFIG[bstack1l1ll111_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ౞")] = True
    bstack1ll11l_opy_ = bstack11llll11l_opy_(CONFIG, bstack1lll11lll_opy_)
    logger.debug(bstack11l111l_opy_.format(str(bstack1ll11l_opy_)))
    if CONFIG[bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ౟")]:
      bstack1lll1ll1_opy_(bstack1ll11l_opy_)
    if bstack1l1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧౠ") in CONFIG and bstack1l1ll111_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪౡ") in CONFIG[bstack1l1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩౢ")][bstack1lll11lll_opy_]:
      bstack1ll111l_opy_ = CONFIG[bstack1l1ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪౣ")][bstack1lll11lll_opy_][bstack1l1ll111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭౤")]
    import urllib
    import json
    bstack1ll11lll_opy_ = bstack1l1ll111_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ౥") + urllib.parse.quote(json.dumps(bstack1ll11l_opy_))
    browser = self.connect(bstack1ll11lll_opy_)
    return browser
except Exception as e:
    pass
def bstack111l11ll1_opy_():
    global bstack1llll1l1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1lll1l_opy_
        bstack1llll1l1l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11l11ll1_opy_
      bstack1llll1l1l_opy_ = True
    except Exception as e:
      pass
def bstack1ll1lll11_opy_(context, bstack11lll1l1l_opy_):
  try:
    context.page.evaluate(bstack1l1ll111_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ౦"), bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨ౧")+ json.dumps(bstack11lll1l1l_opy_) + bstack1l1ll111_opy_ (u"ࠧࢃࡽࠣ౨"))
  except Exception as e:
    logger.debug(bstack1l1ll111_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦ౩"), e)
def bstack1lll1ll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1l1ll111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ౪"), bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭౫") + json.dumps(message) + bstack1l1ll111_opy_ (u"ࠩ࠯ࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠬ౬") + json.dumps(level) + bstack1l1ll111_opy_ (u"ࠪࢁࢂ࠭౭"))
  except Exception as e:
    logger.debug(bstack1l1ll111_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࢀࢃࠢ౮"), e)
def bstack1l111l_opy_(context, status, message = bstack1l1ll111_opy_ (u"ࠧࠨ౯")):
  try:
    if(status == bstack1l1ll111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ౰")):
      context.page.evaluate(bstack1l1ll111_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ౱"), bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡳࡧࡤࡷࡴࡴࠢ࠻ࠩ౲") + json.dumps(bstack1l1ll111_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࠦ౳") + str(message)) + bstack1l1ll111_opy_ (u"ࠪ࠰ࠧࡹࡴࡢࡶࡸࡷࠧࡀࠧ౴") + json.dumps(status) + bstack1l1ll111_opy_ (u"ࠦࢂࢃࠢ౵"))
    else:
      context.page.evaluate(bstack1l1ll111_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ౶"), bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠧ౷") + json.dumps(status) + bstack1l1ll111_opy_ (u"ࠢࡾࡿࠥ౸"))
  except Exception as e:
    logger.debug(bstack1l1ll111_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡾࢁࠧ౹"), e)
def bstack1l1lll11_opy_(self, url):
  global bstack1l111111l_opy_
  try:
    bstack1l11l1111_opy_(url)
  except Exception as err:
    logger.debug(bstack1l11lllll_opy_.format(str(err)))
  try:
    bstack1l111111l_opy_(self, url)
  except Exception as e:
    try:
      bstack1ll1l1ll_opy_ = str(e)
      if any(err_msg in bstack1ll1l1ll_opy_ for err_msg in bstack111lllll_opy_):
        bstack1l11l1111_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l11lllll_opy_.format(str(err)))
    raise e
def bstack1111111l_opy_(self):
  global bstack1lll1lll1_opy_
  bstack1lll1lll1_opy_ = self
  return
def bstack1111ll11_opy_(self):
  global bstack11ll1l111_opy_
  bstack11ll1l111_opy_ = self
  return
def bstack11111l_opy_(self, test):
  global CONFIG
  global bstack11ll1l111_opy_
  global bstack1lll1lll1_opy_
  global bstack1l11ll1l1_opy_
  global bstack1l1llll_opy_
  global bstack1ll111l_opy_
  global bstack1l111llll_opy_
  global bstack1111l111_opy_
  global bstack1lll11ll_opy_
  global bstack1lll1ll11_opy_
  try:
    if not bstack1l11ll1l1_opy_:
      with open(os.path.join(os.path.expanduser(bstack1l1ll111_opy_ (u"ࠩࢁࠫ౺")), bstack1l1ll111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ౻"), bstack1l1ll111_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭౼"))) as f:
        bstack1ll11ll11_opy_ = json.loads(bstack1l1ll111_opy_ (u"ࠧࢁࠢ౽") + f.read().strip() + bstack1l1ll111_opy_ (u"࠭ࠢࡹࠤ࠽ࠤࠧࡿࠢࠨ౾") + bstack1l1ll111_opy_ (u"ࠢࡾࠤ౿"))
        bstack1l11ll1l1_opy_ = bstack1ll11ll11_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1lll1ll11_opy_:
    for driver in bstack1lll1ll11_opy_:
      if bstack1l11ll1l1_opy_ == driver.session_id:
        if test:
          bstack111l1_opy_ = str(test.data)
        if not bstack11111_opy_ and bstack111l1_opy_:
          bstack1l11_opy_ = {
            bstack1l1ll111_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨಀ"): bstack1l1ll111_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪಁ"),
            bstack1l1ll111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ಂ"): {
              bstack1l1ll111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩಃ"): bstack111l1_opy_
            }
          }
          bstack1ll1l11l1_opy_ = bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ಄").format(json.dumps(bstack1l11_opy_))
          driver.execute_script(bstack1ll1l11l1_opy_)
        if bstack1l1llll_opy_:
          bstack1l1llll1_opy_ = {
            bstack1l1ll111_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ಅ"): bstack1l1ll111_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩಆ"),
            bstack1l1ll111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫಇ"): {
              bstack1l1ll111_opy_ (u"ࠩࡧࡥࡹࡧࠧಈ"): bstack111l1_opy_ + bstack1l1ll111_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬಉ"),
              bstack1l1ll111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪಊ"): bstack1l1ll111_opy_ (u"ࠬ࡯࡮ࡧࡱࠪಋ")
            }
          }
          bstack1l11_opy_ = {
            bstack1l1ll111_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ಌ"): bstack1l1ll111_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ಍"),
            bstack1l1ll111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫಎ"): {
              bstack1l1ll111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩಏ"): bstack1l1ll111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪಐ")
            }
          }
          if bstack1l1llll_opy_.status == bstack1l1ll111_opy_ (u"ࠫࡕࡇࡓࡔࠩ಑"):
            bstack1l11ll111_opy_ = bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪಒ").format(json.dumps(bstack1l1llll1_opy_))
            driver.execute_script(bstack1l11ll111_opy_)
            bstack1ll1l11l1_opy_ = bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫಓ").format(json.dumps(bstack1l11_opy_))
            driver.execute_script(bstack1ll1l11l1_opy_)
          elif bstack1l1llll_opy_.status == bstack1l1ll111_opy_ (u"ࠧࡇࡃࡌࡐࠬಔ"):
            reason = bstack1l1ll111_opy_ (u"ࠣࠤಕ")
            bstack11lllll_opy_ = bstack111l1_opy_ + bstack1l1ll111_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠪಖ")
            if bstack1l1llll_opy_.message:
              reason = str(bstack1l1llll_opy_.message)
              bstack11lllll_opy_ = bstack11lllll_opy_ + bstack1l1ll111_opy_ (u"ࠪࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࠪಗ") + reason
            bstack1l1llll1_opy_[bstack1l1ll111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧಘ")] = {
              bstack1l1ll111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫಙ"): bstack1l1ll111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬಚ"),
              bstack1l1ll111_opy_ (u"ࠧࡥࡣࡷࡥࠬಛ"): bstack11lllll_opy_
            }
            bstack1l11_opy_[bstack1l1ll111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫಜ")] = {
              bstack1l1ll111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩಝ"): bstack1l1ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪಞ"),
              bstack1l1ll111_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫಟ"): reason
            }
            bstack1l11ll111_opy_ = bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪಠ").format(json.dumps(bstack1l1llll1_opy_))
            driver.execute_script(bstack1l11ll111_opy_)
            bstack1ll1l11l1_opy_ = bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫಡ").format(json.dumps(bstack1l11_opy_))
            driver.execute_script(bstack1ll1l11l1_opy_)
  elif bstack1l11ll1l1_opy_:
    try:
      data = {}
      bstack111l1_opy_ = None
      if test:
        bstack111l1_opy_ = str(test.data)
      if not bstack11111_opy_ and bstack111l1_opy_:
        data[bstack1l1ll111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಢ")] = bstack111l1_opy_
      if bstack1l1llll_opy_:
        if bstack1l1llll_opy_.status == bstack1l1ll111_opy_ (u"ࠨࡒࡄࡗࡘ࠭ಣ"):
          data[bstack1l1ll111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩತ")] = bstack1l1ll111_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪಥ")
        elif bstack1l1llll_opy_.status == bstack1l1ll111_opy_ (u"ࠫࡋࡇࡉࡍࠩದ"):
          data[bstack1l1ll111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬಧ")] = bstack1l1ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ನ")
          if bstack1l1llll_opy_.message:
            data[bstack1l1ll111_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ಩")] = str(bstack1l1llll_opy_.message)
      user = CONFIG[bstack1l1ll111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪಪ")]
      key = CONFIG[bstack1l1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬಫ")]
      url = bstack1l1ll111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠯ࡼࡿ࠱࡮ࡸࡵ࡮ࠨಬ").format(user, key, bstack1l11ll1l1_opy_)
      headers = {
        bstack1l1ll111_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪಭ"): bstack1l1ll111_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨಮ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack111l1llll_opy_.format(str(e)))
  if bstack11ll1l111_opy_:
    bstack1111l111_opy_(bstack11ll1l111_opy_)
  if bstack1lll1lll1_opy_:
    bstack1lll11ll_opy_(bstack1lll1lll1_opy_)
  bstack1l111llll_opy_(self, test)
def bstack111l11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1lll11l1l_opy_
  bstack1lll11l1l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l1llll_opy_
  bstack1l1llll_opy_ = self._test
def bstack11ll11l11_opy_():
  global bstack1lll111l_opy_
  try:
    if os.path.exists(bstack1lll111l_opy_):
      os.remove(bstack1lll111l_opy_)
  except Exception as e:
    logger.debug(bstack1l1ll111_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠢࡩ࡭ࡱ࡫࠺ࠡࠩಯ") + str(e))
def bstack1l111lll1_opy_():
  global bstack1lll111l_opy_
  bstack11l11llll_opy_ = {}
  try:
    if not os.path.isfile(bstack1lll111l_opy_):
      with open(bstack1lll111l_opy_, bstack1l1ll111_opy_ (u"ࠧࡸࠩರ")):
        pass
      with open(bstack1lll111l_opy_, bstack1l1ll111_opy_ (u"ࠣࡹ࠮ࠦಱ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1lll111l_opy_):
      bstack11l11llll_opy_ = json.load(open(bstack1lll111l_opy_, bstack1l1ll111_opy_ (u"ࠩࡵࡦࠬಲ")))
  except Exception as e:
    logger.debug(bstack1l1ll111_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡸࡥࡢࡦ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬಳ") + str(e))
  finally:
    return bstack11l11llll_opy_
def bstack1lllllll_opy_(platform_index, item_index):
  global bstack1lll111l_opy_
  try:
    bstack11l11llll_opy_ = bstack1l111lll1_opy_()
    bstack11l11llll_opy_[item_index] = platform_index
    with open(bstack1lll111l_opy_, bstack1l1ll111_opy_ (u"ࠦࡼ࠱ࠢ಴")) as outfile:
      json.dump(bstack11l11llll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1l1ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡸࡴ࡬ࡸ࡮ࡴࡧࠡࡶࡲࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪವ") + str(e))
def bstack1l1ll1l1l_opy_(bstack1l1111111_opy_):
  global CONFIG
  bstack1l1lll11l_opy_ = bstack1l1ll111_opy_ (u"࠭ࠧಶ")
  if not bstack1l1ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪಷ") in CONFIG:
    logger.info(bstack1l1ll111_opy_ (u"ࠨࡐࡲࠤࡵࡲࡡࡵࡨࡲࡶࡲࡹࠠࡱࡣࡶࡷࡪࡪࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡸࡥࡱࡱࡵࡸࠥ࡬࡯ࡳࠢࡕࡳࡧࡵࡴࠡࡴࡸࡲࠬಸ"))
  try:
    platform = CONFIG[bstack1l1ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬಹ")][bstack1l1111111_opy_]
    if bstack1l1ll111_opy_ (u"ࠪࡳࡸ࠭಺") in platform:
      bstack1l1lll11l_opy_ += str(platform[bstack1l1ll111_opy_ (u"ࠫࡴࡹࠧ಻")]) + bstack1l1ll111_opy_ (u"ࠬ࠲ࠠࠨ಼")
    if bstack1l1ll111_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩಽ") in platform:
      bstack1l1lll11l_opy_ += str(platform[bstack1l1ll111_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪಾ")]) + bstack1l1ll111_opy_ (u"ࠨ࠮ࠣࠫಿ")
    if bstack1l1ll111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ೀ") in platform:
      bstack1l1lll11l_opy_ += str(platform[bstack1l1ll111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧು")]) + bstack1l1ll111_opy_ (u"ࠫ࠱ࠦࠧೂ")
    if bstack1l1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧೃ") in platform:
      bstack1l1lll11l_opy_ += str(platform[bstack1l1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨೄ")]) + bstack1l1ll111_opy_ (u"ࠧ࠭ࠢࠪ೅")
    if bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ೆ") in platform:
      bstack1l1lll11l_opy_ += str(platform[bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧೇ")]) + bstack1l1ll111_opy_ (u"ࠪ࠰ࠥ࠭ೈ")
    if bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ೉") in platform:
      bstack1l1lll11l_opy_ += str(platform[bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ೊ")]) + bstack1l1ll111_opy_ (u"࠭ࠬࠡࠩೋ")
  except Exception as e:
    logger.debug(bstack1l1ll111_opy_ (u"ࠧࡔࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡶࡪࡶ࡯ࡳࡶࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡴࡴࠧೌ") + str(e))
  finally:
    if bstack1l1lll11l_opy_[len(bstack1l1lll11l_opy_) - 2:] == bstack1l1ll111_opy_ (u"ࠨ࠮್ࠣࠫ"):
      bstack1l1lll11l_opy_ = bstack1l1lll11l_opy_[:-2]
    return bstack1l1lll11l_opy_
def bstack1ll111l11_opy_(path, bstack1l1lll11l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1lll11l_opy_ = ET.parse(path)
    bstack1l1l111ll_opy_ = bstack1lll11l_opy_.getroot()
    bstack11l111l11_opy_ = None
    for suite in bstack1l1l111ll_opy_.iter(bstack1l1ll111_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ೎")):
      if bstack1l1ll111_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ೏") in suite.attrib:
        suite.attrib[bstack1l1ll111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ೐")] += bstack1l1ll111_opy_ (u"ࠬࠦࠧ೑") + bstack1l1lll11l_opy_
        bstack11l111l11_opy_ = suite
    bstack11ll1111l_opy_ = None
    for robot in bstack1l1l111ll_opy_.iter(bstack1l1ll111_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ೒")):
      bstack11ll1111l_opy_ = robot
    bstack1l111l111_opy_ = len(bstack11ll1111l_opy_.findall(bstack1l1ll111_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭೓")))
    if bstack1l111l111_opy_ == 1:
      bstack11ll1111l_opy_.remove(bstack11ll1111l_opy_.findall(bstack1l1ll111_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ೔"))[0])
      bstack1l1l11ll_opy_ = ET.Element(bstack1l1ll111_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨೕ"), attrib={bstack1l1ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨೖ"):bstack1l1ll111_opy_ (u"ࠫࡘࡻࡩࡵࡧࡶࠫ೗"), bstack1l1ll111_opy_ (u"ࠬ࡯ࡤࠨ೘"):bstack1l1ll111_opy_ (u"࠭ࡳ࠱ࠩ೙")})
      bstack11ll1111l_opy_.insert(1, bstack1l1l11ll_opy_)
      bstack1llll11l_opy_ = None
      for suite in bstack11ll1111l_opy_.iter(bstack1l1ll111_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭೚")):
        bstack1llll11l_opy_ = suite
      bstack1llll11l_opy_.append(bstack11l111l11_opy_)
      bstack111l1lll1_opy_ = None
      for status in bstack11l111l11_opy_.iter(bstack1l1ll111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ೛")):
        bstack111l1lll1_opy_ = status
      bstack1llll11l_opy_.append(bstack111l1lll1_opy_)
    bstack1lll11l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1l1ll111_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡵࡧࡲࡴ࡫ࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠧ೜") + str(e))
def bstack11l1l1ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1lllll1_opy_
  global CONFIG
  if bstack1l1ll111_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࡳࡥࡹ࡮ࠢೝ") in options:
    del options[bstack1l1ll111_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣೞ")]
  bstack1ll1ll_opy_ = bstack1l111lll1_opy_()
  for bstack11l1ll1l1_opy_ in bstack1ll1ll_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1l1ll111_opy_ (u"ࠬࡶࡡࡣࡱࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠬ೟"), str(bstack11l1ll1l1_opy_), bstack1l1ll111_opy_ (u"࠭࡯ࡶࡶࡳࡹࡹ࠴ࡸ࡮࡮ࠪೠ"))
    bstack1ll111l11_opy_(path, bstack1l1ll1l1l_opy_(bstack1ll1ll_opy_[bstack11l1ll1l1_opy_]))
  bstack11ll11l11_opy_()
  return bstack1lllll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11l1l11l_opy_(self, ff_profile_dir):
  global bstack11l1111l1_opy_
  if not ff_profile_dir:
    return None
  return bstack11l1111l1_opy_(self, ff_profile_dir)
def bstack1ll1l1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11lllll11_opy_
  bstack1l1111ll_opy_ = []
  if bstack1l1ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪೡ") in CONFIG:
    bstack1l1111ll_opy_ = CONFIG[bstack1l1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫೢ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l1ll111_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥೣ")],
      pabot_args[bstack1l1ll111_opy_ (u"ࠥࡺࡪࡸࡢࡰࡵࡨࠦ೤")],
      argfile,
      pabot_args.get(bstack1l1ll111_opy_ (u"ࠦ࡭࡯ࡶࡦࠤ೥")),
      pabot_args[bstack1l1ll111_opy_ (u"ࠧࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠣ೦")],
      platform[0],
      bstack11lllll11_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l1ll111_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡧ࡫࡯ࡩࡸࠨ೧")] or [(bstack1l1ll111_opy_ (u"ࠢࠣ೨"), None)]
    for platform in enumerate(bstack1l1111ll_opy_)
  ]
def bstack1l11111ll_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack111l1l_opy_=bstack1l1ll111_opy_ (u"ࠨࠩ೩")):
  global bstack1lll11111_opy_
  self.platform_index = platform_index
  self.bstack111ll111l_opy_ = bstack111l1l_opy_
  bstack1lll11111_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1l1ll11l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack11l11l111_opy_
  global bstack1l1l1llll_opy_
  if not bstack1l1ll111_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ೪") in item.options:
    item.options[bstack1l1ll111_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ೫")] = []
  for v in item.options[bstack1l1ll111_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭೬")]:
    if bstack1l1ll111_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫ೭") in v:
      item.options[bstack1l1ll111_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ೮")].remove(v)
    if bstack1l1ll111_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧ೯") in v:
      item.options[bstack1l1ll111_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ೰")].remove(v)
  item.options[bstack1l1ll111_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫೱ")].insert(0, bstack1l1ll111_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙࠼ࡾࢁࠬೲ").format(item.platform_index))
  item.options[bstack1l1ll111_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ೳ")].insert(0, bstack1l1ll111_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓ࠼ࡾࢁࠬ೴").format(item.bstack111ll111l_opy_))
  if bstack1l1l1llll_opy_:
    item.options[bstack1l1ll111_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ೵")].insert(0, bstack1l1ll111_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙࠺ࡼࡿࠪ೶").format(bstack1l1l1llll_opy_))
  return bstack11l11l111_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1ll1l1l11_opy_(command, item_index):
  global bstack1l1l1llll_opy_
  if bstack1l1l1llll_opy_:
    command[0] = command[0].replace(bstack1l1ll111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ೷"), bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠥ࠭೸") + str(item_index) + bstack1l1ll111_opy_ (u"ࠪࠤࠬ೹") + bstack1l1l1llll_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1l1ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ೺"), bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩ೻") + str(item_index), 1)
def bstack1l11lll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11l1l1ll1_opy_
  bstack1ll1l1l11_opy_(command, item_index)
  return bstack11l1l1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack111l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11l1l1ll1_opy_
  bstack1ll1l1l11_opy_(command, item_index)
  return bstack11l1l1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11l1l1ll1_opy_
  bstack1ll1l1l11_opy_(command, item_index)
  return bstack11l1l1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1ll11111_opy_(self, runner, quiet=False, capture=True):
  global bstack1llll11l1_opy_
  bstack111l11l11_opy_ = bstack1llll11l1_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1l1ll111_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡡࡤࡶࡷ࠭೼")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l1ll111_opy_ (u"ࠧࡦࡺࡦࡣࡹࡸࡡࡤࡧࡥࡥࡨࡱ࡟ࡢࡴࡵࠫ೽")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack111l11l11_opy_
def bstack1llllll_opy_(self, name, context, *args):
  global bstack11l1111ll_opy_
  if name in [bstack1l1ll111_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩ೾"), bstack1l1ll111_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ೿")]:
    bstack11l1111ll_opy_(self, name, context, *args)
  if name == bstack1l1ll111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠫഀ"):
    try:
      if(not bstack11111_opy_):
        bstack11lll1l1l_opy_ = str(self.feature.name)
        bstack1ll1lll11_opy_(context, bstack11lll1l1l_opy_)
        context.browser.execute_script(bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩഁ") + json.dumps(bstack11lll1l1l_opy_) + bstack1l1ll111_opy_ (u"ࠬࢃࡽࠨം"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1l1ll111_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ഃ").format(str(e)))
  if name == bstack1l1ll111_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩഄ"):
    try:
      if not hasattr(self, bstack1l1ll111_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪഅ")):
        self.driver_before_scenario = True
      if(not bstack11111_opy_):
        scenario_name = args[0].name
        feature_name = bstack11lll1l1l_opy_ = str(self.feature.name)
        bstack11lll1l1l_opy_ = feature_name + bstack1l1ll111_opy_ (u"ࠩࠣ࠱ࠥ࠭ആ") + scenario_name
        if self.driver_before_scenario:
          bstack1ll1lll11_opy_(context, bstack11lll1l1l_opy_)
          context.browser.execute_script(bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨഇ") + json.dumps(bstack11lll1l1l_opy_) + bstack1l1ll111_opy_ (u"ࠫࢂࢃࠧഈ"))
    except Exception as e:
      logger.debug(bstack1l1ll111_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ഉ").format(str(e)))
  if name == bstack1l1ll111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧഊ"):
    try:
      bstack1l1lll_opy_ = args[0].status.name
      if str(bstack1l1lll_opy_).lower() == bstack1l1ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧഋ"):
        bstack1ll1ll1l_opy_ = bstack1l1ll111_opy_ (u"ࠨࠩഌ")
        bstack11l1_opy_ = bstack1l1ll111_opy_ (u"ࠩࠪ഍")
        bstack1llll1ll1_opy_ = bstack1l1ll111_opy_ (u"ࠪࠫഎ")
        try:
          import traceback
          bstack1ll1ll1l_opy_ = self.exception.__class__.__name__
          bstack1llllllll_opy_ = traceback.format_tb(self.exc_traceback)
          bstack11l1_opy_ = bstack1l1ll111_opy_ (u"ࠫࠥ࠭ഏ").join(bstack1llllllll_opy_)
          bstack1llll1ll1_opy_ = bstack1llllllll_opy_[-1]
        except Exception as e:
          logger.debug(bstack1ll1l1ll1_opy_.format(str(e)))
        bstack1ll1ll1l_opy_ += bstack1llll1ll1_opy_
        bstack1lll1ll_opy_(context, json.dumps(str(args[0].name) + bstack1l1ll111_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦഐ") + str(bstack11l1_opy_)), bstack1l1ll111_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ഑"))
        if self.driver_before_scenario:
          bstack1l111l_opy_(context, bstack1l1ll111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢഒ"), bstack1ll1ll1l_opy_)
        context.browser.execute_script(bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ഓ") + json.dumps(str(args[0].name) + bstack1l1ll111_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣഔ") + str(bstack11l1_opy_)) + bstack1l1ll111_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪക"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࠲ࠠࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠣࠫഖ") + json.dumps(bstack1l1ll111_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤഗ") + str(bstack1ll1ll1l_opy_)) + bstack1l1ll111_opy_ (u"࠭ࡽࡾࠩഘ"))
      else:
        bstack1lll1ll_opy_(context, bstack1l1ll111_opy_ (u"ࠢࡑࡣࡶࡷࡪࡪࠡࠣങ"), bstack1l1ll111_opy_ (u"ࠣ࡫ࡱࡪࡴࠨച"))
        if self.driver_before_scenario:
          bstack1l111l_opy_(context, bstack1l1ll111_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤഛ"))
        context.browser.execute_script(bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨജ") + json.dumps(str(args[0].name) + bstack1l1ll111_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣഝ")) + bstack1l1ll111_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫഞ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡱࡣࡶࡷࡪࡪࠢࡾࡿࠪട"))
    except Exception as e:
      logger.debug(bstack1l1ll111_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩഠ").format(str(e)))
  if name == bstack1l1ll111_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨഡ"):
    try:
      if context.failed is True:
        bstack11111lll_opy_ = []
        bstack1111ll1_opy_ = []
        bstack1ll1l1l1l_opy_ = []
        bstack111111ll_opy_ = bstack1l1ll111_opy_ (u"ࠩࠪഢ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack11111lll_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1llllllll_opy_ = traceback.format_tb(exc_tb)
            bstack1ll111l1_opy_ = bstack1l1ll111_opy_ (u"ࠪࠤࠬണ").join(bstack1llllllll_opy_)
            bstack1111ll1_opy_.append(bstack1ll111l1_opy_)
            bstack1ll1l1l1l_opy_.append(bstack1llllllll_opy_[-1])
        except Exception as e:
          logger.debug(bstack1ll1l1ll1_opy_.format(str(e)))
        bstack1ll1ll1l_opy_ = bstack1l1ll111_opy_ (u"ࠫࠬത")
        for i in range(len(bstack11111lll_opy_)):
          bstack1ll1ll1l_opy_ += bstack11111lll_opy_[i] + bstack1ll1l1l1l_opy_[i] + bstack1l1ll111_opy_ (u"ࠬࡢ࡮ࠨഥ")
        bstack111111ll_opy_ = bstack1l1ll111_opy_ (u"࠭ࠠࠨദ").join(bstack1111ll1_opy_)
        if not self.driver_before_scenario:
          bstack1lll1ll_opy_(context, bstack111111ll_opy_, bstack1l1ll111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨധ"))
          bstack1l111l_opy_(context, bstack1l1ll111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣന"), bstack1ll1ll1l_opy_)
          context.browser.execute_script(bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧഩ") + json.dumps(bstack111111ll_opy_) + bstack1l1ll111_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪപ"))
          context.browser.execute_script(bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࠲ࠠࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠣࠫഫ") + json.dumps(bstack1l1ll111_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥബ") + str(bstack1ll1ll1l_opy_)) + bstack1l1ll111_opy_ (u"࠭ࡽࡾࠩഭ"))
      else:
        if not self.driver_before_scenario:
          bstack1lll1ll_opy_(context, bstack1l1ll111_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥമ") + str(self.feature.name) + bstack1l1ll111_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥയ"), bstack1l1ll111_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢര"))
          bstack1l111l_opy_(context, bstack1l1ll111_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥറ"))
          context.browser.execute_script(bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩല") + json.dumps(bstack1l1ll111_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣള") + str(self.feature.name) + bstack1l1ll111_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣഴ")) + bstack1l1ll111_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭വ"))
          context.browser.execute_script(bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡳࡥࡸࡹࡥࡥࠤࢀࢁࠬശ"))
    except Exception as e:
      logger.debug(bstack1l1ll111_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫഷ").format(str(e)))
  if name in [bstack1l1ll111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪസ"), bstack1l1ll111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬഹ")]:
    bstack11l1111ll_opy_(self, name, context, *args)
    if (name == bstack1l1ll111_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ഺ") and self.driver_before_scenario) or (name == bstack1l1ll111_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ഻࠭") and not self.driver_before_scenario):
      try:
        context.browser.quit()
      except Exception:
        pass
def bstack11ll1ll1l_opy_(config, startdir):
  return bstack1l1ll111_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁ഼ࠧ").format(bstack1l1ll111_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢഽ"))
class Notset:
  def __repr__(self):
    return bstack1l1ll111_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦാ")
notset = Notset()
def bstack1ll1l1lll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l1ll1lll_opy_
  if str(name).lower() == bstack1l1ll111_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪി"):
    return bstack1l1ll111_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥീ")
  else:
    return bstack1l1ll1lll_opy_(self, name, default, skip)
def bstack1ll1llll_opy_(item, when):
  global bstack1l11l111_opy_
  try:
    bstack1l11l111_opy_(item, when)
  except Exception as e:
    pass
def bstack111l11l_opy_():
  return
def bstack11l1l1l1l_opy_(type, name, status, reason, bstack1l1111_opy_, bstack1l1l1lll_opy_):
  bstack1l11_opy_ = {
    bstack1l1ll111_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬു"): type,
    bstack1l1ll111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩൂ"): {}
  }
  if type == bstack1l1ll111_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩൃ"):
    bstack1l11_opy_[bstack1l1ll111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫൄ")][bstack1l1ll111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ൅")] = bstack1l1111_opy_
    bstack1l11_opy_[bstack1l1ll111_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭െ")][bstack1l1ll111_opy_ (u"ࠫࡩࡧࡴࡢࠩേ")] = json.dumps(str(bstack1l1l1lll_opy_))
  if type == bstack1l1ll111_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ൈ"):
    bstack1l11_opy_[bstack1l1ll111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ൉")][bstack1l1ll111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬൊ")] = name
  if type == bstack1l1ll111_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫോ"):
    bstack1l11_opy_[bstack1l1ll111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬൌ")][bstack1l1ll111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵ്ࠪ")] = status
    if status == bstack1l1ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫൎ"):
      bstack1l11_opy_[bstack1l1ll111_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ൏")][bstack1l1ll111_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭൐")] = json.dumps(str(reason))
  bstack1ll1l11l1_opy_ = bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ൑").format(json.dumps(bstack1l11_opy_))
  return bstack1ll1l11l1_opy_
def bstack1l11lll_opy_(item, call, rep):
  global bstack111lllll1_opy_
  global bstack1lll1ll11_opy_
  name = bstack1l1ll111_opy_ (u"ࠨࠩ൒")
  try:
    if rep.when == bstack1l1ll111_opy_ (u"ࠩࡦࡥࡱࡲࠧ൓"):
      bstack1l11ll1l1_opy_ = threading.current_thread().bstack111l111l1_opy_
      try:
        name = str(rep.nodeid)
        bstack1l1l1ll1l_opy_ = bstack11l1l1l1l_opy_(bstack1l1ll111_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫൔ"), name, bstack1l1ll111_opy_ (u"ࠫࠬൕ"), bstack1l1ll111_opy_ (u"ࠬ࠭ൖ"), bstack1l1ll111_opy_ (u"࠭ࠧൗ"), bstack1l1ll111_opy_ (u"ࠧࠨ൘"))
        for driver in bstack1lll1ll11_opy_:
          if bstack1l11ll1l1_opy_ == driver.session_id:
            driver.execute_script(bstack1l1l1ll1l_opy_)
      except Exception as e:
        logger.debug(bstack1l1ll111_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ൙").format(str(e)))
      try:
        status = bstack1l1ll111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ൚") if rep.outcome.lower() == bstack1l1ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ൛") else bstack1l1ll111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ൜")
        reason = bstack1l1ll111_opy_ (u"ࠬ࠭൝")
        if (reason != bstack1l1ll111_opy_ (u"ࠨࠢ൞")):
          try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
          except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
          threading.current_thread().bstackTestErrorMessages.append(str(reason))
        if status == bstack1l1ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧൟ"):
          reason = rep.longrepr.reprcrash.message
          if (not threading.current_thread().bstackTestErrorMessages):
            threading.current_thread().bstackTestErrorMessages = []
          threading.current_thread().bstackTestErrorMessages.append(reason)
        level = bstack1l1ll111_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ൠ") if status == bstack1l1ll111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩൡ") else bstack1l1ll111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩൢ")
        data = name + bstack1l1ll111_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ൣ") if status == bstack1l1ll111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ൤") else name + bstack1l1ll111_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩ൥") + reason
        bstack11llll1_opy_ = bstack11l1l1l1l_opy_(bstack1l1ll111_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ൦"), bstack1l1ll111_opy_ (u"ࠨࠩ൧"), bstack1l1ll111_opy_ (u"ࠩࠪ൨"), bstack1l1ll111_opy_ (u"ࠪࠫ൩"), level, data)
        for driver in bstack1lll1ll11_opy_:
          if bstack1l11ll1l1_opy_ == driver.session_id:
            driver.execute_script(bstack11llll1_opy_)
      except Exception as e:
        logger.debug(bstack1l1ll111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ൪").format(str(e)))
  except Exception as e:
    logger.debug(bstack1l1ll111_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩ൫").format(str(e)))
  bstack111lllll1_opy_(item, call, rep)
def bstack11lll11l1_opy_(framework_name):
  global bstack1l1l1_opy_
  global bstack1llll1l1l_opy_
  global bstack1llll111_opy_
  bstack1l1l1_opy_ = framework_name
  logger.info(bstack1ll111lll_opy_.format(bstack1l1l1_opy_.split(bstack1l1ll111_opy_ (u"࠭࠭ࠨ൬"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    Service.start = bstack1l11l1l1_opy_
    Service.stop = bstack111ll111_opy_
    webdriver.Remote.__init__ = bstack1ll11ll1_opy_
    webdriver.Remote.get = bstack1l1lll11_opy_
    WebDriver.close = bstack1l1lllll1_opy_
    WebDriver.quit = bstack1l1l1l11l_opy_
    bstack1llll1l1l_opy_ = True
  except Exception as e:
    pass
  bstack111l11ll1_opy_()
  if not bstack1llll1l1l_opy_:
    bstack1111lll1_opy_(bstack1l1ll111_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤ൭"), bstack11ll1l11_opy_)
  if bstack1l111ll_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1l1l1l1l1_opy_
    except Exception as e:
      logger.error(bstack11l111_opy_.format(str(e)))
  if (bstack1l1ll111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ൮") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11l1l11l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1111ll11_opy_
      except Exception as e:
        logger.warn(bstack111l1111l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1111111l_opy_
      except Exception as e:
        logger.debug(bstack11l1l111_opy_ + str(e))
    except Exception as e:
      bstack1111lll1_opy_(e, bstack111l1111l_opy_)
    Output.end_test = bstack11111l_opy_
    TestStatus.__init__ = bstack111l11_opy_
    QueueItem.__init__ = bstack1l11111ll_opy_
    pabot._create_items = bstack1ll1l1_opy_
    try:
      from pabot import __version__ as bstack1llll1ll_opy_
      if version.parse(bstack1llll1ll_opy_) >= version.parse(bstack1l1ll111_opy_ (u"ࠩ࠵࠲࠶࠻࠮࠱ࠩ൯")):
        pabot._run = bstack1l1ll1_opy_
      elif version.parse(bstack1llll1ll_opy_) >= version.parse(bstack1l1ll111_opy_ (u"ࠪ࠶࠳࠷࠳࠯࠲ࠪ൰")):
        pabot._run = bstack111l11ll_opy_
      else:
        pabot._run = bstack1l11lll1_opy_
    except Exception as e:
      pabot._run = bstack1l11lll1_opy_
    pabot._create_command_for_execution = bstack1l1ll11l_opy_
    pabot._report_results = bstack11l1l1ll_opy_
  if bstack1l1ll111_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ൱") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1111lll1_opy_(e, bstack1l1llll11_opy_)
    Runner.run_hook = bstack1llllll_opy_
    Step.run = bstack1ll11111_opy_
  if bstack1l1ll111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ൲") in str(framework_name).lower():
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11ll1ll1l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack111l11l_opy_
      Config.getoption = bstack1ll1l1lll_opy_
    except Exception as e:
      pass
    try:
      from _pytest import runner
      runner._update_current_test_var = bstack1ll1llll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l11lll_opy_
    except Exception as e:
      pass
def bstack1111l11l_opy_():
  global CONFIG
  if bstack1l1ll111_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭൳") in CONFIG and int(CONFIG[bstack1l1ll111_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ൴")]) > 1:
    logger.warn(bstack1lll1l111_opy_)
def bstack1ll1lll1_opy_(arg):
  arg.append(bstack1l1ll111_opy_ (u"ࠣ࠯࠰࡭ࡲࡶ࡯ࡳࡶ࠰ࡱࡴࡪࡥ࠾࡫ࡰࡴࡴࡸࡴ࡭࡫ࡥࠦ൵"))
  arg.append(bstack1l1ll111_opy_ (u"ࠤ࠰࡛ࠧ൶"))
  arg.append(bstack1l1ll111_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡑࡴࡪࡵ࡭ࡧࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡳࡰࡰࡴࡷࡩࡩࡀࡰࡺࡶࡨࡷࡹ࠴ࡐࡺࡶࡨࡷࡹ࡝ࡡࡳࡰ࡬ࡲ࡬ࠨ൷"))
  arg.append(bstack1l1ll111_opy_ (u"ࠦ࠲࡝ࠢ൸"))
  arg.append(bstack1l1ll111_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿࡚ࡨࡦࠢ࡫ࡳࡴࡱࡩ࡮ࡲ࡯ࠦ൹"))
  global CONFIG
  bstack11lll11l1_opy_(bstack1l11l11l1_opy_)
  os.environ[bstack1l1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧൺ")] = CONFIG[bstack1l1ll111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩൻ")]
  os.environ[bstack1l1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫർ")] = CONFIG[bstack1l1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬൽ")]
  from _pytest.config import main as bstack11lll11ll_opy_
  bstack11lll11ll_opy_(arg)
def bstack1l11ll11_opy_(arg):
  bstack11lll11l1_opy_(bstack1l1ll1ll1_opy_)
  from behave.__main__ import main as bstack1l1lll1_opy_
  bstack1l1lll1_opy_(arg)
def bstack1ll1lll1l_opy_():
  logger.info(bstack1ll11ll1l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l1ll111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩൾ"), help=bstack1l1ll111_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡩ࡯࡯ࡨ࡬࡫ࠬൿ"))
  parser.add_argument(bstack1l1ll111_opy_ (u"ࠬ࠳ࡵࠨ඀"), bstack1l1ll111_opy_ (u"࠭࠭࠮ࡷࡶࡩࡷࡴࡡ࡮ࡧࠪඁ"), help=bstack1l1ll111_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡺࡹࡥࡳࡰࡤࡱࡪ࠭ං"))
  parser.add_argument(bstack1l1ll111_opy_ (u"ࠨ࠯࡮ࠫඃ"), bstack1l1ll111_opy_ (u"ࠩ࠰࠱ࡰ࡫ࡹࠨ඄"), help=bstack1l1ll111_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡢࡥࡦࡩࡸࡹࠠ࡬ࡧࡼࠫඅ"))
  parser.add_argument(bstack1l1ll111_opy_ (u"ࠫ࠲࡬ࠧආ"), bstack1l1ll111_opy_ (u"ࠬ࠳࠭ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪඇ"), help=bstack1l1ll111_opy_ (u"࡙࠭ࡰࡷࡵࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬඈ"))
  bstack1l111l11_opy_ = parser.parse_args()
  try:
    bstack1l1ll1111_opy_ = bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡧࡦࡰࡨࡶ࡮ࡩ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫඉ")
    if bstack1l111l11_opy_.framework and bstack1l111l11_opy_.framework not in (bstack1l1ll111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨඊ"), bstack1l1ll111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪඋ")):
      bstack1l1ll1111_opy_ = bstack1l1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩඌ")
    bstack111l1ll1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1ll1111_opy_)
    bstack111111l_opy_ = open(bstack111l1ll1_opy_, bstack1l1ll111_opy_ (u"ࠫࡷ࠭ඍ"))
    bstack1l11l_opy_ = bstack111111l_opy_.read()
    bstack111111l_opy_.close()
    if bstack1l111l11_opy_.username:
      bstack1l11l_opy_ = bstack1l11l_opy_.replace(bstack1l1ll111_opy_ (u"ࠬ࡟ࡏࡖࡔࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬඎ"), bstack1l111l11_opy_.username)
    if bstack1l111l11_opy_.key:
      bstack1l11l_opy_ = bstack1l11l_opy_.replace(bstack1l1ll111_opy_ (u"࡙࠭ࡐࡗࡕࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠨඏ"), bstack1l111l11_opy_.key)
    if bstack1l111l11_opy_.framework:
      bstack1l11l_opy_ = bstack1l11l_opy_.replace(bstack1l1ll111_opy_ (u"࡚ࠧࡑࡘࡖࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨඐ"), bstack1l111l11_opy_.framework)
    file_name = bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫඑ")
    file_path = os.path.abspath(file_name)
    bstack1111l1l1_opy_ = open(file_path, bstack1l1ll111_opy_ (u"ࠩࡺࠫඒ"))
    bstack1111l1l1_opy_.write(bstack1l11l_opy_)
    bstack1111l1l1_opy_.close()
    logger.info(bstack111lll1ll_opy_)
    try:
      os.environ[bstack1l1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬඓ")] = bstack1l111l11_opy_.framework if bstack1l111l11_opy_.framework != None else bstack1l1ll111_opy_ (u"ࠦࠧඔ")
      config = yaml.safe_load(bstack1l11l_opy_)
      config[bstack1l1ll111_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬඕ")] = bstack1l1ll111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡳࡦࡶࡸࡴࠬඖ")
      bstack1lll1l11l_opy_(bstack11l11l1l_opy_, config)
    except Exception as e:
      logger.debug(bstack1l111l1ll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1ll1ll1l1_opy_.format(str(e)))
def bstack1lll1l11l_opy_(bstack11l11_opy_, config, bstack11ll11l_opy_ = {}):
  global bstack1l11l1ll_opy_
  if not config:
    return
  bstack111l1l1_opy_ = bstack1ll1lll_opy_ if not bstack1l11l1ll_opy_ else ( bstack111l1l11_opy_ if bstack1l1ll111_opy_ (u"ࠧࡢࡲࡳࠫ඗") in config else bstack11lll11_opy_ )
  data = {
    bstack1l1ll111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ඘"): config[bstack1l1ll111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ඙")],
    bstack1l1ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ක"): config[bstack1l1ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧඛ")],
    bstack1l1ll111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩග"): bstack11l11_opy_,
    bstack1l1ll111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩඝ"): {
      bstack1l1ll111_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬඞ"): str(config[bstack1l1ll111_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨඟ")]) if bstack1l1ll111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩච") in config else bstack1l1ll111_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦඡ"),
      bstack1l1ll111_opy_ (u"ࠫࡷ࡫ࡦࡦࡴࡵࡩࡷ࠭ජ"): bstack11l1lll1l_opy_(os.getenv(bstack1l1ll111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠢඣ"), bstack1l1ll111_opy_ (u"ࠨࠢඤ"))),
      bstack1l1ll111_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩඥ"): bstack1l1ll111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨඦ"),
      bstack1l1ll111_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪට"): bstack111l1l1_opy_,
      bstack1l1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ඨ"): config[bstack1l1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧඩ")]if config[bstack1l1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨඪ")] else bstack1l1ll111_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢණ"),
      bstack1l1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩඬ"): str(config[bstack1l1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪත")]) if bstack1l1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫථ") in config else bstack1l1ll111_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦද"),
      bstack1l1ll111_opy_ (u"ࠫࡴࡹࠧධ"): sys.platform,
      bstack1l1ll111_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧන"): socket.gethostname()
    }
  }
  update(data[bstack1l1ll111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ඲")], bstack11ll11l_opy_)
  try:
    response = bstack1l1l1ll_opy_(bstack1l1ll111_opy_ (u"ࠧࡑࡑࡖࡘࠬඳ"), bstack11l11l11_opy_, data, config)
    if response:
      logger.debug(bstack11ll1_opy_.format(bstack11l11_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1ll1l_opy_.format(str(e)))
def bstack1l1l1ll_opy_(type, url, data, config):
  bstack1l11lll1l_opy_ = bstack1111ll1l_opy_.format(url)
  proxies = bstack1lll1111l_opy_(config, bstack1l11lll1l_opy_)
  if type == bstack1l1ll111_opy_ (u"ࠨࡒࡒࡗ࡙࠭ප"):
    response = requests.post(bstack1l11lll1l_opy_, json=data,
                    headers={bstack1l1ll111_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨඵ"): bstack1l1ll111_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭බ")}, auth=(config[bstack1l1ll111_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭භ")], config[bstack1l1ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨම")]), proxies=proxies)
  return response
def bstack11l1lll1l_opy_(framework):
  return bstack1l1ll111_opy_ (u"ࠨࡻࡾ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥඹ").format(str(framework), __version__) if framework else bstack1l1ll111_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣය").format(__version__)
def bstack111llll11_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack111ll_opy_()
    logger.debug(bstack111l1l11l_opy_.format(str(CONFIG)))
    bstack1l1111lll_opy_()
    bstack1l1ll111l_opy_()
  except Exception as e:
    logger.error(bstack1l1ll111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧර") + str(e))
    sys.exit(1)
  sys.excepthook = bstack11llll1l_opy_
  atexit.register(bstack11lllll1_opy_)
  signal.signal(signal.SIGINT, bstack11l1ll1ll_opy_)
  signal.signal(signal.SIGTERM, bstack11l1ll1ll_opy_)
def bstack11llll1l_opy_(exctype, value, traceback):
  global bstack1lll1ll11_opy_
  try:
    for driver in bstack1lll1ll11_opy_:
      driver.execute_script(
        bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩ඼") + json.dumps(bstack1l1ll111_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨල") + str(value)) + bstack1l1ll111_opy_ (u"ࠫࢂࢃࠧ඾"))
  except Exception:
    pass
  bstack11lll1ll1_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11lll1ll1_opy_(message = bstack1l1ll111_opy_ (u"ࠬ࠭඿")):
  global CONFIG
  try:
    if message:
      bstack11ll11l_opy_ = {
        bstack1l1ll111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬව"): str(message)
      }
      bstack1lll1l11l_opy_(bstack111ll1111_opy_, CONFIG, bstack11ll11l_opy_)
    else:
      bstack1lll1l11l_opy_(bstack111ll1111_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l111_opy_.format(str(e)))
def bstack11l111111_opy_(bstack1ll11l1ll_opy_, size):
  bstack11ll1ll11_opy_ = []
  while len(bstack1ll11l1ll_opy_) > size:
    bstack111llllll_opy_ = bstack1ll11l1ll_opy_[:size]
    bstack11ll1ll11_opy_.append(bstack111llllll_opy_)
    bstack1ll11l1ll_opy_   = bstack1ll11l1ll_opy_[size:]
  bstack11ll1ll11_opy_.append(bstack1ll11l1ll_opy_)
  return bstack11ll1ll11_opy_
def bstack1l111ll11_opy_(args):
  if bstack1l1ll111_opy_ (u"ࠧ࠮࡯ࠪශ") in args and bstack1l1ll111_opy_ (u"ࠨࡲࡧࡦࠬෂ") in args:
    return True
  return False
def run_on_browserstack(bstack11l1lll_opy_=None, bstack1l1l11111_opy_=None, bstack111ll1l1l_opy_=False):
  global CONFIG
  global bstack11lll111l_opy_
  global bstack1l111l11l_opy_
  bstack11l11ll11_opy_ = bstack1l1ll111_opy_ (u"ࠩࠪස")
  if bstack11l1lll_opy_ and isinstance(bstack11l1lll_opy_, str):
    bstack11l1lll_opy_ = eval(bstack11l1lll_opy_)
  if bstack11l1lll_opy_:
    CONFIG = bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪහ")]
    bstack11lll111l_opy_ = bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬළ")]
    bstack1l111l11l_opy_ = bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧෆ")]
    bstack11l11ll11_opy_ = bstack1l1ll111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭෇")
  if not bstack111ll1l1l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack111l11l1l_opy_)
      return
    if sys.argv[1] == bstack1l1ll111_opy_ (u"ࠧ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪ෈")  or sys.argv[1] == bstack1l1ll111_opy_ (u"ࠨ࠯ࡹࠫ෉"):
      logger.info(bstack1l1ll111_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡕࡇࡏࠥࡼࡻࡾ්ࠩ").format(__version__))
      return
    if sys.argv[1] == bstack1l1ll111_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ෋"):
      bstack1ll1lll1l_opy_()
      return
  args = sys.argv
  bstack111llll11_opy_()
  global bstack1llll11_opy_
  global bstack1ll_opy_
  global bstack11l1l1l_opy_
  global bstack11l111ll_opy_
  global bstack11lllll11_opy_
  global bstack1l1l1llll_opy_
  global bstack1l1lll111_opy_
  global bstack1llll111_opy_
  if not bstack11l11ll11_opy_:
    if args[1] == bstack1l1ll111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ෌") or args[1] == bstack1l1ll111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭෍"):
      bstack11l11ll11_opy_ = bstack1l1ll111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭෎")
      args = args[2:]
    elif args[1] == bstack1l1ll111_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ා"):
      bstack11l11ll11_opy_ = bstack1l1ll111_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧැ")
      args = args[2:]
    elif args[1] == bstack1l1ll111_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨෑ"):
      bstack11l11ll11_opy_ = bstack1l1ll111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩි")
      args = args[2:]
    elif args[1] == bstack1l1ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬී"):
      bstack11l11ll11_opy_ = bstack1l1ll111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ු")
      args = args[2:]
    elif args[1] == bstack1l1ll111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෕"):
      bstack11l11ll11_opy_ = bstack1l1ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧූ")
      args = args[2:]
    elif args[1] == bstack1l1ll111_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ෗"):
      bstack11l11ll11_opy_ = bstack1l1ll111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩෘ")
      args = args[2:]
    else:
      if not bstack1l1ll111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ෙ") in CONFIG or str(CONFIG[bstack1l1ll111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧේ")]).lower() in [bstack1l1ll111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬෛ"), bstack1l1ll111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧො")]:
        bstack11l11ll11_opy_ = bstack1l1ll111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧෝ")
        args = args[1:]
      elif str(CONFIG[bstack1l1ll111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫෞ")]).lower() == bstack1l1ll111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨෟ"):
        bstack11l11ll11_opy_ = bstack1l1ll111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ෠")
        args = args[1:]
      elif str(CONFIG[bstack1l1ll111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ෡")]).lower() == bstack1l1ll111_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ෢"):
        bstack11l11ll11_opy_ = bstack1l1ll111_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ෣")
        args = args[1:]
      elif str(CONFIG[bstack1l1ll111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ෤")]).lower() == bstack1l1ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ෥"):
        bstack11l11ll11_opy_ = bstack1l1ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ෦")
        args = args[1:]
      elif str(CONFIG[bstack1l1ll111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭෧")]).lower() == bstack1l1ll111_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ෨"):
        bstack11l11ll11_opy_ = bstack1l1ll111_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ෩")
        args = args[1:]
      else:
        os.environ[bstack1l1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ෪")] = bstack11l11ll11_opy_
        bstack11lll1l11_opy_(bstack1l1lll1l1_opy_)
  global bstack1l11l1_opy_
  if bstack11l1lll_opy_:
    try:
      os.environ[bstack1l1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ෫")] = bstack11l11ll11_opy_
      bstack1lll1l11l_opy_(bstack1l1l11ll1_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1l111_opy_.format(str(e)))
  global bstack1lll111_opy_
  global bstack1111lll1l_opy_
  global bstack1l111llll_opy_
  global bstack1lll11ll_opy_
  global bstack1111l111_opy_
  global bstack1lll11l1l_opy_
  global bstack11l1111l1_opy_
  global bstack11l1l1ll1_opy_
  global bstack1lll11111_opy_
  global bstack11l11l111_opy_
  global bstack11l1l1_opy_
  global bstack11l1111ll_opy_
  global bstack1llll11l1_opy_
  global bstack1l111111l_opy_
  global bstack1l1lll1l_opy_
  global bstack1l1ll1lll_opy_
  global bstack1l11l111_opy_
  global bstack1lllll1_opy_
  global bstack111lllll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll111_opy_ = webdriver.Remote.__init__
    bstack1111lll1l_opy_ = WebDriver.quit
    bstack11l1l1_opy_ = WebDriver.close
    bstack1l111111l_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l11l1_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack111l1ll_opy_():
    if bstack1l1l1l11_opy_() < version.parse(bstack1l1ll1ll_opy_):
      logger.error(bstack1111l_opy_.format(bstack1l1l1l11_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1lll1l_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack11l111_opy_.format(str(e)))
  if bstack11l11ll11_opy_ != bstack1l1ll111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ෬") or (bstack11l11ll11_opy_ == bstack1l1ll111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ෭") and not bstack11l1lll_opy_):
    bstack1l111lll_opy_()
  if (bstack11l11ll11_opy_ in [bstack1l1ll111_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ෮"), bstack1l1ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ෯"), bstack1l1ll111_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭෰")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack11l1l11l_opy_
        bstack1111l111_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack111l1111l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1lll11ll_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack11l1l111_opy_ + str(e))
    except Exception as e:
      bstack1111lll1_opy_(e, bstack111l1111l_opy_)
    if bstack11l11ll11_opy_ != bstack1l1ll111_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ෱"):
      bstack11ll11l11_opy_()
    bstack1l111llll_opy_ = Output.end_test
    bstack1lll11l1l_opy_ = TestStatus.__init__
    bstack11l1l1ll1_opy_ = pabot._run
    bstack1lll11111_opy_ = QueueItem.__init__
    bstack11l11l111_opy_ = pabot._create_command_for_execution
    bstack1lllll1_opy_ = pabot._report_results
  if bstack11l11ll11_opy_ == bstack1l1ll111_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧෲ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1111lll1_opy_(e, bstack1l1llll11_opy_)
    bstack11l1111ll_opy_ = Runner.run_hook
    bstack1llll11l1_opy_ = Step.run
  if bstack11l11ll11_opy_ == bstack1l1ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨෳ"):
    try:
      from _pytest.config import Config
      bstack1l1ll1lll_opy_ = Config.getoption
      from _pytest import runner
      bstack1l11l111_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l1l111l_opy_)
    try:
      from pytest_bdd import reporting
      bstack111lllll1_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1l1ll111_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪ෴"))
  if bstack11l11ll11_opy_ == bstack1l1ll111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ෵"):
    bstack1ll_opy_ = True
    if bstack11l1lll_opy_ and bstack111ll1l1l_opy_:
      bstack11lllll11_opy_ = CONFIG.get(bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ෶"), {}).get(bstack1l1ll111_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ෷"))
      bstack11lll11l1_opy_(bstack1l111l1l_opy_)
    elif bstack11l1lll_opy_:
      bstack11lllll11_opy_ = CONFIG.get(bstack1l1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ෸"), {}).get(bstack1l1ll111_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ෹"))
      global bstack1lll1ll11_opy_
      try:
        if bstack1l111ll11_opy_(bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ෺")]) and multiprocessing.current_process().name == bstack1l1ll111_opy_ (u"ࠩ࠳ࠫ෻"):
          bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෼")].remove(bstack1l1ll111_opy_ (u"ࠫ࠲ࡳࠧ෽"))
          bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ෾")].remove(bstack1l1ll111_opy_ (u"࠭ࡰࡥࡤࠪ෿"))
          bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ฀")] = bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫก")][0]
          with open(bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬข")], bstack1l1ll111_opy_ (u"ࠪࡶࠬฃ")) as f:
            bstack11111l1l_opy_ = f.read()
          bstack1111l1_opy_ = bstack1l1ll111_opy_ (u"ࠦࠧࠨࡦࡳࡱࡰࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡩࡱࠠࡪ࡯ࡳࡳࡷࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧ࠾ࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࠨࡼࡿࠬ࠿ࠥ࡬ࡲࡰ࡯ࠣࡴࡩࡨࠠࡪ࡯ࡳࡳࡷࡺࠠࡑࡦࡥ࠿ࠥࡵࡧࡠࡦࡥࠤࡂࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࡀࠐࡤࡦࡨࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰ࠮ࡳࡦ࡮ࡩ࠰ࠥࡧࡲࡨ࠮ࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦ࠽ࠡ࠲ࠬ࠾ࠏࠦࠠࡵࡴࡼ࠾ࠏࠦࠠࠡࠢࡤࡶ࡬ࠦ࠽ࠡࡵࡷࡶ࠭࡯࡮ࡵࠪࡤࡶ࡬࠯ࠫ࠲࠲ࠬࠎࠥࠦࡥࡹࡥࡨࡴࡹࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡤࡷࠥ࡫࠺ࠋࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࡵࡧࡠࡦࡥࠬࡸ࡫࡬ࡧ࠮ࡤࡶ࡬࠲ࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠫࠍࡔࡩࡨ࠮ࡥࡱࡢࡦࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࡔࡩࡨ࠮ࡥࡱࡢࡦࡷ࡫ࡡ࡬ࠢࡀࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠊࡑࡦࡥࠬ࠮࠴ࡳࡦࡶࡢࡸࡷࡧࡣࡦࠪࠬࡠࡳࠨࠢࠣค").format(str(bstack11l1lll_opy_))
          bstack1l1l1ll1_opy_ = bstack1111l1_opy_ + bstack11111l1l_opy_
          bstack11l1ll_opy_ = bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨฅ")] + bstack1l1ll111_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡵࡧࡰࡴ࠳ࡶࡹࠨฆ")
          with open(bstack11l1ll_opy_, bstack1l1ll111_opy_ (u"ࠧࡸࠩง")):
            pass
          with open(bstack11l1ll_opy_, bstack1l1ll111_opy_ (u"ࠣࡹ࠮ࠦจ")) as f:
            f.write(bstack1l1l1ll1_opy_)
          import subprocess
          bstack11l11l1ll_opy_ = subprocess.run([bstack1l1ll111_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤฉ"), bstack11l1ll_opy_])
          if os.path.exists(bstack11l1ll_opy_):
            os.unlink(bstack11l1ll_opy_)
          os._exit(bstack11l11l1ll_opy_.returncode)
        else:
          if bstack1l111ll11_opy_(bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ช")]):
            bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧซ")].remove(bstack1l1ll111_opy_ (u"ࠬ࠳࡭ࠨฌ"))
            bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩญ")].remove(bstack1l1ll111_opy_ (u"ࠧࡱࡦࡥࠫฎ"))
            bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫฏ")] = bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬฐ")][0]
          bstack11lll11l1_opy_(bstack1l111l1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ฑ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1l1ll111_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭ฒ")] = bstack1l1ll111_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧณ")
          mod_globals[bstack1l1ll111_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨด")] = os.path.abspath(bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪต")])
          exec(open(bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫถ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1l1ll111_opy_ (u"ࠩࡆࡥࡺ࡭ࡨࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠩท").format(str(e)))
          for driver in bstack1lll1ll11_opy_:
            bstack1l1l11111_opy_.append({
              bstack1l1ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨธ"): bstack11l1lll_opy_[bstack1l1ll111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧน")],
              bstack1l1ll111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫบ"): str(e),
              bstack1l1ll111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬป"): multiprocessing.current_process().name
            })
            driver.execute_script(
              bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ࠮ࠣࠦࡷ࡫ࡡࡴࡱࡱࠦ࠿ࠦࠧผ") + json.dumps(bstack1l1ll111_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦฝ") + str(e)) + bstack1l1ll111_opy_ (u"ࠩࢀࢁࠬพ"))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1lll1ll11_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      bstack1llll111l_opy_()
      bstack1111l11l_opy_()
      bstack1ll1111_opy_ = {
        bstack1l1ll111_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ฟ"): args[0],
        bstack1l1ll111_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫภ"): CONFIG,
        bstack1l1ll111_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ม"): bstack11lll111l_opy_,
        bstack1l1ll111_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨย"): bstack1l111l11l_opy_
      }
      if bstack1l1ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪร") in CONFIG:
        bstack11ll1ll_opy_ = []
        manager = multiprocessing.Manager()
        bstack1llll1l_opy_ = manager.list()
        if bstack1l111ll11_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1l1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫฤ")]):
            if index == 0:
              bstack1ll1111_opy_[bstack1l1ll111_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬล")] = args
            bstack11ll1ll_opy_.append(multiprocessing.Process(name=str(index),
                                          target=run_on_browserstack, args=(bstack1ll1111_opy_, bstack1llll1l_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1l1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ฦ")]):
            bstack11ll1ll_opy_.append(multiprocessing.Process(name=str(index),
                                          target=run_on_browserstack, args=(bstack1ll1111_opy_, bstack1llll1l_opy_)))
        for t in bstack11ll1ll_opy_:
          t.start()
        for t in bstack11ll1ll_opy_:
          t.join()
        bstack1l1lll111_opy_ = list(bstack1llll1l_opy_)
      else:
        if bstack1l111ll11_opy_(args):
          bstack1ll1111_opy_[bstack1l1ll111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧว")] = args
          test = multiprocessing.Process(name=str(0),
                                        target=run_on_browserstack, args=(bstack1ll1111_opy_,))
          test.start()
          test.join()
        else:
          bstack11lll11l1_opy_(bstack1l111l1l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1l1ll111_opy_ (u"ࠬࡥ࡟࡯ࡣࡰࡩࡤࡥࠧศ")] = bstack1l1ll111_opy_ (u"࠭࡟ࡠ࡯ࡤ࡭ࡳࡥ࡟ࠨษ")
          mod_globals[bstack1l1ll111_opy_ (u"ࠧࡠࡡࡩ࡭ࡱ࡫࡟ࡠࠩส")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11l11ll11_opy_ == bstack1l1ll111_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧห") or bstack11l11ll11_opy_ == bstack1l1ll111_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨฬ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1111lll1_opy_(e, bstack111l1111l_opy_)
    bstack1llll111l_opy_()
    bstack11lll11l1_opy_(bstack111l1lll_opy_)
    if bstack1l1ll111_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨอ") in args:
      i = args.index(bstack1l1ll111_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩฮ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1llll11_opy_))
    args.insert(0, str(bstack1l1ll111_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪฯ")))
    pabot.main(args)
  elif bstack11l11ll11_opy_ == bstack1l1ll111_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧะ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1111lll1_opy_(e, bstack111l1111l_opy_)
    for a in args:
      if bstack1l1ll111_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ั") in a:
        bstack11l111ll_opy_ = int(a.split(bstack1l1ll111_opy_ (u"ࠨ࠼ࠪา"))[1])
      if bstack1l1ll111_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ำ") in a:
        bstack11lllll11_opy_ = str(a.split(bstack1l1ll111_opy_ (u"ࠪ࠾ࠬิ"))[1])
      if bstack1l1ll111_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫี") in a:
        bstack1l1l1llll_opy_ = str(a.split(bstack1l1ll111_opy_ (u"ࠬࡀࠧึ"))[1])
    bstack11l1111l_opy_ = None
    if bstack1l1ll111_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬื") in args:
      i = args.index(bstack1l1ll111_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽุ࠭"))
      args.pop(i)
      bstack11l1111l_opy_ = args.pop(i)
    if bstack11l1111l_opy_ is not None:
      global bstack11l1l_opy_
      bstack11l1l_opy_ = bstack11l1111l_opy_
    bstack11lll11l1_opy_(bstack111l1lll_opy_)
    run_cli(args)
  elif bstack11l11ll11_opy_ == bstack1l1ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨู"):
    try:
      from _pytest.config import _prepareconfig
      from _pytest.config import Config
      from _pytest import runner
      import importlib
      bstack11ll111ll_opy_ = importlib.find_loader(bstack1l1ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰฺࠫ"))
    except Exception as e:
      logger.warn(e, bstack1l1l111l_opy_)
    bstack1llll111l_opy_()
    try:
      if bstack1l1ll111_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬ฻") in args:
        i = args.index(bstack1l1ll111_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭฼"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l1ll111_opy_ (u"ࠬ࠳࠭ࡱ࡮ࡸ࡫࡮ࡴࡳࠨ฽") in args:
        i = args.index(bstack1l1ll111_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩ฾"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l1ll111_opy_ (u"ࠧ࠮ࡲࠪ฿") in args:
        i = args.index(bstack1l1ll111_opy_ (u"ࠨ࠯ࡳࠫเ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l1ll111_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪแ") in args:
        i = args.index(bstack1l1ll111_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫโ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l1ll111_opy_ (u"ࠫ࠲ࡴࠧใ") in args:
        i = args.index(bstack1l1ll111_opy_ (u"ࠬ࠳࡮ࠨไ"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack1l1l1l_opy_ = config.args
    bstack1ll11ll_opy_ = config.invocation_params.args
    bstack1ll11ll_opy_ = list(bstack1ll11ll_opy_)
    bstack1ll1l11_opy_ = [os.path.normpath(item) for item in bstack1l1l1l_opy_]
    bstack1l1l11l11_opy_ = [os.path.normpath(item) for item in bstack1ll11ll_opy_]
    bstack111ll1lll_opy_ = [item for item in bstack1l1l11l11_opy_ if item not in bstack1ll1l11_opy_]
    if bstack1l1ll111_opy_ (u"࠭࠭࠮ࡥࡤࡧ࡭࡫࠭ࡤ࡮ࡨࡥࡷ࠭ๅ") not in bstack111ll1lll_opy_:
      bstack111ll1lll_opy_.append(bstack1l1ll111_opy_ (u"ࠧ࠮࠯ࡦࡥࡨ࡮ࡥ࠮ࡥ࡯ࡩࡦࡸࠧๆ"))
    import platform as pf
    if pf.system().lower() == bstack1l1ll111_opy_ (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩ็"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l1l1l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1llll11ll_opy_)))
                    for bstack1llll11ll_opy_ in bstack1l1l1l_opy_]
    if (bstack11111_opy_):
      bstack111ll1lll_opy_.append(bstack1l1ll111_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ่࠭"))
      bstack111ll1lll_opy_.append(bstack1l1ll111_opy_ (u"ࠪࡘࡷࡻࡥࠨ้"))
    try:
      from pytest_bdd import reporting
      bstack1llll111_opy_ = True
    except Exception as e:
      pass
    if (not bstack1llll111_opy_):
      bstack111ll1lll_opy_.append(bstack1l1ll111_opy_ (u"ࠫ࠲ࡶ๊ࠧ"))
      bstack111ll1lll_opy_.append(bstack1l1ll111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰ๋ࠪ"))
    bstack111ll1lll_opy_.append(bstack1l1ll111_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨ์"))
    bstack111ll1lll_opy_.append(bstack1l1ll111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧํ"))
    bstack11l11ll1l_opy_ = []
    for spec in bstack1l1l1l_opy_:
      bstack1lll1l1_opy_ = []
      bstack1lll1l1_opy_.append(spec)
      bstack1lll1l1_opy_ += bstack111ll1lll_opy_
      bstack11l11ll1l_opy_.append(bstack1lll1l1_opy_)
    bstack11l1l1l_opy_ = True
    bstack11l1l1l11_opy_ = 1
    if bstack1l1ll111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ๎") in CONFIG:
      bstack11l1l1l11_opy_ = CONFIG[bstack1l1ll111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ๏")]
    bstack11ll11lll_opy_ = int(bstack11l1l1l11_opy_)*int(len(CONFIG[bstack1l1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭๐")]))
    execution_items = []
    for bstack1lll1l1_opy_ in bstack11l11ll1l_opy_:
      for index, _ in enumerate(CONFIG[bstack1l1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ๑")]):
        item = {}
        item[bstack1l1ll111_opy_ (u"ࠬࡧࡲࡨࠩ๒")] = bstack1lll1l1_opy_
        item[bstack1l1ll111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ๓")] = index
        execution_items.append(item)
    bstack111l_opy_ = bstack11l111111_opy_(execution_items, bstack11ll11lll_opy_)
    for execution_item in bstack111l_opy_:
      bstack11ll1ll_opy_ = []
      for item in execution_item:
        bstack11ll1ll_opy_.append(bstack1lll11l1_opy_(name=str(item[bstack1l1ll111_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭๔")]),
                                            target=bstack1ll1lll1_opy_,
                                            args=(item[bstack1l1ll111_opy_ (u"ࠨࡣࡵ࡫ࠬ๕")],)))
      for t in bstack11ll1ll_opy_:
        t.start()
      for t in bstack11ll1ll_opy_:
        t.join()
  elif bstack11l11ll11_opy_ == bstack1l1ll111_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ๖"):
    try:
      from behave.__main__ import main as bstack1l1lll1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1111lll1_opy_(e, bstack1l1llll11_opy_)
    bstack1llll111l_opy_()
    bstack11l1l1l_opy_ = True
    bstack11l1l1l11_opy_ = 1
    if bstack1l1ll111_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ๗") in CONFIG:
      bstack11l1l1l11_opy_ = CONFIG[bstack1l1ll111_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ๘")]
    bstack11ll11lll_opy_ = int(bstack11l1l1l11_opy_)*int(len(CONFIG[bstack1l1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ๙")]))
    config = Configuration(args)
    bstack1ll1l11l_opy_ = config.paths
    if len(bstack1ll1l11l_opy_) == 0:
      import glob
      pattern = bstack1l1ll111_opy_ (u"࠭ࠪࠫ࠱࠭࠲࡫࡫ࡡࡵࡷࡵࡩࠬ๚")
      bstack1ll1ll1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1ll1ll1_opy_)
      config = Configuration(args)
      bstack1ll1l11l_opy_ = config.paths
    bstack1l1l1l_opy_ = [os.path.normpath(item) for item in bstack1ll1l11l_opy_]
    bstack11l11l1l1_opy_ = [os.path.normpath(item) for item in args]
    bstack1ll11_opy_ = [item for item in bstack11l11l1l1_opy_ if item not in bstack1l1l1l_opy_]
    import platform as pf
    if pf.system().lower() == bstack1l1ll111_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨ๛"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l1l1l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1llll11ll_opy_)))
                    for bstack1llll11ll_opy_ in bstack1l1l1l_opy_]
    bstack11l11ll1l_opy_ = []
    for spec in bstack1l1l1l_opy_:
      bstack1lll1l1_opy_ = []
      bstack1lll1l1_opy_ += bstack1ll11_opy_
      bstack1lll1l1_opy_.append(spec)
      bstack11l11ll1l_opy_.append(bstack1lll1l1_opy_)
    execution_items = []
    for bstack1lll1l1_opy_ in bstack11l11ll1l_opy_:
      for index, _ in enumerate(CONFIG[bstack1l1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ๜")]):
        item = {}
        item[bstack1l1ll111_opy_ (u"ࠩࡤࡶ࡬࠭๝")] = bstack1l1ll111_opy_ (u"ࠪࠤࠬ๞").join(bstack1lll1l1_opy_)
        item[bstack1l1ll111_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ๟")] = index
        execution_items.append(item)
    bstack111l_opy_ = bstack11l111111_opy_(execution_items, bstack11ll11lll_opy_)
    for execution_item in bstack111l_opy_:
      bstack11ll1ll_opy_ = []
      for item in execution_item:
        bstack11ll1ll_opy_.append(bstack1lll11l1_opy_(name=str(item[bstack1l1ll111_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ๠")]),
                                            target=bstack1l11ll11_opy_,
                                            args=(item[bstack1l1ll111_opy_ (u"࠭ࡡࡳࡩࠪ๡")],)))
      for t in bstack11ll1ll_opy_:
        t.start()
      for t in bstack11ll1ll_opy_:
        t.join()
  else:
    bstack11lll1l11_opy_(bstack1l1lll1l1_opy_)
  if not bstack11l1lll_opy_:
    bstack11ll11111_opy_()
def browserstack_initialize(bstack111l1ll1l_opy_=None):
  run_on_browserstack(bstack111l1ll1l_opy_, None, True)
def bstack11ll11111_opy_():
  [bstack1ll111111_opy_, bstack11ll111_opy_] = bstack1l11ll1_opy_()
  if bstack1ll111111_opy_ is not None and bstack11lll1ll_opy_() != -1:
    sessions = bstack111lll11_opy_(bstack1ll111111_opy_)
    bstack1l1l1l1_opy_(sessions, bstack11ll111_opy_)
def bstack11ll11ll_opy_(bstack1lllll11l_opy_):
    if bstack1lllll11l_opy_:
        return bstack1lllll11l_opy_.capitalize()
    else:
        return bstack1lllll11l_opy_
def bstack1lll1l11_opy_(bstack11lll11l_opy_):
    if bstack1l1ll111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ๢") in bstack11lll11l_opy_ and bstack11lll11l_opy_[bstack1l1ll111_opy_ (u"ࠨࡰࡤࡱࡪ࠭๣")] != bstack1l1ll111_opy_ (u"ࠩࠪ๤"):
        return bstack11lll11l_opy_[bstack1l1ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨ๥")]
    else:
        bstack111l1_opy_ = bstack1l1ll111_opy_ (u"ࠦࠧ๦")
        if bstack1l1ll111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ๧") in bstack11lll11l_opy_ and bstack11lll11l_opy_[bstack1l1ll111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭๨")] != None:
            bstack111l1_opy_ += bstack11lll11l_opy_[bstack1l1ll111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ๩")] + bstack1l1ll111_opy_ (u"ࠣ࠮ࠣࠦ๪")
            if bstack11lll11l_opy_[bstack1l1ll111_opy_ (u"ࠩࡲࡷࠬ๫")] == bstack1l1ll111_opy_ (u"ࠥ࡭ࡴࡹࠢ๬"):
                bstack111l1_opy_ += bstack1l1ll111_opy_ (u"ࠦ࡮ࡕࡓࠡࠤ๭")
            bstack111l1_opy_ += (bstack11lll11l_opy_[bstack1l1ll111_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ๮")] or bstack1l1ll111_opy_ (u"࠭ࠧ๯"))
            return bstack111l1_opy_
        else:
            bstack111l1_opy_ += bstack11ll11ll_opy_(bstack11lll11l_opy_[bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ๰")]) + bstack1l1ll111_opy_ (u"ࠣࠢࠥ๱") + (bstack11lll11l_opy_[bstack1l1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ๲")] or bstack1l1ll111_opy_ (u"ࠪࠫ๳")) + bstack1l1ll111_opy_ (u"ࠦ࠱ࠦࠢ๴")
            if bstack11lll11l_opy_[bstack1l1ll111_opy_ (u"ࠬࡵࡳࠨ๵")] == bstack1l1ll111_opy_ (u"ࠨࡗࡪࡰࡧࡳࡼࡹࠢ๶"):
                bstack111l1_opy_ += bstack1l1ll111_opy_ (u"ࠢࡘ࡫ࡱࠤࠧ๷")
            bstack111l1_opy_ += bstack11lll11l_opy_[bstack1l1ll111_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ๸")] or bstack1l1ll111_opy_ (u"ࠩࠪ๹")
            return bstack111l1_opy_
def bstack11ll1l1ll_opy_(bstack111l111_opy_):
    if bstack111l111_opy_ == bstack1l1ll111_opy_ (u"ࠥࡨࡴࡴࡥࠣ๺"):
        return bstack1l1ll111_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡃࡰ࡯ࡳࡰࡪࡺࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ๻")
    elif bstack111l111_opy_ == bstack1l1ll111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ๼"):
        return bstack1l1ll111_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡋࡧࡩ࡭ࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ๽")
    elif bstack111l111_opy_ == bstack1l1ll111_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ๾"):
        return bstack1l1ll111_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡔࡦࡹࡳࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ๿")
    elif bstack111l111_opy_ == bstack1l1ll111_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ຀"):
        return bstack1l1ll111_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡇࡵࡶࡴࡸ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬກ")
    elif bstack111l111_opy_ == bstack1l1ll111_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧຂ"):
        return bstack1l1ll111_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࠤࡧࡨࡥ࠸࠸࠶࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࠦࡩࡪࡧ࠳࠳࠸ࠥࡂ࡙࡯࡭ࡦࡱࡸࡸࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ຃")
    elif bstack111l111_opy_ == bstack1l1ll111_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠢຄ"):
        return bstack1l1ll111_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࡕࡹࡳࡴࡩ࡯ࡩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ຅")
    else:
        return bstack1l1ll111_opy_ (u"ࠨ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࠬຆ")+bstack11ll11ll_opy_(bstack111l111_opy_)+bstack1l1ll111_opy_ (u"ࠩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨງ")
def bstack11llll11_opy_(session):
    return bstack1l1ll111_opy_ (u"ࠪࡀࡹࡸࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡳࡱࡺࠦࡃࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࡾࢁࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࡽࢀࡀ࠴ࡧ࠾࠽࠱ࡷࡨࡃࢁࡽࡼࡿ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁ࠵ࡴࡳࡀࠪຈ").format(session[bstack1l1ll111_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨຉ")],bstack1lll1l11_opy_(session), bstack11ll1l1ll_opy_(session[bstack1l1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶࠫຊ")]), bstack11ll1l1ll_opy_(session[bstack1l1ll111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭຋")]), bstack11ll11ll_opy_(session[bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨຌ")] or session[bstack1l1ll111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨຍ")] or bstack1l1ll111_opy_ (u"ࠩࠪຎ")) + bstack1l1ll111_opy_ (u"ࠥࠤࠧຏ") + (session[bstack1l1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ຐ")] or bstack1l1ll111_opy_ (u"ࠬ࠭ຑ")), session[bstack1l1ll111_opy_ (u"࠭࡯ࡴࠩຒ")] + bstack1l1ll111_opy_ (u"ࠢࠡࠤຓ") + session[bstack1l1ll111_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬດ")], session[bstack1l1ll111_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫຕ")] or bstack1l1ll111_opy_ (u"ࠪࠫຖ"), session[bstack1l1ll111_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨທ")] if session[bstack1l1ll111_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩຘ")] else bstack1l1ll111_opy_ (u"࠭ࠧນ"))
def bstack1l1l1l1_opy_(sessions, bstack11ll111_opy_):
  try:
    bstack11llll_opy_ = bstack1l1ll111_opy_ (u"ࠢࠣບ")
    if not os.path.exists(bstack1l1111ll1_opy_):
      os.mkdir(bstack1l1111ll1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1ll111_opy_ (u"ࠨࡣࡶࡷࡪࡺࡳ࠰ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ࠭ປ")), bstack1l1ll111_opy_ (u"ࠩࡵࠫຜ")) as f:
      bstack11llll_opy_ = f.read()
    bstack11llll_opy_ = bstack11llll_opy_.replace(bstack1l1ll111_opy_ (u"ࠪࡿࠪࡘࡅࡔࡗࡏࡘࡘࡥࡃࡐࡗࡑࡘࠪࢃࠧຝ"), str(len(sessions)))
    bstack11llll_opy_ = bstack11llll_opy_.replace(bstack1l1ll111_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠧࢀࠫພ"), bstack11ll111_opy_)
    bstack11llll_opy_ = bstack11llll_opy_.replace(bstack1l1ll111_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠩࢂ࠭ຟ"), sessions[0].get(bstack1l1ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡡ࡮ࡧࠪຠ")) if sessions[0] else bstack1l1ll111_opy_ (u"ࠧࠨມ"))
    with open(os.path.join(bstack1l1111ll1_opy_, bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬຢ")), bstack1l1ll111_opy_ (u"ࠩࡺࠫຣ")) as stream:
      stream.write(bstack11llll_opy_.split(bstack1l1ll111_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧ຤"))[0])
      for session in sessions:
        stream.write(bstack11llll11_opy_(session))
      stream.write(bstack11llll_opy_.split(bstack1l1ll111_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨລ"))[1])
    logger.info(bstack1l1ll111_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠢࡤࡸࠥࢁࡽࠨ຦").format(bstack1l1111ll1_opy_));
  except Exception as e:
    logger.debug(bstack11lll_opy_.format(str(e)))
def bstack111lll11_opy_(bstack1ll111111_opy_):
  global CONFIG
  try:
    host = bstack1l1ll111_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩວ") if bstack1l1ll111_opy_ (u"ࠧࡢࡲࡳࠫຨ") in CONFIG else bstack1l1ll111_opy_ (u"ࠨࡣࡳ࡭ࠬຩ")
    user = CONFIG[bstack1l1ll111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫສ")]
    key = CONFIG[bstack1l1ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ຫ")]
    bstack1lll11ll1_opy_ = bstack1l1ll111_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪຬ") if bstack1l1ll111_opy_ (u"ࠬࡧࡰࡱࠩອ") in CONFIG else bstack1l1ll111_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨຮ")
    url = bstack1l1ll111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠮࡫ࡵࡲࡲࠬຯ").format(user, key, host, bstack1lll11ll1_opy_, bstack1ll111111_opy_)
    headers = {
      bstack1l1ll111_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧະ"): bstack1l1ll111_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬັ"),
    }
    proxies = bstack1lll1111l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1l1ll111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨາ")], response.json()))
  except Exception as e:
    logger.debug(bstack11lllllll_opy_.format(str(e)))
def bstack1l11ll1_opy_():
  global CONFIG
  try:
    if bstack1l1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧຳ") in CONFIG:
      host = bstack1l1ll111_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨິ") if bstack1l1ll111_opy_ (u"࠭ࡡࡱࡲࠪີ") in CONFIG else bstack1l1ll111_opy_ (u"ࠧࡢࡲ࡬ࠫຶ")
      user = CONFIG[bstack1l1ll111_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪື")]
      key = CONFIG[bstack1l1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽຸࠬ")]
      bstack1lll11ll1_opy_ = bstack1l1ll111_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦູࠩ") if bstack1l1ll111_opy_ (u"ࠫࡦࡶࡰࠨ຺") in CONFIG else bstack1l1ll111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧົ")
      url = bstack1l1ll111_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭ຼ").format(user, key, host, bstack1lll11ll1_opy_)
      headers = {
        bstack1l1ll111_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭ຽ"): bstack1l1ll111_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ຾"),
      }
      if bstack1l1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ຿") in CONFIG:
        params = {bstack1l1ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨເ"):CONFIG[bstack1l1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧແ")], bstack1l1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨໂ"):CONFIG[bstack1l1ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨໃ")]}
      else:
        params = {bstack1l1ll111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬໄ"):CONFIG[bstack1l1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ໅")]}
      proxies = bstack1lll1111l_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1lll_opy_ = response.json()[0][bstack1l1ll111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬໆ")]
        if bstack1lll_opy_:
          bstack11ll111_opy_ = bstack1lll_opy_[bstack1l1ll111_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧ໇")].split(bstack1l1ll111_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦ່ࠪ"))[0] + bstack1l1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴້࠭") + bstack1lll_opy_[bstack1l1ll111_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥ໊ࠩ")]
          logger.info(bstack1l1l111l1_opy_.format(bstack11ll111_opy_))
          bstack1lllll11_opy_ = CONFIG[bstack1l1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ໋ࠪ")]
          if bstack1l1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ໌") in CONFIG:
            bstack1lllll11_opy_ += bstack1l1ll111_opy_ (u"ࠩࠣࠫໍ") + CONFIG[bstack1l1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ໎")]
          if bstack1lllll11_opy_!= bstack1lll_opy_[bstack1l1ll111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ໏")]:
            logger.debug(bstack1111l11_opy_.format(bstack1lll_opy_[bstack1l1ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ໐")], bstack1lllll11_opy_))
          return [bstack1lll_opy_[bstack1l1ll111_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ໑")], bstack11ll111_opy_]
    else:
      logger.warn(bstack11111ll1_opy_)
  except Exception as e:
    logger.debug(bstack11lll1lll_opy_.format(str(e)))
  return [None, None]
def bstack1l11l1111_opy_(url, bstack11l11111l_opy_=False):
  global CONFIG
  global bstack11l1l1l1_opy_
  if not bstack11l1l1l1_opy_:
    hostname = bstack111ll1l11_opy_(url)
    is_private = bstack11ll_opy_(hostname)
    if (bstack1l1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ໒") in CONFIG and not CONFIG[bstack1l1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ໓")]) and (is_private or bstack11l11111l_opy_):
      bstack11l1l1l1_opy_ = hostname
def bstack111ll1l11_opy_(url):
  return urlparse(url).hostname
def bstack11ll_opy_(hostname):
  for bstack111ll1_opy_ in bstack1l1l11lll_opy_:
    regex = re.compile(bstack111ll1_opy_)
    if regex.match(hostname):
      return True
  return False