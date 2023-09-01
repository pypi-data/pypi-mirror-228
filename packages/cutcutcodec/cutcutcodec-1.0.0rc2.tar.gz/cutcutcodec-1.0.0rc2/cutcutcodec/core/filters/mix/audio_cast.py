#!/usr/bin/env python3

"""
** Basic linear casts between different audio profiles. **
----------------------------------------------------------

For coefficient downmixing, based on https://www.rfc-editor.org/rfc/rfc7845#section-5.1.1.5
and http://www.atsc.org/wp-content/uploads/2015/03/A52-201212-17.pdf p96
"""

import numbers
import typing

from sympy.core.basic import Basic
from sympy.core.symbol import Symbol
import networkx
import numpy as np
import torch

from cutcutcodec.core.classes.frame_audio import FrameAudio
from cutcutcodec.core.classes.profile import AllProfiles, ProfileAudio




class LinearAudioConvertor:
    """
    ** Convertion of a specific profile thanks the transition matrix. **

    Parameters
    ----------
    in_profile : cutcutcodec.core.classes.profile.ProfileAudio
        The profile of the input frames (readonly).
    out_profile : cutcutcodec.core.classes.profile.ProfileAudio
        The profile of the converted frames (readonly).
    """

    def __init__(self,
        in_profile: ProfileAudio, out_profile: ProfileAudio, matrix: np.ndarray[np.float64]
    ):
        """
        Parameters
        ----------
        in_profile : cutcutcodec.core.classes.profile.ProfileAudio
            The profile of the input frames.
        out_profile : cutcutcodec.core.classes.profile.ProfileAudio
            The profile of the converted frames.
        matrix : array
            The linear transformation matrix.
        """
        assert isinstance(in_profile, ProfileAudio), in_profile.__class__.__name__
        assert isinstance(out_profile, ProfileAudio), out_profile.__class__.__name__
        assert isinstance(matrix, np.ndarray), matrix.__class__.__name__
        assert matrix.shape == (len(out_profile.channels), len(in_profile.channels))
        self._in_profile = in_profile
        self._out_profile = out_profile
        self._matrix = torch.from_numpy(matrix)

    def __call__(self, frame: FrameAudio) -> FrameAudio:
        """
        ** Apply the convertion of the audio frame. **

        Parameters
        ----------
        frame : cutcutcodec.core.classes.frame_audio.FrameAudio
            The input frame audio with the profile ``in_profile``.

        Returns
        -------
        cutcutcodec.core.classes.frame_audio.FrameAudio
            The input ``frame`` converted in the profile ``out_profile``.
        """
        assert isinstance(frame, FrameAudio), frame.__class__.__name__
        assert frame.profile == self._in_profile, (frame.profile, self._in_profile)
        out_frame = self._matrix.to(device=frame.device, dtype=frame.dtype) @ torch.Tensor(frame)
        out_frame = FrameAudio(frame.time, frame.rate, self._out_profile, out_frame)
        return out_frame

    @property
    def equations(self) -> dict[Symbol, Basic]:
        """
        ** To each output channel, associate the equation. **

        The symbols are the real cannonocal name of each channels.
        """
        in_vars = [Symbol(v, real=True) for v, _ in self._in_profile.channels]
        out_vars = [Symbol(v, real=True) for v, _ in self._out_profile.channels]
        eqs = self._matrix.numpy(force=True) @ np.array([in_vars], dtype=object).transpose()
        return dict(zip(out_vars, eqs[:, 0]))

    @property
    def in_profile(self) -> ProfileAudio:
        """
        ** The profile of the input frames. **
        """
        return self._in_profile

    @property
    def out_profile(self) -> ProfileAudio:
        """
        ** The profile of the converted frames. **
        """
        return self._out_profile



