#!/usr/bin/env python3

"""
** Properties of a ``cutcutcodec.core.filter.basic.meta.subclip.FilterSubclip``. **
-----------------------------------------------------------------------------------
"""

import math

from qtpy import QtWidgets

from cutcutcodec.gui.edit_node_state.base import EditBase
from cutcutcodec.gui.edit_node_state.interface import Numberable



class EditFilterSubclip(EditBase):
    """
    ** Allows to view and modify the properties of a filter of type ``FilterSubclip``.
    """

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)
        grid_layout = QtWidgets.QGridLayout()
        ref_span = Numberable(self, "delay", (0, math.inf), isfinite=True)(grid_layout)
        Numberable(self, "duration_max", (0, math.inf), isfinite=False)(grid_layout, ref_span)
        self.setLayout(grid_layout)
