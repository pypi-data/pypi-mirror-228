#!/usr/bin/env python3

"""
** Defines the structure an audio frame. **
-------------------------------------------
"""

from fractions import Fraction
import numbers
import re
import typing

import torch

from cutcutcodec.core.classes.frame import Frame
from cutcutcodec.core.classes.profile import ProfileAudio



class FrameAudio(Frame):
    """
    ** An audio sample packet with time information. **

    Behaves like a torch tensor of shape (nbr_channels, samples).
    The shape is consistent with pyav and torchaudio.
    Values are supposed to be between -1 and 1.

    Attributes
    ----------
    channels : int
        The numbers of channels (readonly).
        For more informations about each channels, let see ``self.profile``.
    profile : cutcutcodec.core.classes.profile.ProfileAudio
        The signification of each channels (readonly).
    rate : int
        The frequency of the samples in Hz (readonly).
    samples : int
        The number of samples per channels (readonly).
    time : Fraction
        The time of the first sample of the frame in second (readonly).
    """

    def __new__(cls,
        time: typing.Union[Fraction, numbers.Real, str],
        rate: numbers.Integral,
        profile: typing.Union[ProfileAudio, str, numbers.Integral],
        *args,
        **kwargs,
    ):
        """
        Parameters
        ----------
        time : Fraction
            The time of the first sample of the frame in second.
        rate : int
            The frequency of the samples in Hz.
        profile : cutcutcodec.core.classes.profile.ProfileAudio or str or numbers.Integral
            The canonical name of the profile,
            let see ``cutcutcodec.core.classes.profile.ProfileAudio`` for the available profiles.
        *args : tuple
            Transmitted to ``cutcutcodec.core.classes.frame.Frame`` initialisator.
        **kwargs : dict
            Transmitted to ``cutcutcodec.core.classes.frame.Frame`` initialisator.
        """
        frame = super().__new__(cls, *args, metadata=[time, rate, profile], **kwargs)
        frame.check_state()
        return frame

    def __repr__(self) -> str:
        """
        ** Compact and complete display of an evaluable version of the audio frame. **

        Examples
        --------
        >>> import torch
        >>> from cutcutcodec.core.classes.frame_audio import FrameAudio
        >>>
        >>> FrameAudio("2/4", 48000, "stereo", torch.zeros((2, 1024)))
        FrameAudio('1/2', 48000, 'stereo', [[0., 0., 0., ..., 0., 0., 0.]
                                            [0., 0., 0., ..., 0., 0., 0.]])
        >>> _.to(dtype=torch.float16)
        FrameAudio('1/2', 48000, 'stereo', [[0., 0., 0., ..., 0., 0., 0.]
                                            [0., 0., 0., ..., 0., 0., 0.]],
                                           dtype=torch.float16)
        >>> _.requires_grad = True
        >>> _
        FrameAudio('1/2', 48000, 'stereo', [[0., 0., 0., ..., 0., 0., 0.]
                                            [0., 0., 0., ..., 0., 0., 0.]],
                                           dtype=torch.float16,
                                           requires_grad=True)
        >>>
        """
        tensor_str = re.sub(r"(?!^)(\d|\.) ", r"\1, ", str(self.numpy(force=True))) # insert ","
        time_str = f"'{self.time}'" if int(self.time) != self.time else f"{self.time}"
        header = f"{self.__class__.__name__}({time_str}, {self.rate}, {repr(self.profile.name)}, "
        tensor_str = ("\n" + " "*len(header)).join(tensor_str.split("\n"))
        if (infos := re.findall(r"\w+=[a-zA-Z0-9_\-.\"']+", torch.Tensor.__repr__(self))):
            infos = "\n" + " "*len(header) + (",\n" + " "*len(header)).join(infos)
            return f"{header}{tensor_str},{infos})"
        return f"{header}{tensor_str})"

    def check_state(self) -> None:
        """
        ** Apply verifications. **

        Raises
        ------
        AssertionError
            If something wrong in this frame.
        """
        assert isinstance(self.metadata[0], (Fraction, numbers.Real, str)), \
            self.metadata[0].__class__.__name__ # corresponds to time attribute
        self.metadata[0] = Fraction(self.metadata[0])
        assert isinstance(self.metadata[1], numbers.Integral), \
            self.metadata[1].__class__.__name__ # corresponds to rate attribute
        self.metadata[1] = int(self.metadata[1])
        assert self.metadata[1] > 0, self.metadata[1] # corresponds to rate attribute
        assert isinstance(self.metadata[2], (ProfileAudio, str,  numbers.Integral)), \
            self.metadata[2].__class__.__name__ # corresponds to the profile
        if isinstance(self.metadata[2], (str, numbers.Integral)):
            self.metadata[2] = ProfileAudio(self.metadata[2])
        assert self.ndim == 2, self.shape
        assert self.shape[0] == len(self.metadata[2].channels), self.shape # nbr_channels
        assert self.dtype.is_floating_point, self.dtype

    @property
    def profile(self) -> ProfileAudio:
        """
        ** The signification of each channels. **

        Examples
        --------
        >>> from cutcutcodec.core.classes.frame_audio import FrameAudio
        >>> FrameAudio(0, 48000, "stereo", 2, 10).profile
        ProfileAudio('stereo')
        >>>
        """
        return self.metadata[2]

    @property
    def rate(self) -> int:
        """
        ** The frequency of the samples in Hz. **

        Examples
        --------
        >>> from cutcutcodec.core.classes.frame_audio import FrameAudio
        >>> FrameAudio(0, 48000, "stereo", 2, 1024).rate
        48000
        >>>
        """
        return self.metadata[1]

    @property
    def samples(self) -> int:
        """
        ** The number of samples per channels. **

        Examples
        --------
        >>> from cutcutcodec.core.classes.frame_audio import FrameAudio
        >>> FrameAudio(0, 48000, "stereo", 2, 1024).samples
        1024
        >>>
        """
        return self.shape[1]

    @property
    def time(self) -> Fraction:
        """
        ** The time of the first sample of the frame in second. **

        Examples
        --------
        >>> from cutcutcodec.core.classes.frame_audio import FrameAudio
        >>> FrameAudio(0, 48000, "stereo", 2, 1024).time
        Fraction(0, 1)
        >>>
        """
        return self.metadata[0]