class AudioConvertor(LinearAudioConvertor):
    """
    ** Combine the matrix in order to find the complete transformation chain. **

    Examples
    --------
    >>> import torch
    >>> _ = torch.manual_seed(0)
    >>> from cutcutcodec.core.classes.frame_audio import FrameAudio
    >>> from cutcutcodec.core.filters.mix.audio_cast import AudioConvertor
    >>> frame_in = FrameAudio(0, 1, "5.1", torch.randn((6, 1024)))
    >>> (conv := AudioConvertor("5.1", "mono"))
    AudioConvertor('5.1', 'mono')
    >>> torch.round(conv(frame_in), decimals=3)
    FrameAudio(0, 1, 'mono', [[-0.296,  0.279, -0.775, ..., -2.045, -2.013, -0.316]])
    >>> torch.round(
    ...     AudioConvertor("stereo", "mono")(AudioConvertor("5.1", "stereo")(frame_in)), decimals=3
    ... )
    FrameAudio(0, 1, 'mono', [[-0.296,  0.279, -0.775, ..., -2.045, -2.013, -0.316]])
    >>>
    """

    def __init__(self,
        in_profile: typing.Union[ProfileAudio, str, numbers.Integral],
        out_profile: typing.Union[ProfileAudio, str, numbers.Integral],
    ):
        """
        Parameters
        ----------
        in_profile : cutcutcodec.core.classes.profile.ProfileAudio
            Casted and transmitted to
            ``cutcutcodec.core.filters.mix.audio_cast.LinearAudioConvert`` initialisator.
        out_profile : cutcutcodec.core.classes.profile.ProfileAudio
            Casted and transmitted to
            ``cutcutcodec.core.filters.mix.audio_cast.LinearAudioConvert`` initialisator.
        """
        in_profile, out_profile = ProfileAudio(in_profile), ProfileAudio(out_profile)

        # search the path
        graph = networkx.from_edgelist(
            (
                (p_in, p_out, {"matrix": matrix, "weight": 1.0})
                for (p_in, p_out), matrix in self.all_profiles().items()
            ),
            create_using=networkx.DiGraph,
        )
        try:
            path = networkx.dijkstra_path(graph, in_profile.name, out_profile.name, weight="weight")
        except ValueError as err:
            raise NotImplementedError(
                f"impossible convertion from {in_profile.name} to {out_profile.name}"
            ) from err

        # compute the matrix
        if len(path) == 1: # case identity
            path = [path[0], path[0]]
        matrix = np.array(graph.get_edge_data(path[0], path[1])["matrix"])
        for p_in, p_out in zip(path[1:-1], path[2:]):
            matrix = np.array(graph.get_edge_data(p_in, p_out)["matrix"]) @ matrix

        super().__init__(in_profile, out_profile, matrix)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"({repr(self._in_profile.name)}, {repr(self._out_profile.name)})"
        )

    @staticmethod
    def all_profiles() -> dict[tuple[str, str], list[list[float]]]:
        """
        ** To each profiles, associate the convertion matrix. **
        """
        downmixing = {
            ("stereo", "mono"): # 'fl', 'fr'
                [[0.500000, 0.500000]], # be carefull of phase inversion
            ("3.0", "stereo"): # 'fl', 'fr', 'fc'
                [[0.585786, 0.000000, 0.414214],
                 [0.000000, 0.585786, 0.414214]],
            ("quad", "stereo"): # 'fl', 'fr', 'bl', 'br'
                [[0.422650, 0.000000, 0.366025, 0.211325],
                 [0.000000, 0.422650, 0.211325, 0.366025]],
            ("5.0", "stereo"): # 'fl', 'fr', 'fc', 'bl', 'br'
                [[0.650802, 0.000000, 0.460186, 0.563611, 0.325401],
                 [0.000000, 0.650802, 0.460186, 0.325401, 0.563611]],
            ("5.1", "stereo"): # 'fl', 'fr', 'fc', 'lfe', 'bl', 'br'
                [[0.529067, 0.000000, 0.374107, 0.374107, 0.458186, 0.264534],
                 [0.000000, 0.529067, 0.374107, 0.374107, 0.264534, 0.458186]],
            ("6.1", "stereo"): # 'fl', 'fr', 'fc', 'lfe', 'bc', 'sl', 'sr'
                [[0.455310, 0.000000, 0.321953, 0.321953, 0.278819, 0.394310, 0.227655],
                 [0.000000, 0.455310, 0.321953, 0.321953, 0.278819, 0.227655, 0.394310]],
            ("7.1", "stereo"): # 'fl', 'fr', 'fc', 'lfe', 'bl', 'br', 'sl', 'sr'
                [[0.388631, 0.000000, 0.274804, 0.274804, 0.336565, 0.194316, 0.336565, 0.194316],
                 [0.000000, 0.388631, 0.274804, 0.274804, 0.194316, 0.336565, 0.194316, 0.336565]],
        }
        upmixing = {
            ("mono", "stereo"): # 'fc'
                [[1.000000],
                 [1.000000]],
        }
        identity = {
            (c, c): [[1.0 if d2 == d1 else 0.0 for d2 in d] for d1 in d]
            for c, d in AllProfiles().profiles.items()
        }
        return downmixing | upmixing | identity
