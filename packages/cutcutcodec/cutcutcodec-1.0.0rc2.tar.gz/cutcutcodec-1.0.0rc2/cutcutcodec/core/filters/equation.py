#!/usr/bin/env python3

"""
** Allows to filter independentely each audio and video samples by any equation. **
-----------------------------------------------------------------------------------
"""

from fractions import Fraction
import math
import numbers
import re
import typing

from sympy.core.basic import Basic
from sympy.core.containers import Tuple
from sympy.core.numbers import Zero
from sympy.core.symbol import Symbol
import torch

from cutcutcodec.core.classes.filter import Filter
from cutcutcodec.core.classes.frame_audio import FrameAudio
from cutcutcodec.core.classes.profile import AllProfiles
from cutcutcodec.core.classes.profile import ProfileAudio
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.classes.stream_audio import StreamAudio
from cutcutcodec.core.classes.stream_video import StreamVideo
from cutcutcodec.core.compilation.parse import parse_to_sympy
from cutcutcodec.core.compilation.sympy_to_torch import Lambdify
from cutcutcodec.core.exceptions import OutOfTimeRange



class FilterAudioEquation(Filter):
    """
    ** Apply any equation on each channels. **

    The relation can not mix differents timestamps (no convolution).

    Attributes
    ----------
    profile : cutcutcodec.core.classes.profile.ProfileAudio
        The signification of each channels (readonly).
    signals : list[sympy.core.expr.Expr]
        The amplitude expression of the differents channels (readonly).

    Examples
    --------
    >>> from cutcutcodec.core.filters.equation import FilterAudioEquation
    >>> from cutcutcodec.core.generation.audio.noise import GeneratorAudioNoise
    >>> (stream_in,) = GeneratorAudioNoise(0).out_streams
    >>> stream_in.snapshot(0, 48000, 4)
    FrameAudio(0, 48000, 'stereo', [[-0.92382674,  0.02767801, -0.44544228,  0.98969342]
                                    [ 0.52793658, -0.98823813, -0.84168343, -0.46822516]],
                                   dtype=torch.float64)
    >>> (stream_out,) = FilterAudioEquation([stream_in], "fl_0 + t", "fl_0 + fr_0").out_streams
    >>> stream_out.snapshot(0, 48000, 4)
    FrameAudio(0, 48000, 'stereo', [[-0.92382675,  0.02769884, -0.44540063,  0.9897559, ]
                                    [-0.39589015, -0.96056014, -1.,          0.5214683, ]])
    >>>
    """

    def __init__(self,
        in_streams: typing.Iterable[StreamAudio],
        *signals: typing.Union[Basic, numbers.Real, str],
        profile: typing.Union[ProfileAudio, str, numbers.Integral]=None,
    ):
        """
        Parameters
        ----------
        in_streams : typing.Iterable[Stream]
            Transmitted to ``cutcutcodec.core.classes.filter.Filter``.
        *signals : str or sympy.Basic
            The amplitude function of each channel respectively.
            The channels are interpreted like is describe in
            ``cutcutcodec.core.classes.frame_audio.FrameAudio``.
            The number of expressions correspond to the number of channels.
            The return values will be cliped to stay in the range [-1, 1].
            If the expression gives a complex, the real part is taken.
            The variables that can be used in these functions are the following:

                * t : The time in seconds since the beginning of the audio.
                * x_i : With `x` any channels available
                    for ``cutcutcodec.core.classes.profile.ProfileAudio.channels``
                    and `i` the stream index, i starts from 0 included.
                    examples: `fl_0` for front left of the stream 0.
        profile: cutcutcodec.core.classes.profile.ProfileAudio or str or int, optional
            The audio profile to associate to each equation,
            let see ``cutcutcodec.core.classes.profile.ProfileAudio`` for more details.
            By default, the profile is automaticaly detected from the number of equations.
        """
        # check
        assert hasattr(in_streams, "__iter__"), in_streams.__class__.__name__
        in_streams = tuple(in_streams)
        assert all(isinstance(s, StreamAudio) for s in in_streams), in_streams
        assert all(isinstance(s, (Basic, numbers.Real, str)) for s in signals), signals
        assert profile is None or isinstance(profile, (ProfileAudio, str,  numbers.Integral)), \
            profile.__class__.__name__

        # initialisation
        self._signals = [
            parse_to_sympy(s, symbols={"t": Symbol("t", real=True, positive=True)})
            for s in signals
        ]
        Filter.__init__(self, in_streams, in_streams)

        if not self.in_streams and not self._signals:
            self._free_symbs = set()
            self._profile = None
            return
        self._signals = self._signals or [Zero()]
        self._free_symbs = set.union(*(c.free_symbols for c in self._signals))
        self._profile = ProfileAudio(profile if profile is not None else len(self._signals))
        assert len(self._profile.channels) == len(self._signals)

        # check
        pattern = r"t|" + r"|".join(fr'{p}_\d+' for p in sorted(AllProfiles().individuals))
        if excess := {s for s in self._free_symbs if re.fullmatch(pattern, str(s)) is None}:
            raise ValueError(f"the vars {excess} not match the required format")
        symbs = (
            [re.fullmatch(r"(?P<channel>[a-z]+)(?P<index>\d+)", str(s)) for s in self._free_symbs]
        )
        if excess := (
            {s["channel"] for s in symbs if s is not None} - set(AllProfiles().individuals)
        ):
            raise ValueError(f"the vars {excess} are not in {set(AllProfiles().individuals)}")
        if excess := {int(s["index"]) for s in symbs if s is not None}:
            raise ValueError(f"only {len(self.in_streams)} input stream, {excess} is not reachable")

        Filter.__init__(self, self.in_streams, [_StreamAudioEquation(self)])

    def _getstate(self) -> dict:
        return {
            "signals": [str(c) for c in self._signals],
            "profile": (self._profile.name if self._profile is not None else None),
        }

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert set(state) == {"signals", "profile"}, set(state)
        FilterAudioEquation.__init__(self, in_streams, *state["signals"], profile=state["profile"])

    @property
    def profile(self) -> ProfileAudio:
        """
        ** The signification of each channels. **
        """
        return self._profile

    @property
    def signals(self) -> list[Basic]:
        """
        ** The amplitude expression of the differents channels. **
        """
        return self._signals.copy()

    @classmethod
    def default(cls):
        return cls([])

    @property
    def free_symbols(self) -> set[Symbol]:
        """
        ** The set of the diferents used symbols. **
        """
        return self._free_symbs.copy()


