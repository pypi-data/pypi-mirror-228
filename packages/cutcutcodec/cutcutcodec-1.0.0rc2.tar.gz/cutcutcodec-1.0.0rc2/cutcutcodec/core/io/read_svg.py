#!/usr/bin/env python3

"""
** Decodes the svg vectorial images based on `cairosvg` lib. **
---------------------------------------------------------------
"""


from fractions import Fraction
import math
import pathlib
import typing

import cairosvg
import cv2
import numpy as np
import torch

from cutcutcodec.core.classes.container import ContainerInput
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.classes.stream_video import StreamVideo
from cutcutcodec.core.exceptions import OutOfTimeRange



class ContainerInputSVG(ContainerInput):
    """
    ** Decode an svg image to a matricial image of any dimension. **

    Examples
    --------
    >>> from cutcutcodec.core.io.read_svg import ContainerInputSVG
    >>> (stream,) = ContainerInputSVG.default().out_streams
    >>> stream.snapshot(0, (12, 12))[..., 3]
    tensor([[  0,   0,   7, 110, 200, 244, 244, 200, 109,   7,   0,   0],
            [  0,  27, 208, 255, 255, 255, 255, 255, 255, 207,  27,   0],
            [  7, 208, 255, 255, 255, 255, 255, 255, 255, 255, 207,   7],
            [110, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 108],
            [201, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 199],
            [243, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 243],
            [243, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 241],
            [201, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 199],
            [109, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 108],
            [  7, 207, 255, 255, 255, 255, 255, 255, 255, 255, 207,   6],
            [  0,  27, 207, 255, 255, 255, 255, 255, 255, 207,  27,   0],
            [  0,   0,   6, 108, 199, 243, 243, 198, 108,   6,   0,   0]],
           dtype=torch.uint8)
    >>>
    """

    def __init__(self, bytestring=None, *, url=None, unsafe=False):
        """
        All parameters are transmitted to ``cairosvg.svg2png``.
        """
        if url is not None and pathlib.Path(url).is_file():
            with open(url, "rb") as file:
                bytestring, url = file.read(), None
        self.bytestring = bytestring
        self.url = url
        self.unsafe = unsafe

        super().__init__([_StreamVideoSVG(self)])

    def _getstate(self) -> dict:
        return {
            "bytestring": (
                self.bytestring.decode("utf-8") if self.bytestring is not None else None
            ),
            "url": (str(self.url) if self.url is not None else None),
            "unsafe": self.unsafe,
        }

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        keys = {"bytestring", "url", "unsafe"}
        assert set(state) == keys, set(state)-keys
        bytestring = (
            state["bytestring"] if state["bytestring"] is None
            else state["bytestring"].encode("utf8")
        )
        ContainerInputSVG.__init__(self, bytestring, url=state["url"], unsafe=state["unsafe"])

    @classmethod
    def default(cls):
        return cls(url="cutcutcodec/examples/logo.svg")


class _StreamVideoSVG(StreamVideo):
    """
    Parameters
    ----------
    height : int
        The preconised dimension i (vertical) of the picture in pxl (readonly).
    width : int
        The preconised dimension j (horizontal) of the picture in pxl (readonly).
    """

    is_space_continuous = True
    is_time_continuous = True

    def __init__(self, node: ContainerInputSVG):
        assert isinstance(node, ContainerInputSVG), node.__class__.__name__
        super().__init__(node)
        self._height, self._width = None, None
        self._img = None

    def _get_img(self, shape: tuple[int, int]) -> torch.Tensor:
        """
        ** Cache the image. **
        """
        if self._img is None or self._img[0] != shape:
            self._img = (
                shape,
                torch.from_numpy(
                    cv2.imdecode(
                        np.frombuffer(
                            cairosvg.svg2png(
                                self.node.bytestring,
                                url=self.node.url,
                                unsafe=self.node.unsafe,
                                output_height=shape[0],
                                output_width=shape[1],
                            ),
                            np.uint8,
                        ),
                        cv2.IMREAD_UNCHANGED,
                    ),
                ),
            )
        return self._img[1]

    def _snapshot(self, timestamp: Fraction, mask: torch.Tensor) -> torch.Tensor:
        if timestamp < 0:
            raise OutOfTimeRange(f"there is no audio frame at timestamp {timestamp} (need >= 0)")
        return self._get_img(mask.shape)

    @property
    def beginning(self) -> Fraction:
        return Fraction(0)

    @property
    def duration(self) -> typing.Union[Fraction, float]:
        return math.inf

    @property
    def height(self) -> int:
        """
        ** The preconised dimension i (vertical) of the picture in pxl. **
        """
        raise NotImplementedError

    @property
    def width(self) -> int:
        """
        ** The preconised dimension j (horizontal) of the picture in pxl. **
        """
        raise NotImplementedError
