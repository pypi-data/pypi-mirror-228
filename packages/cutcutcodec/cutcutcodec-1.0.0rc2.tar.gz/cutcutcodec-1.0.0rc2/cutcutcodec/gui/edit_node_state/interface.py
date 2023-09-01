#!/usr/bin/env python3

"""
** Allows you to avoid redundancy in the node editing windows. **
-----------------------------------------------------------------

Defines several accessors that allow to lighten the code of child classes.
This is also where methods common to several classes are implemented to avoid data redundancy.
"""

import math
import numbers
import re

from qtpy import QtWidgets

from cutcutcodec.core.classes.profile import AllProfiles, ProfileAudio
from cutcutcodec.core.compilation.parse import parse_to_number
from cutcutcodec.core.compilation.parse import parse_to_sympy
from cutcutcodec.gui.edit_node_state.base import EditBase



class Equationable:
    """
    ** Allows to manage a sympy equation field. **
    """

    def __init__(self, edit: EditBase, pos_state: tuple[int, str], label: str, re_symb=str):
        assert isinstance(edit, EditBase), edit.__class__.__name__
        assert isinstance(pos_state, tuple), pos_state.__class__.__name__
        assert len(pos_state) == 2, pos_state
        position, state = pos_state
        assert isinstance(position, int), position.__class__.__name__
        assert position >= 0, position
        assert isinstance(state, str), state
        assert state in edit.state
        assert isinstance(edit.state[state], list), edit.state.__class__.__name__
        assert isinstance(label, str), label.__class__.__name__
        assert isinstance(re_symb, str), re_symb.__class__.__name__
        if len(edit.state[state]) < position:
            edit.state[state].extend(["0"]*(position-len(edit.state[state])))
        self.edit = edit
        self.position = position
        self.state = state
        self.label = QtWidgets.QLabel(label)
        self.re_symb = re_symb
        self.textbox = QtWidgets.QLineEdit(edit)

    def __call__(self, grid_layout: QtWidgets.QGridLayout, ref_span=0):
        """
        ** Displays and allows to modify an equation field. **
        """
        assert isinstance(grid_layout, QtWidgets.QGridLayout), grid_layout.__class__.__name__
        grid_layout.addWidget(self.label, ref_span, 0)
        if len(self.edit.state[self.state]) > self.position:
            self.textbox.setText(str(self.edit.state[self.state][self.position]))
        self.textbox.textChanged.connect(self.validate)
        grid_layout.addWidget(self.textbox, ref_span, 1)
        return ref_span + 1

    def delete(self):
        """
        ** Delete the widgets. **
        """
        self.label.deleteLater()
        self.textbox.deleteLater()

    def validate(self, text):
        """
        ** Checks and updates the new equation. **
        """
        eqs = self.edit.state[self.state].copy()
        reset = False
        if text:
            try:
                expr = parse_to_sympy(text)
            except (SyntaxError, ZeroDivisionError):
                self.textbox.setStyleSheet("background:red;")
                return
            for symb in map(str, expr.free_symbols):
                if not re.fullmatch(self.re_symb, symb):
                    self.textbox.setStyleSheet("background:red;")
                    return
            if self.position == len(eqs):
                eqs.append(str(expr))
                reset = True
            else:
                eqs[self.position] = str(expr)
        elif len(eqs) - 1 == self.position:
            if self.position == 0:
                self.textbox.setStyleSheet("background:red;")
                return
            del eqs[self.position]
            reset = True
        else:
            self.textbox.setStyleSheet("background:red;")
            return

        self.edit.try_set_state(self.edit.get_new_state({self.state: eqs}), self.textbox)
        if reset:
            self.edit.reset()


