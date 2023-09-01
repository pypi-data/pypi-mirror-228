#!/usr/bin/env python3

"""
** Allows to generate a fractal annimation. **
----------------------------------------------
"""


from fractions import Fraction
import math
import numbers
import typing

from sympy.core.basic import Basic
from sympy.core.symbol import Symbol
import torch

from cutcutcodec.core.classes.container import ContainerInput
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.classes.stream_video import StreamVideo
from cutcutcodec.core.compilation.parse import parse_to_sympy
from cutcutcodec.core.compilation.sympy_to_torch import Lambdify
from cutcutcodec.core.exceptions import OutOfTimeRange
from cutcutcodec.core.generation.video.fractal.geometry import deduce_all_bounds




class GeneratorVideoMandelbrot(ContainerInput):
    """
    ** Generation of an annimated mandelbrot fractal. **

    Attributes
    ----------
    bounds : tuple[sympy.core.expr.Expr, ...]
        The four i_min, i_max, j_min and j_max bounds expressions of `t` (readonly).

    Examples
    --------
    >>> from cutcutcodec.core.generation.video.fractal.mandelbrot import GeneratorVideoMandelbrot
    >>> (stream,) = GeneratorVideoMandelbrot.default().out_streams
    >>> stream.snapshot(0, (13, 9))[..., 0]
    tensor([[  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   2,   4,   6, 255,   6,   4,   2,   0],
            [  2,   4,   4,   6, 255,   6,   4,   4,   2],
            [  2,   4,   4,  10, 255,  10,   4,   4,   2],
            [  4,   4,   6,  36, 255,  36,   6,   4,   4],
            [  4,   4,   8,  38, 255,  38,   8,   4,   4],
            [  4,   6,  10,  20, 255,  20,  10,   6,   4],
            [  4,   6, 124, 255, 255, 255, 124,   6,   4],
            [  6,  10, 255, 255, 255, 255, 255,  10,   6],
            [  8, 255, 255, 255, 255, 255, 255, 255,   8],
            [  6,  12, 255, 255, 255, 255, 255,  12,   6],
            [  4,   6, 255, 255,  48, 255, 255,   6,   4],
            [  2,   4,   8,  10,   8,  10,   8,   4,   2]], dtype=torch.uint8)
    >>>
    """

    def __init__(self, bounds: dict[str, typing.Union[Basic, numbers.Real, str]]):
        """
        Parameters
        ----------
        bounds : dict[str, str or sympy.Basic]
            The 4 bounds expressions of the complex plan limit of pixels.
            The admitted keys are defined in
            ``cutcutcodec.core.generation.video.fractal.geometry.SYMBOLS``.
            If an expression is used, only the symbol `t` is available.
        """
        assert isinstance(bounds, dict), bounds.__class__.__name__
        assert all(isinstance(name, str) for name in bounds), bounds
        all_bounds = {
            name: parse_to_sympy(expr, symbols={"t": Symbol("t", real=True, positive=True)})
            for name, expr in bounds.items()
        }
        assert all(set(map(str, e.free_symbols)).issubset({"t"}) for e in all_bounds.values())
        all_bounds = deduce_all_bounds(**all_bounds)


        self._bounds = (
            all_bounds["i_min"],
            all_bounds["i_max"],
            all_bounds["j_min"],
            all_bounds["j_max"],
        )

        super().__init__([_StreamVideoMandelbrot(self)])

    def _getstate(self) -> dict:
        return {
            "bounds": dict(zip(("i_min", "i_max", "j_min", "j_max"), map(str, self._bounds)))
        }

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert set(state) == {"bounds"}, set(state)
        GeneratorVideoMandelbrot.__init__(self, **state)

    @property
    def bounds(self):
        """
        ** The four i_min, i_max, j_min and j_max bounds expressions of `t`. **
        """
        return self._bounds

    @classmethod
    def default(cls):
        return cls(bounds={"i_min": -2, "i_max": 0.47, "j_min": -1.12, "j_max": 1.12})


class _StreamVideoMandelbrot(StreamVideo):
    """
    ** Fractal video stream. **
    """

    is_space_continuous = True
    is_time_continuous = True

    def __init__(self, node: GeneratorVideoMandelbrot):
        assert isinstance(node, GeneratorVideoMandelbrot), node.__class__.__name__
        super().__init__(node)
        self._bounds_func = None # cache

    def _get_bounds_func(self) -> callable:
        """
        ** Allows to "compile" bounds equations at the last moment. **
        """
        if self._bounds_func is None:
            self._bounds_func = Lambdify(self.node.bounds, copy=False)
        return self._bounds_func

    def _get_complex_map(self, timestamp: Fraction, mask: torch.Tensor) -> torch.Tensor:
        """
        ** Compute the complex map, one complex number by pixel. **
        """
        i_min, i_max, j_min, j_max = self._get_bounds_func()(t=float(timestamp))
        i_min, i_max, j_min, j_max = i_min.item(), i_max.item(), j_min.item(), j_max.item()
        real, imag = torch.meshgrid(
            torch.linspace(i_min, i_max, mask.shape[0], dtype=torch.float64),
            torch.linspace(j_min, j_max, mask.shape[1], dtype=torch.float64),
            indexing="ij",
        )
        return torch.complex(real, imag)

    def _snapshot(self, timestamp: Fraction, mask: torch.Tensor) -> torch.Tensor:
        if timestamp < 0:
            raise OutOfTimeRange(f"there is no audio frame at timestamp {timestamp} (need >= 0)")

        # return torch.zeros((*mask.shape, 1), dtype=torch.float32)

        iterations = torch.zeros(mask.shape, dtype=torch.float32) # final returns tensor
        comp = self._get_complex_map(timestamp, mask)
        indexs_i, indexs_j = torch.meshgrid(
            torch.arange(mask.shape[0], dtype=int),
            torch.arange(mask.shape[1], dtype=int),
            indexing="ij",
        )
        indexs_i, indexs_j = indexs_i[mask], indexs_j[mask] # 1d
        serie = torch.zeros(mask.shape, dtype=torch.complex128) # 1d

        for i in range(128):
            serie[indexs_i, indexs_j] = serie[indexs_i, indexs_j]**2 + comp[indexs_i, indexs_j]
            end = serie[indexs_i, indexs_j].real**2 + serie[indexs_i, indexs_j].imag**2 >= 4.0
            iterations[indexs_i[end], indexs_j[end]] = i/128
            indexs_i, indexs_j = indexs_i[~end], indexs_j[~end]
        iterations[indexs_i, indexs_j] = 1.0

        return torch.unsqueeze(iterations, dim=2)

    @property
    def beginning(self) -> Fraction:
        return Fraction(0)

    @property
    def duration(self) -> typing.Union[Fraction, float]:
        return math.inf