class FilterVideoEquation(Filter):
    """
    ** Apply any equation on each pixels. **

    The relation is only between the pixel at the same timestamp at the same position.

    Attributes
    ----------
    colors : list[sympy.core.expr.Expr]
        The luminosity expression of the differents channels (readonly).

    Examples
    --------
    >>> from cutcutcodec.core.filters.equation import FilterVideoEquation
    >>> from cutcutcodec.core.generation.video.noise import GeneratorVideoNoise
    >>> (stream_in,) = GeneratorVideoNoise(0).out_streams
    >>> (stream_out,) = FilterVideoEquation([stream_in], "b0", "(b0+g0+r0)/3", "0").out_streams
    >>> stream_in.snapshot(0, (2, 2))
    FrameVideo(0, [[[127, 101, 236]
                    [ 38,  57, 254]]
    <BLANKLINE>
                   [[184,  95, 125]
                    [235,   3, 208]]])
    >>> stream_out.snapshot(0, (2, 2))
    FrameVideo(0, [[[127, 155,   0]
                    [ 38, 116,   0]]
    <BLANKLINE>
                   [[184, 135,   0]
                    [235, 148,   0]]])
    >>>
    """

    def __init__(self,
        in_streams: typing.Iterable[StreamVideo], *colors: typing.Union[Basic, numbers.Real, str]
    ):
        """
        Parameters
        ----------
        in_streams : typing.Iterable[Stream]
            Transmitted to ``cutcutcodec.core.classes.filter.Filter``.
        *colors : str or sympy.Basic
            The brightness of the color channels.
            The channels are interpreted like is describe in
            ``cutcutcodec.core.classes.frame_video.FrameVideo``.
            The return values will be cliped to stay in the range [0, 1].
            The value is 0 for min brightness and 1 for the max.
            If the expression gives a complex, the module is taken.
            The variables that can be used in these functions are the following:

                * i : The relative position along the vertical axis (numpy convention).
                    This value evolves between -1 and 1.
                * j : The relative position along the horizontal axis (numpy convention).
                    This value evolves between -1 and 1.
                * t : The time in seconds since the beginning of the video.
                * bi: The blue channel of the stream index i, i starts from 0 included.
                    This value evolves between 0 (dark) and 1 (light).
                * gi: The green channel of the stream index i, i starts from 0 included.
                    This value evolves between 0 (dark) and 1 (light).
                * ri: The red channel of the stream index i, i starts from 0 included.
                    This value evolves between 0 (dark) and 1 (light).
                * ai: The alpha channel of the stream index i, i starts from 0 included.
                    This value evolves between 0 (transparent) and 1 (blind).
        """
        # check
        assert hasattr(in_streams, "__iter__"), in_streams.__class__.__name__
        in_streams = tuple(in_streams)
        assert all(isinstance(s, StreamVideo) for s in in_streams), in_streams
        assert all(isinstance(c, (Basic, numbers.Real, str)) for c in colors), colors
        assert len(colors) <= 4, len(colors)

        # initialisation
        self._colors = [
            parse_to_sympy(
                c,
                symbols={
                    "t": Symbol("t", real=True, positive=True),
                    "i": Symbol("i", real=True),
                    "j": Symbol("j", real=True),
                }
            )
            for c in colors
        ]
        Filter.__init__(self, in_streams, in_streams)
        if not self.in_streams and not self._colors:
            self._free_symbs = set()
            return
        self._colors = self._colors or [Zero()]
        self._free_symbs = set.union(*(c.free_symbols for c in self._colors))

        # check
        if excess := (
            {s for s in self._free_symbs if re.fullmatch(r"i|j|t|[bgra]\d+", str(s)) is None}
        ):
            raise ValueError(f"only i, j, t, bi, gi, ri and ai symbols are allowed, not {excess}")
        if excess := (
            {
                s for s in self._free_symbs
                if re.fullmatch(r"[bgra]\d+", str(s)) is not None
                and int(str(s)[1:]) >= len(self.in_streams)
            }
        ):
            raise ValueError(f"only {len(self.in_streams)} input stream, {excess} is not reachable")

        Filter.__init__(self, self.in_streams, [_StreamVideoEquation(self)])

    def _getstate(self) -> dict:
        return {"colors": [str(c) for c in self.colors]}

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert set(state) == {"colors"}, set(state)
        FilterVideoEquation.__init__(self, in_streams, *state["colors"])

    @property
    def colors(self) -> list[Basic]:
        """
        ** The luminosity expression of the differents channels. **
        """
        return self._colors.copy()

    @classmethod
    def default(cls):
        return cls([])

    @property
    def free_symbols(self) -> set[Symbol]:
        """
        ** The set of the diferents used symbols. **
        """
        return self._free_symbs.copy()