class Numberable:
    """
    ** Allows to manage a number field to extract a fraction or or inf. **
    """

    def __init__(self,
        edit: EditBase,
        state: str,
        bounds: tuple[numbers.Real, numbers.Real]=(-math.inf, math.inf),
        isfinite: bool=False,
    ):
        assert isinstance(edit, EditBase), edit.__class__.__name__
        assert isinstance(state, str), state.__class__.__name__
        assert state in edit.state, f"{state} not in {sorted(edit.state)}"
        assert isinstance(bounds, tuple), bounds.__class__.__name__
        assert len(bounds) == 2, bounds
        assert isinstance(bounds[0], numbers.Real), bounds[0].__class__.__name__
        assert isinstance(bounds[1], numbers.Real), bounds[1].__class__.__name__
        assert bounds[0] < bounds[1], bounds
        assert isinstance(isfinite, bool), isfinite.__class__.__name__
        self.edit = edit
        self.edit.ref.append(self)
        self.state = state
        self.bounds = bounds
        self.isfinite = isfinite
        self.textbox = QtWidgets.QLineEdit(edit)

    def __call__(self, grid_layout: QtWidgets.QGridLayout, ref_span=0):
        """
        ** Displays and allows to modify the number field. **
        """
        assert isinstance(grid_layout, QtWidgets.QGridLayout), grid_layout.__class__.__name__
        grid_layout.addWidget(
            QtWidgets.QLabel(
                f"{self.state.replace('_', ' ').title()} "
                f"({self.bounds[0]} {'<=' if math.isfinite(self.bounds[0]) else '<'} "
                "number "
                f"{'<=' if math.isfinite(self.bounds[1]) else '<'} {self.bounds[1]}):",
                self.edit,
            ),
            ref_span,
            0,
        )
        self.textbox.setText(str(self.edit.state[self.state]))
        self.textbox.textChanged.connect(self.validate)
        grid_layout.addWidget(self.textbox, ref_span, 1)
        return ref_span + 1

    def validate(self, text):
        """
        ** Checks and updates the new number. **,
        """
        try:
            val = parse_to_number(text)
        except (ValueError, ZeroDivisionError):
            self.textbox.setStyleSheet("background:red;")
            return
        if val < self.bounds[0] or val > self.bounds[1]:
            self.textbox.setStyleSheet("background:red;")
            return
        if self.isfinite and not math.isfinite(val):
            self.textbox.setStyleSheet("background:red;")
            return

        self.edit.try_set_state(self.edit.get_new_state({self.state: str(val)}), self.textbox)


class Profilable:
    """
    ** Allows to select an audio profile. **
    """

    def __init__(self, edit: EditBase):
        assert isinstance(edit, EditBase), edit.__class__.__name__
        assert "profile" in edit.state, sorted(edit.state)
        self.edit = edit
        self.edit.ref.append(self)
        self.combobox = QtWidgets.QComboBox(edit)

    def __call__(self, grid_layout: QtWidgets.QGridLayout, ref_span=0):
        """
        ** Displays and allows to select the profile field. **
        """
        assert isinstance(grid_layout, QtWidgets.QGridLayout), grid_layout.__class__.__name__
        grid_layout.addWidget(QtWidgets.QLabel("Audio Profile:", self.edit), ref_span, 0)
        self.combobox.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.combobox.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.InsertAtBottom)

        self.combobox.addItem("default")
        profiles = AllProfiles().profiles
        defaults = (
            {ProfileAudio(nb_channels).name for nb_channels in set(map(len, profiles.values()))}
        )
        for profile in sorted(profiles, key=lambda p: (len(profiles[p]), (p not in defaults), p)):
            if profile in defaults:
                item = (
                    f'{len(profiles[profile])} channels default "{profile}" '
                    f"({'+'.join(profiles[profile])})"
                )
            else:
                item = (
                    f'{len(profiles[profile])} channels "{profile}" ({"+".join(profiles[profile])})'
                )
            self.combobox.addItem(item)
            if self.edit.state["profile"] == profile:
                self.combobox.setCurrentText(item)
        self.combobox.currentTextChanged.connect(self.validate)

        grid_layout.addWidget(self.combobox, ref_span, 1)
        return ref_span + 1

    def validate(self, text):
        """
        ** Checks and updates the audio layout. **,
        """
        old_profile = self.edit.state["profile"]
        new_profile = None if text == "default" else re.search(r'".+"', text).group()[1:-1]
        if new_profile != old_profile:
            self.edit.state["profile"] = new_profile
            self.edit.reset()

class Seedable:
    """
    ** Allows to manage a `seed` field. **

    It is a float between [0, 1[.
    """

    def __init__(self, edit: EditBase):
        assert isinstance(edit, EditBase), edit.__class__.__name__
        assert "seed" in edit.state, sorted(edit.state)
        self.edit = edit
        self.edit.ref.append(self)
        self.textbox = QtWidgets.QLineEdit(edit)

    def __call__(self, grid_layout: QtWidgets.QGridLayout, ref_span=0):
        """
        ** Displays and allows to modify the seed field. **
        """
        assert isinstance(grid_layout, QtWidgets.QGridLayout), grid_layout.__class__.__name__
        grid_layout.addWidget(QtWidgets.QLabel("Seed (0 <= float < 1):", self.edit), ref_span, 0)
        self.textbox.setText(str(self.edit.state["seed"]))
        self.textbox.textChanged.connect(self.validate)
        grid_layout.addWidget(self.textbox, ref_span, 1)
        return ref_span + 1

    def validate(self, text):
        """
        ** Checks and updates the new seed. **,
        """
        try:
            seed = float(text)
        except ValueError:
            self.textbox.setStyleSheet("background:red;")
            return
        if seed < 0 or seed >= 1:
            self.textbox.setStyleSheet("background:red;")
            return

        self.edit.try_set_state(self.edit.get_new_state({"seed": seed}), self.textbox)
