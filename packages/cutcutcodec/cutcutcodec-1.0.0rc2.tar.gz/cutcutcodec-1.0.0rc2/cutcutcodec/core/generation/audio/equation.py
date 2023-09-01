#!/usr/bin/env python3

"""
** Allows to generate sound from mathematical functions. **
------------------------------------------------------------
"""

import numbers
import typing

from sympy.core.basic import Basic

from cutcutcodec.core.classes.container import ContainerInput
from cutcutcodec.core.classes.profile import ProfileAudio
from cutcutcodec.core.filters.equation import FilterAudioEquation




class GeneratorAudioEquation(FilterAudioEquation, ContainerInput):
    """
    ** Generate an audio stream whose channels are defened by any equations. **

    It is a particular case of ``cutcutcodec.core.filter.equation.FilterAudioEquation``.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.generation.audio.equation import GeneratorAudioEquation
    >>> (stream,) = GeneratorAudioEquation("sin(2*pi*440*t)").out_streams
    >>> torch.round(stream.snapshot(0, 3520, 8), decimals=3)
    FrameAudio(0, 3520, 'mono', [[ 0.,     0.707,  1.,     0.707,  0.,    -0.707, -1.,    -0.707]])
    >>>
    """

    def __init__(self,
        *signals: typing.Union[Basic, numbers.Real, str],
        profile: typing.Union[ProfileAudio, str, numbers.Integral]=None,
    ):
        """
        Parameters
        ----------
        *signals : str or sympy.Basic
            Transmitted to ``cutcutcodec.core.filters.equation.FilterAudioEquation`` initialisator.
            But the only available vars is `t`.
        profile: cutcutcodec.core.classes.profile.ProfileAudio or str or int, optional
            Transmitted to ``cutcutcodec.core.filters.equation.FilterAudioEquation`` initialisator.
        """
        FilterAudioEquation.__init__(self, [], *signals, profile=profile)
        ContainerInput.__init__(self, self.out_streams)
        if excess := set(map(str, self._free_symbs)) - {"t"}:
            raise ValueError(f"only t symbol is allowed, not {excess}")

    @classmethod
    def default(cls):
        return cls(0)