class _StreamAudioEquation(StreamAudio):
    """
    ** Channels field parameterized by time and incoming samples. **
    """

    is_time_continuous = True

    def __init__(self, node: FilterAudioEquation):
        assert isinstance(node, FilterAudioEquation), node.__class__.__name__
        super().__init__(node)
        self._signals_func = None # cache

    def _get_signals_func(self) -> callable:
        """
        ** Allows to "compile" equations at the last moment. **
        """
        if self._signals_func is None:
            self._signals_func = Lambdify(self.node.signals, copy=True)
        return self._signals_func

    def _get_inputs(self,
        timestamp: Fraction, rate: int, samples: int
    ) -> dict[str, typing.Union[float, torch.Tensor]]:
        """
        ** Help for getting input vars. **
        """
        symbs = {}
        in_frames = {} # cache
        for symb in self.node.free_symbols:
            symb = str(symb)
            if symb == "t":
                time_field = torch.arange(samples, dtype=int) # not float for avoid round mistakes
                time_field = time_field.to(dtype=torch.float64, copy=False)
                time_field /= float(rate)
                time_field += float(timestamp)
                symbs["t"] = time_field # 1d vect
                continue
            match = re.fullmatch(r"(?P<channel>[a-z]+)_(?P<index>\d+)", symb)
            if (stream_index := int(match["index"])) not in in_frames:
                in_frames[stream_index] = (
                    self.node.in_streams[stream_index]._snapshot(timestamp, rate, samples)
                )
            try:
                channel_index = (
                    [n for n, _ in self.node.in_streams[stream_index].profile.channels]
                    .index(match["channel"])
                )
            except ValueError as err:
                raise NotImplementedError(
                    f"symbol {match['channel']} not allowed, "
                    f"only {self.node.in_streams[stream_index].profile.channels} are allowed"
                ) from err
            symbs[symb] = in_frames[stream_index][channel_index, :] # 1d vect
        return symbs

    def _snapshot(self, timestamp: Fraction, rate: int, samples: int) -> FrameAudio:
        # verif
        if timestamp < 0:
            raise OutOfTimeRange(f"there is no audio frame at timestamp {timestamp} (need >= 0)")

        # calculation
        signals = self._get_signals_func()(**self._get_inputs(timestamp, rate, samples))

        # correction + cast
        frame = FrameAudio(
            timestamp,
            rate,
            self.node.profile,
            torch.empty((len(self.node.signals), samples), dtype=torch.float32),
        )
        for i, signal in enumerate(signals):
            if signal.dtype.is_complex:
                signal = torch.real(signal)
            torch.nan_to_num(signal, nan=0.0, posinf=1.0, neginf=-1.0, out=signal)
            torch.clip(signal, -1.0, 1.0, out=signal)
            frame[i, :] = signal

        return frame

    @property
    def beginning(self) -> Fraction:
        index = [re.fullmatch(r"[a-z]+(?P<index>\d+)", str(s)) for s in self.node.free_symbols]
        index = {int(i["index"]) for i in index if i is not None}
        return min((self.node.in_streams[i].beginning for i in index), default=Fraction(0))

    @property
    def duration(self) -> typing.Union[Fraction, float]:
        index = [re.fullmatch(r"[a-z]+(?P<index>\d+)", str(s)) for s in self.node.free_symbols]
        index = {int(i["index"]) for i in index if i is not None}
        streams = (self.node.in_streams[i] for i in index)
        end = max((s.beginning + s.duration for s in streams), default=math.inf)
        return end - self.beginning

    @property
    def profile(self) -> ProfileAudio:
        return self.node.profile


