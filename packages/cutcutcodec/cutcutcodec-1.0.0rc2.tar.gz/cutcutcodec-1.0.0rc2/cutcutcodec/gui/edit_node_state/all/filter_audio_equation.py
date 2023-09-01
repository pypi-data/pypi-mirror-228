#!/usr/bin/env python3

"""
** Properties of a ``cutcutcodec.core.filters.equation.FilterAudioEquation``. **
--------------------------------------------------------------------------------
"""


from qtpy import QtWidgets

from cutcutcodec.core.classes.profile import AllProfiles, ProfileAudio
from cutcutcodec.gui.edit_node_state.base import EditBase
from cutcutcodec.gui.edit_node_state.interface import Equationable, Profilable



class EditFilterAudioEquation(EditBase):
    """
    ** Allows to view and modify the properties of a node of type ``FilterAudioEquation``.
    """

    def __init__(self, parent, node_name):
        super().__init__(parent, node_name)
        self.signals = []
        self.re_symb = r"t|" + r"|".join(fr'{p}_\d+' for p in sorted(AllProfiles().individuals))

        self.grid_layout = QtWidgets.QGridLayout()
        self.signals_ref_span = Profilable(self)(self.grid_layout)
        self.init_signal(self.grid_layout, self.signals_ref_span)
        self.setLayout(self.grid_layout)

    def init_signal(self, grid_layout, ref_span=0):
        """
        ** Displays and allows to modify the signals. **
        """
        profile = ProfileAudio(self.state["profile"] or len(self.state["signals"]))
        self.state["signals"] += ["0"] * (len(profile.channels)-len(self.state["signals"])) # < 0 ok
        self.state["signals"] = self.state["signals"][:len(profile.channels)]
        for i, (channel, desc) in enumerate(profile.channels):
            self.signals.append(
                Equationable(self, (i, "signals"), f"{desc} ({channel}):", self.re_symb)
            )
        for equation in self.signals:
            equation(grid_layout, ref_span)
            ref_span += 1
        return ref_span + 1

    def reset(self):
        """
        ** Called by the signals interface. **
        """
        for signal in self.signals:
            signal.delete()
        self.signals = []
        self.init_signal(self.grid_layout, ref_span=self.signals_ref_span)
