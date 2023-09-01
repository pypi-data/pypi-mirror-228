#!/usr/bin/env python3

"""
** Selects a time slice of the stream. **
-----------------------------------------
"""

from fractions import Fraction
import math
import numbers
import typing

from cutcutcodec.core.classes.meta_filter import MetaFilter
from cutcutcodec.core.classes.node import Node
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.compilation.parse import parse_to_number
from cutcutcodec.core.filters.basic.cut import FilterCut
from cutcutcodec.core.filters.basic.identity import FilterIdentity



class FilterSubclip(MetaFilter):
    """
    ** Extract a segment from the stream. **

    It is a particular case of ``cutcutcodec.core.filters.basic.cut.FilterCut``.
    Allows to start a flow after the beginning and or finish it before the end.

    Attributes
    ----------
    delay : Fraction
        The offset from the parent stream (readonly).
    duration_max : Fraction or inf
        The maximum duration beyond which the flows do not return anything (readonly).

    Examples
    --------
    >>> from cutcutcodec.core.filters.basic.meta.subclip import FilterSubclip
    >>> from cutcutcodec.core.generation.audio.noise import GeneratorAudioNoise
    >>> from cutcutcodec.core.generation.video.noise import GeneratorVideoNoise
    >>>
    >>> (s_audio,) = GeneratorAudioNoise(0).out_streams
    >>> (s_video,) = GeneratorVideoNoise(0).out_streams
    >>> s_subclip_audio, s_subclip_video = FilterSubclip([s_audio, s_video], 10, 20).out_streams
    >>>
    >>> s_subclip_audio.beginning
    Fraction(10, 1)
    >>> s_subclip_audio.duration
    Fraction(20, 1)
    >>> s_subclip_video.beginning
    Fraction(10, 1)
    >>> s_subclip_video.duration
    Fraction(20, 1)
    >>>
    """

    def __init__(self,
        in_streams: typing.Iterable[Stream],
        delay: numbers.Real=Fraction(0),
        duration_max: numbers.Real=math.inf,
    ):
        """
        Parameters
        ----------
        in_streams : typing.Iterable[Stream]
            Transmitted to ``cutcutcodec.core.classes.filter.Filter``.
        delay: numbers.Real, default=0
            The time lapse from the parent stream.
            0 means that the beginning of the new stream coincides
            with the beginning of the stream that arrives at this node.
            A delay of x >= 0 seconds means that
            the first x seconds of the stream arriving on this filter are discarded.
        duration_max : numbers.Real, default=inf
            The maximal duration of the new stream.
        """
        assert isinstance(delay, numbers.Real), delay.__class__.__name__
        assert math.isfinite(delay), delay
        assert delay >= 0, delay
        assert isinstance(duration_max, numbers.Real), duration_max.__class__.__name__
        assert duration_max > 0, duration_max
        self._delay = Fraction(delay)
        self._duration_max = Fraction(duration_max) if math.isfinite(duration_max) else duration_max
        super().__init__(in_streams)

    def _compile(self, in_streams: tuple[Stream]) -> Node:
        if self.delay:
            if math.isfinite(self.duration_max):
                trunc_streams = (
                    FilterCut(in_streams, self.delay, self.delay+self.duration_max)
                    .out_streams[len(in_streams):2*len(in_streams)]
                )
            else:
                trunc_streams = FilterCut(in_streams, self.delay).out_streams[len(in_streams):]
        else:
            if math.isfinite(self.duration_max):
                trunc_streams = FilterCut(
                    in_streams, self.delay+self.duration_max
                ).out_streams[:len(in_streams)]
            else:
                trunc_streams = in_streams
        return FilterIdentity(trunc_streams)

    def _getstate(self) -> dict:
        return {"delay": str(self.delay), "duration_max": str(self.duration_max)}

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert set(state) == {"delay", "duration_max"}, set(state)
        FilterSubclip.__init__(self,
            in_streams, Fraction(state["delay"]), parse_to_number(state["duration_max"])
        )

    @classmethod
    def default(cls):
        return cls([], 0, math.inf)

    @property
    def delay(self) -> Fraction:
        """
        ** The offset from the parent stream. **
        """
        return self._delay

    @property
    def duration_max(self) -> Fraction:
        """
        ** The maximum duration beyond which the flows do not return anything. **
        """
        return self._duration_max