class _StreamVideoEquation(StreamVideo):
    """
    ** Color field parameterized by time, position and incoming pixels. **
    """

    is_space_continuous = True
    is_time_continuous = True

    def __init__(self, node: FilterVideoEquation):
        assert isinstance(node, FilterVideoEquation), node.__class__.__name__
        super().__init__(node)
        self._colors_func = None # cache
        self._fields = None # cache
        self._fileds_mask = None

    def _get_colors_func(self) -> callable:
        """
        ** Allows to "compile" equations at the last moment. **
        """
        if self._colors_func is None:
            free_symbs = Tuple(*self.node.colors).free_symbols
            cst_args = {s for s in free_symbs if str(s) in {"i, j"}}
            if (shapes := {s for s in free_symbs if str(s) != "t"}):
                shapes = sorted(shapes, key=str)
                shapes = {s: shapes[0] for s in shapes[1:]}
            else:
                shapes = None
            self._colors_func = Lambdify(
                self.node.colors,
                cst_args=cst_args,
                shapes=shapes,
                copy=True,
            )
        return self._colors_func

    def _get_fields(self, mask: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """
        ** Returns the i and j field, minimising realloc by cache. **

        Returns a new copy each time.
        """
        height, width = mask.shape
        if self._fields is None or self._fields[0].shape != (height, width):
            self._fields = torch.meshgrid(
                torch.linspace(-1, 1, height, dtype=torch.float32),
                torch.linspace(-1, 1, width, dtype=torch.float32),
                indexing="ij",
            )
        if self._fileds_mask is None or mask.numpy(force=True).tobytes() != self._fileds_mask[2]:
            self._fileds_mask = (
                self._fields[0][mask], self._fields[1][mask], mask.numpy(force=True).tobytes()
            )
        return (self._fileds_mask[0], self._fileds_mask[1])

    def _get_inputs(self,
        timestamp: Fraction, mask: torch.Tensor
    ) -> dict[str, typing.Union[float, torch.Tensor]]:
        """
        ** Help for getting input vars. **
        """
        symbs = {}
        in_frames = {} # cache
        for symb in self.node.free_symbols:
            symb = str(symb)
            if (func := {
                "i": lambda: self._get_fields(mask)[0],
                "j": lambda: self._get_fields(mask)[1],
                "t": lambda: float(timestamp),
            }.get(symb, None)) is not None:
                symbs[symb] = func()
                continue
            stream_index = int(symb[1:])
            if stream_index not in in_frames:
                in_frames[stream_index] = self._frame_to_float(
                    self.node.in_streams[stream_index]._snapshot(timestamp, mask)
                )
            frame = in_frames[stream_index]
            if symb[0] in {"b", "g", "r"}:
                if frame.shape[2] in {1, 2}:
                    symbs[symb] = frame[..., 0][mask]
                else:
                    symbs[symb] = frame[..., {"b": 0, "g": 1, "r": 2}[symb[0]]][mask]
            elif symb[0] == "a":
                if frame.shape[2] in {2, 4}:
                    symbs[symb] = frame[..., -1][mask]
                else:
                    symbs[symb] = 1.0
            else:
                raise NotImplementedError(f"only i, j, t, b, g, r and are allowed, not {symb}")
        return symbs

    def _snapshot(self, timestamp: Fraction, mask: torch.Tensor) -> torch.Tensor:
        # verif
        if timestamp < 0:
            raise OutOfTimeRange(f"there is no video frame at timestamp {timestamp} (need >= 0)")

        # calculation
        colors = self._get_colors_func()(**self._get_inputs(timestamp, mask))

        # correction
        frame = torch.empty((*mask.shape, len(self.node.colors)), dtype=torch.float32)
        for i, col in enumerate(colors):
            if col.dtype.is_complex:
                col = torch.abs(col)
            torch.nan_to_num(col, nan=127.0/255.0, posinf=1.0, neginf=0.0, out=col)
            torch.clip(col, 0.0, 1.0, out=col)
            frame[:, :, i][mask] = col

        return frame

    @property
    def beginning(self) -> Fraction:
        index = (
            {int(str(s)[1:]) for s in self.node.free_symbols if re.fullmatch(r"[bgra]\d+", str(s))}
        )
        return min((self.node.in_streams[i].beginning for i in index), default=Fraction(0))

    @property
    def duration(self) -> typing.Union[Fraction, float]:
        index = (
            {int(str(s)[1:]) for s in self.node.free_symbols if re.fullmatch(r"[bgra]\d+", str(s))}
        )
        streams = (self.node.in_streams[i] for i in index)
        end = max((s.beginning + s.duration for s in streams), default=math.inf)
        return end - self.beginning
