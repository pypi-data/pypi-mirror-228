#!/usr/bin/env python3

"""
** Allows you to temporarily translate a sequence. **
-----------------------------------------------------
"""

from fractions import Fraction
import numbers
import typing

import torch

from cutcutcodec.core.classes.filter import Filter
from cutcutcodec.core.classes.frame_audio import FrameAudio
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.classes.stream_audio import StreamAudioWrapper
from cutcutcodec.core.classes.stream_video import StreamVideoWrapper



class FilterDelay(Filter):
    """
    ** Change the beginning time of a stream. **

    Attributes
    ----------
    delay : Fraction
        The delay append to the original beginning time of the stream (readonly).
        a positive value indicates that the output flow is later than the input flow.

    Examples
    --------
    >>> from cutcutcodec.core.filters.basic.delay import FilterDelay
    >>> from cutcutcodec.core.generation.audio.noise import GeneratorAudioNoise
    >>> from cutcutcodec.core.generation.video.noise import GeneratorVideoNoise
    >>>
    >>> (s_base_audio,) = GeneratorAudioNoise(0).out_streams
    >>> (s_base_video,) = GeneratorVideoNoise(0).out_streams
    >>> s_trans_audio, s_trans_video = FilterDelay([s_base_audio, s_base_video], 10).out_streams
    >>>
    >>> (s_base_audio.snapshot(0) == s_trans_audio.snapshot(10)).all()
    tensor(True)
    >>> (s_base_video.snapshot(0, (1, 1)) == s_trans_video.snapshot(10, (1, 1))).all()
    tensor(True)
    >>> (s_base_audio.snapshot(10) == s_trans_audio.snapshot(10)).all()
    tensor(False)
    >>> (s_base_video.snapshot(10, (1, 1)) == s_trans_video.snapshot(10, (1, 1))).all()
    tensor(False)
    >>>
    """

    def __init__(self, in_streams: typing.Iterable[Stream], delay: numbers.Real):
        """
        Parameters
        ----------
        in_streams : typing.Iterable[Stream]
            Transmitted to ``cutcutcodec.core.classes.filter.Filter``.
        delay : numbers.Real
            The temporal translation value to apply at the output stream.
        """
        assert hasattr(in_streams, "__iter__"), in_streams.__class__.__name__
        in_streams = tuple(in_streams)
        assert all(isinstance(stream, Stream) for stream in in_streams), \
            [stream.__class__.__name__ for stream in in_streams]
        assert isinstance(delay, numbers.Real), delay.__class__.__name__

        self._delay = Fraction(delay)
        super().__init__(in_streams, in_streams)
        super().__init__(
            self.in_streams, # not in_stream without self because generator can be exausted
            [
                (
                    {"audio": _StreamAudioTranslate, "video": _StreamVideoTranslate}
                )[in_stream.type](self, index) for index, in_stream in enumerate(self.in_streams)
            ]
        )

    def _getstate(self) -> dict:
        return {"delay": str(self.delay)}

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert set(state) == {"delay"}, set(state)
        FilterDelay.__init__(self, in_streams, Fraction(state["delay"]))

    @classmethod
    def default(cls):
        return cls([], 0)

    @property
    def delay(self) -> Fraction:
        """
        ** The delay append to the original beginning time of the stream. **
        """
        return self._delay


class _StreamAudioTranslate(StreamAudioWrapper):
    """
    ** Translate an audio stream from a certain delay. **
    """

    def _snapshot(self, timestamp: Fraction, rate: int, samples: int) -> FrameAudio:
        frame = self.stream._snapshot(timestamp - self.node.delay, rate, samples)
        frame = FrameAudio(frame.time + self.node.delay, rate, frame.profile, frame)
        return frame

    @property
    def beginning(self) -> Fraction:
        return self.stream.beginning + self.node.delay


class _StreamVideoTranslate(StreamVideoWrapper):
    """
    ** Translate a video stream from a certain delay. **
    """

    def _snapshot(self, timestamp: Fraction, mask: torch.Tensor) -> torch.Tensor:
        return self.stream._snapshot(timestamp - self.node.delay, mask)

    @property
    def beginning(self) -> Fraction:
        return self.stream.beginning + self.node.delay
